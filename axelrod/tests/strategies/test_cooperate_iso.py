import random
import numpy as np

import axelrod as axl
from axelrod.action import Action
from axelrod.tests.strategies.test_player import TestPlayer
from axelrod.strategies.cooperate_iso import LongtermTfT, ISO, CooperateISO
from unittest.mock import patch, MagicMock

C, D = Action.C, Action.D

class TestLongtermTfT(TestPlayer):
    name = "LongtermTfT"
    player = LongtermTfT
    
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
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
        # (Player Action, Opponent Action)
        expected = [
            (C, C),  # T1: No history, defaults to C
            (C, D),  # T2: Mirrors Opponent's T1 (C)
            (D, D),  # T3: Mirrors Opponent's T2 (D)
            (D, C),  # T4: Mirrors Opponent's T3 (D)
            (C, C),  # T5: Mirrors Opponent's T4 (C)
        ]
        
        self.versus_test(
            opponent=axl.MockPlayer(actions=[C, D, D, C, C]),
            expected_actions=expected,
            match_attributes={"noise": 0.1}
        )

    def test_forgiveness_and_z_score_retaliation(self):
        """
        Tests the transition from TfT to the forgiving Z-score phase, 
        and verifies that it retaliates when Z >= 2.
        """
        # (Player Action, Opponent Action)
        expected = [
            (C, C),  # T1: History len 0
            (C, C),  # T2: History len 1
            (C, C),  # T3: n_c=1, n_d=0 -> TfT (plays C)
            (C, C),  # T4: n_c=2, n_d=0 -> TfT (plays C)
            (C, C),  # T5: n_c=3, n_d=0 -> TfT (plays C)
            
            # --- Z-Score Phase Begins (n_c reaches 4, about to be 5) ---
            (C, D),  # T6: n_c=4, n_d=0 -> TfT (plays C). Opp defects.
            
            # Opponent defected, but Z-score is low (Z=0.5), so player forgives.
            (C, D),  # T7: n_c=5, n_d=1 -> Forgives (plays C). Opp defects again.
            
            # Z-score climbs (Z=1.4) but stays < 2.
            (C, D),  # T8: n_c=6, n_d=2 -> Forgives (plays C). Opp defects 3rd time.
            
            # Z-score hits Z=2.3 (>= 2). Strategy falls back to TfT and retaliates.
            (D, C),  # T9: n_c=7, n_d=3 -> Retaliates (plays D). Opp plays C.
            
            # Mirroring Opponent's C from T9 (Z=2.2, TfT mode).
            (C, C),  # T10: n_c=8, n_d=3 -> TfT (plays C).
        ]
        
        self.versus_test(
            opponent=axl.MockPlayer(actions=[C, C, C, C, C, D, D, D, C, C]),
            expected_actions=expected,
            match_attributes={"noise": 0.1}
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
        """Unit test for the state indexing logic mapping history to 0,1,2,3."""
        player = self.player()
        opponent = axl.MockPlayer(actions=[C, D, C, D])
        
        # T1: No history -> Defaults to 0 (CC)
        self.assertEqual(player._get_state_idx(opponent), 0)
        
        # T2: CC
        # History.append(play, coplay)
        player.history.append(C, C)
        opponent.history.append(C, C)
        self.assertEqual(player._get_state_idx(opponent), 0)

        # T3: CD
        player.history.append(C, D)
        opponent.history.append(D, C)
        self.assertEqual(player._get_state_idx(opponent), 1)
        
        # T4: DC
        player.history.append(D, C)
        opponent.history.append(C, D)
        self.assertEqual(player._get_state_idx(opponent), 2)

        # T5: DD
        player.history.append(D, D)
        opponent.history.append(D, D)
        self.assertEqual(player._get_state_idx(opponent), 3)

    def test_update_opponent_model(self):
        """Unit test for the discounted moving average calculation."""
        player = self.player()
        opponent = axl.MockPlayer()
        
        # Turn 1: Both played C
        # history.append(action, coplay)
        player.history.append(C, C)
        opponent.history.append(C, C)
        
        # Turn 2: Player played C, Opponent played D
        player.history.append(C, D)
        opponent.history.append(D, C)
        
        player._update_opponent_model(opponent)
        
        # Check EWMA accumulator state [numerator, denominator] for CC
        # Initial state was [1.0, 1.0]; after seeing D (0.0):
        # num = 0.99 * 1.0 + 0.0 = 0.99
        # den = 0.99 * 1.0 + 1.0 = 1.99
        self.assertAlmostEqual(player.ewma_CC[0], 0.99, places=6)
        self.assertAlmostEqual(player.ewma_CC[1], 1.99, places=6)
        
        # Check discount logic: mean = num / den
        expected_mean = 0.99 / 1.99
        self.assertAlmostEqual(player.opp_model[0], expected_mean, places=4)

    @patch("axelrod.strategies.cooperate_iso.optimize_against")
    def test_strategy_with_mocked_optimizer(self, mock_optimize):
        """
        Tests the strategy execution loop deterministically by patching 
        out the PyTorch optimization step.
        """
        # We force the optimizer to return absolute 1.0 (C) or 0.0 (D) policies.
        # Policy structure: [P(C|CC), P(C|CD), P(C|DC), P(C|DD)]
        # We will make it always cooperate after CC, and always defect otherwise.
        mock_optimize.return_value = (3.0, [1.0, 0.0, 0.0, 0.0])
        
        # Because we return absolute probabilities, np.random.uniform() < pr_c
        # becomes strictly deterministic.
        expected = [
            (C, C),  # T1: No history -> Defaults to CC (idx 0) -> policy[0] is 1.0 (Plays C)
            (C, D),  # T2: T1 was (C, C) -> state CC (idx 0) -> policy[0] is 1.0 (Plays C)
            (D, D),  # T3: T2 was (C, D) -> state CD (idx 1) -> policy[1] is 0.0 (Plays D)
            (D, C),  # T4: T3 was (D, D) -> state DD (idx 3) -> policy[3] is 0.0 (Plays D)
        ]
        
        self.versus_test(
            opponent=axl.MockPlayer(actions=[C, D, D, C]),
            expected_actions=expected,
            match_attributes={"noise": 0.1}
        )

    def test_vs_random_defects(self):
        """ISO should learn to defect against a random player."""
        player = self.player()
        opponent = axl.Random()
        
        match = axl.Match([player, opponent], turns=200, noise=0.05, seed=42)
        match.play()

        print(player.opp_model)
        print(player.my_policy)
        for pr_c in player.my_policy:
            self.assertLess(pr_c, 0.1), player.my_policy
        
        self.assertEqual(player.history[-1], D)


    def test_vs_tit_for_tat_with_noise_cooperates(self):
        """Against TitForTat under noise, ISO should learn that cooperation avoids retaliation."""       
        player = self.player()
        opponent = axl.TitForTat()
        
        match = axl.Match([player, opponent], turns=200, noise=0.05, seed=42)
        match.play()

        print(player.opp_model)
        print(player.my_policy)
        for pr_c in player.my_policy:
            self.assertGreater(pr_c, 0.9), player.my_policy        

        self.assertEqual(player.history[-1], C)


    def test_optimization_runs(self):
        """Runs an actual match for a few turns to ensure optimization executes without crashing."""
        player = self.player()
        opponent = axl.MockPlayer(actions=[C, D, C])
        
        # Play a 3-turn match
        match = axl.Match([player, opponent], turns=3)
        match.play()
        
        self.assertEqual(len(player.history), 3)
        self.assertEqual(len(player.my_policy), 4)
        
        # Ensure all resulting policy probabilities are valid bounded floats
        for pr_c in player.my_policy:
            self.assertTrue(0.0 <= pr_c <= 1.0)

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

        # Turn 1: Mutual Cooperation (C, C) -> Should append R (3)
        player.history.append(C, C)
        opponent.history.append(C, C)
        player._update_reward_history(opponent)
        self.assertEqual(player.reward_history, [3])

        # Turn 2: Sucker's payoff (C, D) -> Should append S (0)
        player.history.append(C, D)
        opponent.history.append(D, C)
        player._update_reward_history(opponent)
        self.assertEqual(player.reward_history, [3, 0])

        # Turn 3: Temptation (D, C) -> Should append T (5)
        player.history.append(D, C)
        opponent.history.append(C, D)
        player._update_reward_history(opponent)
        self.assertEqual(player.reward_history, [3, 0, 5])

        # Turn 4: Punishment (D, D) -> Should append P (1)
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
        # ISO update always returns 0.0 (highly unprofitable)
        mock_update.return_value = 0.0
        
        expected = [
            (C, C),  # T1: No history, defaults to C
            (C, D),  # T2: Mirrors Opponent's T1 (C)
            (D, D),  # T3: Mirrors Opponent's T2 (D)
            (D, C),  # T4: Mirrors Opponent's T3 (D)
            (C, C),  # T5: Mirrors Opponent's T4 (C)
        ]
        
        self.versus_test(
            opponent=axl.MockPlayer(actions=[C, D, D, C, C]),
            expected_actions=expected,
            match_attributes={"noise": 0.0, "game": axl.DefaultGame}
        )
        # Because we never switched to ISO, act() should never have been called
        mock_act.assert_not_called()

    @patch("axelrod.strategies.cooperate_iso.ISO.update")
    @patch("axelrod.strategies.cooperate_iso.ISO.act")
    def test_switches_to_iso_when_profitable(self, mock_act, mock_update):
        """
        Tests the switch condition: if we have 10 rounds of history and ISO predicts
        a sufficiently high expected gain, the strategy flips to playing ISO.
        """
        # We will mock ISO to return D whenever it acts
        mock_act.return_value = D
        
        # We play 11 rounds. 
        # Turns 1-10: ISO predicts 3.0 (same as average for mutual cooperation, so expected_gain = 0)
        # Turn 11: ISO suddenly predicts 5.0. expected_gain (2.0) crosses the threshold.
        mock_update.side_effect = [3.0] * 9 + [5.0]

        # T1 to T10: Mutual cooperation (LongtermTfT mirroring)
        expected = [(C, C)] * 10
        
        # T11: The threshold is crossed, we switch to ISO, which our mock says will return D
        expected.append((D, C))

        self.versus_test(
            opponent=axl.MockPlayer(actions=[C] * 11),
            expected_actions=expected,
            match_attributes={"noise": 0.0, "game": axl.DefaultGame}
        )
        
        # Verify ISO took over on the final turn
        mock_act.assert_called_once()

    def test_set_seed(self):
        """Ensures random seeds are passed down to the inner ISO instance."""
        player = self.player()
        
        # Mock the internal ISO instance's set_seed method
        player.iso_instance.set_seed = MagicMock()
        
        player.set_seed(42)
        player.iso_instance.set_seed.assert_called_once_with(42)