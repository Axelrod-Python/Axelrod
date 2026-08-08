import random
from unittest.mock import MagicMock, patch

import numpy as np

import axelrod as axl
from axelrod.action import Action
from axelrod.strategies.cooperate_iso import ISO, CooperateISO, LongtermTfT
from axelrod.tests.strategies.test_player import TestPlayer

C, D = Action.C, Action.D


class TestLongtermTfT(TestPlayer):
    name = "LongtermTfT"
    player = LongtermTfT

    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": {"noise"},
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_early_rounds_tit_for_tat(self):
        """
        Tests that the strategy strictly defaults to Tit-for-Tat
        when the threshold conditions (n_tft_would_c < 5) are active.
        """
        expected = [(C, C), (C, D), (D, D), (D, C),(C, C)]
        _, opponent_actions = zip(*expected)

        self.versus_test(
            opponent=axl.MockPlayer(actions=opponent_actions),
            expected_actions=expected,
            match_attributes={"noise": 0.1},
        )

    def test_forgiveness_and_z_score_retaliation(self):
        """
        Tests the transition from TfT to the forgiving Z-score phase,
        and verifies that it retaliates when Z >= 2.

        Z >= 2 is reached on the 9th turn (n_c=7, n_d=3), so we retaliate.
        """
        # (Player Action, Opponent Action)
        expected = [
            (C, C), 
            (C, C),
            (C, C),
            (C, C),
            (C, C),
            (C, D),
            (
                C,
                D,
            ),
            (
                C,
                D,
            ),
            (D, C),
            (C, C),
        ]

        self.versus_test(
            opponent=axl.MockPlayer(actions=[C, C, C, C, C, D, D, D, C, C]),
            expected_actions=expected,
            match_attributes={"noise": 0.1},
        )


class TestISO(TestPlayer):
    name = "ISO"
    player = ISO

    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": {"noise", "game"},
        "long_run_time": True,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_get_state_idx(self):
        """Unit test for the state indexing logic mapping history to 0,1,2,3.
        
        Also testing invalid values -> -1."""
        player = self.player()
        opponent = axl.MockPlayer(actions=[C, D, C, D])

        self.assertEqual(player._get_state_idx(opponent), 0)

        player.history.append(C, C)
        opponent.history.append(C, C)
        self.assertEqual(player._get_state_idx(opponent), 0)

        player.history.append(C, D)
        opponent.history.append(D, C)
        self.assertEqual(player._get_state_idx(opponent), 1)

        player.history.append(D, C)
        opponent.history.append(C, D)
        self.assertEqual(player._get_state_idx(opponent), 2)

        player.history.append(D, D)
        opponent.history.append(D, D)
        self.assertEqual(player._get_state_idx(opponent), 3)

        player.history.append("C", "C")
        opponent.history.append("C", "C")
        self.assertEqual(player._get_state_idx(opponent), -1)

    def test_update_opponent_model(self):
        """Unit test for the discounted moving average calculation."""
        player = self.player()
        opponent = axl.MockPlayer()

        player.history.append(C, C)
        opponent.history.append(C, C)

        player.history.append(C, D)
        opponent.history.append(D, C)

        player._update_opponent_model(opponent)

        self.assertAlmostEqual(player.ewma_CC[0], 0.99, places=6)
        self.assertAlmostEqual(player.ewma_CC[1], 1.99, places=6)

        expected_mean = 0.99 / 1.99
        self.assertAlmostEqual(player.opp_model[0], expected_mean, places=4)

    def test_vs_random_defects(self):
        """ISO should learn to defect against a random player."""
        player = self.player()
        opponent = axl.Random()

        match = axl.Match([player, opponent], turns=200, noise=0.05, seed=42)
        match.play()

        for pr_c in player.my_policy:
            self.assertLess(pr_c, 0.1), player.my_policy

        self.assertEqual(player.history[-1], D)

    def test_vs_tit_for_tat_with_noise_cooperates(self):
        """Against TitForTat under noise, ISO should learn that cooperation avoids retaliation."""
        player = self.player()
        opponent = axl.TitForTat()

        match = axl.Match([player, opponent], turns=200, noise=0.05, seed=42)
        match.play()

        for pr_c in player.my_policy:
            self.assertGreater(pr_c, 0.9), player.my_policy

        self.assertEqual(player.history[-1], C)


class TestCooperateISO(TestPlayer):
    name = "CooperateISO"
    player = CooperateISO

    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": {"noise", "game"},
        "long_run_time": True,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_update_reward_history(self):
        """Unit test for ensuring the reward history accurately maps RPST to match states."""
        player = self.player()
        player.RPST = (3, 1, 0, 5)
        opponent = axl.MockPlayer()

        player.history.append(C, C)
        opponent.history.append(C, C)
        player._update_reward_history(opponent)
        self.assertEqual(player.reward_history, [3])

        player.history.append(C, D)
        opponent.history.append(D, C)
        player._update_reward_history(opponent)
        self.assertEqual(player.reward_history, [3, 0])

        player.history.append(D, C)
        opponent.history.append(C, D)
        player._update_reward_history(opponent)
        self.assertEqual(player.reward_history, [3, 0, 5])

        player.history.append(D, D)
        opponent.history.append(D, D)
        player._update_reward_history(opponent)
        self.assertEqual(player.reward_history, [3, 0, 5, 1])

    @patch("axelrod.strategies.cooperate_iso.ISO.update")
    @patch("axelrod.strategies.cooperate_iso.ISO.act")
    def test_maintains_tft_when_iso_not_profitable(self, mock_act, mock_update):
        """
        Tests that if ISO's expected reward does not beat the historical average,
        the strategy maintains LongtermTfT behavior.
        """
        mock_update.return_value = 0.0

        expected = [
            (C, C),
            (C, D),
            (D, D),
            (D, C),
            (C, C),
        ]

        self.versus_test(
            opponent=axl.MockPlayer(actions=[C, D, D, C, C]),
            expected_actions=expected,
            match_attributes={"noise": 0.0, "game": axl.DefaultGame},
        )
        mock_act.assert_not_called()

    @patch("axelrod.strategies.cooperate_iso.ISO.update")
    @patch("axelrod.strategies.cooperate_iso.ISO.act")
    def test_switches_to_iso_when_profitable(self, mock_act, mock_update):
        """
        Tests the switch condition: if we have 10 rounds of history and ISO predicts
        a sufficiently high expected gain, the strategy flips to playing ISO.
        """
        mock_act.return_value = D

        mock_update.side_effect = [3.0] * 9 + [5.0]

        expected = [(C, C)] * 10

        expected.append((D, C))

        self.versus_test(
            opponent=axl.MockPlayer(actions=[C] * 11),
            expected_actions=expected,
            match_attributes={"noise": 0.0, "game": axl.DefaultGame},
        )

        mock_act.assert_called_once()

    @patch("axelrod.strategies.cooperate_iso.ISO.update")
    @patch("axelrod.strategies.cooperate_iso.ISO.act")
    @patch("axelrod.strategies.cooperate_iso.ISO.strategy")
    def test_continues_playing_iso_on_subsequent_turns(
        self, mock_strategy, mock_act, mock_update
    ):
        """
        Tests that once playing_iso is True, strategy() delegates directly
        to self.iso_instance.strategy(opponent) on following turns.
        """
        mock_act.return_value = D
        mock_strategy.return_value = D

        mock_update.side_effect = [3.0] * 9 + [5.0, 5.0]

        expected = [(C, C)] * 10 + [(D, C), (D, C)]

        self.versus_test(
            opponent=axl.MockPlayer(actions=[C] * 12),
            expected_actions=expected,
            match_attributes={"noise": 0.0, "game": axl.DefaultGame},
        )

        mock_act.assert_called_once()
        mock_strategy.assert_called_once()

    def test_set_seed(self):
        """Ensures random seeds are passed down to the inner ISO instance."""
        player = self.player()

        player.iso_instance.set_seed = MagicMock()

        player.set_seed(42)
        player.iso_instance.set_seed.assert_called_once_with(42)
