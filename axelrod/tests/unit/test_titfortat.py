"""Tests for the tit for tat strategies."""

import random
from hypothesis import given
from hypothesis.strategies import integers
import axelrod
from axelrod.tests.property import strategy_lists
from .test_player import TestMatch, TestPlayer


C, D = axelrod.Actions.C, axelrod.Actions.D


class TestTitForTat(TestPlayer):
    """
    Note that this test is referred to in the documentation as an example on
    writing tests.  If you modify the tests here please also modify the
    documentation.
    """

    name = "Tit For Tat"
    player = axelrod.TitForTat
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        self.second_play_test(rCC=C, rCD=D, rDC=C, rDD=D)

        # Play against opponents
        outcomes = [(C, C), (C, D), (D, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_outcomes=outcomes)

        outcomes = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_outcomes=outcomes)

        outcomes = [(C, D), (D, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_outcomes=outcomes)

        # This behaviour is independent of knowledge of the Match length
        outcomes = [(C, C), (C, D), (D, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_outcomes=outcomes,
                         match_attributes={"length": -1})

        # We can also test against random strategies
        outcomes = [(C, D), (D, D), (D, C), (C, C)]
        self.versus_test(axelrod.Random(), expected_outcomes=outcomes,
                         seed=0)

        outcomes = [(C, C), (C, D), (D, D), (D, C)]
        self.versus_test(axelrod.Random(), expected_outcomes=outcomes,
                         seed=1)

        #  Play against sequence of moves
        opponent_sequence = [C, D]
        outcomes = [(C, C), (C, D), (D, C), (C, D)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes)

        opponent_sequence = [D, D]
        outcomes = [(C, D), (D, D), (D, D), (D, D)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes)

        opponent_sequence = [C, C, D, D, C, D]
        outcomes = [(C, C), (C, C), (C, D), (D, D), (D, C), (C, D)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes)


class TestTitFor2Tats(TestPlayer):

    name = 'Tit For 2 Tats'
    player = axelrod.TitFor2Tats
    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        self.second_play_test(rCC=C, rCD=C, rDC=C, rDD=C)

        # Will punish sequence of 2 defections but will forgive
        opponent_sequence = [D, D, D, C, C]
        outcomes = [(C, D), (C, D), (D, D), (D, C), (C, C)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes)


class TestTwoTitsForTat(TestPlayer):

    name = 'Two Tits For Tat'
    player = axelrod.TwoTitsForTat
    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        self.second_play_test(rCC=C, rCD=D, rDC=C, rDD=D)

        # Will defect twice when last turn of opponent was defection.
        opponent_sequence = [D, C, C, D, C]
        outcomes = [(C, D), (D, C), (D, C), (C, D), (D, C)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes)


class TestBully(TestPlayer):

    name = "Bully"
    player = axelrod.Bully
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by defecting.
        self.first_play_test(D)
        # Will do opposite of what opponent does.
        self.second_play_test(rCC=D, rCD=C, rDC=D, rDD=C)

        outcomes = [(D, C), (D, D), (C, C), (D, D), (C, C)]
        self.versus_test(axelrod.Alternator(), expected_outcomes=outcomes)

        outcomes = [(D, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(axelrod.Cooperator(), expected_outcomes=outcomes)

        outcomes = [(D, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(axelrod.Defector(), expected_outcomes=outcomes)


class TestSneakyTitForTat(TestPlayer):

    name = "Sneaky Tit For Tat"
    player = axelrod.SneakyTitForTat
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating.
        self.first_play_test(C)

        opponent_sequence = [C, C, C, D, C, C]
        outcomes = [(C, C), (C, C), (D, C), (D, D), (C, C), (C, C)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes)

        # Repents if punished for a defection
        outcomes = [(C, C), (C, D), (D, C), (C, D), (C, C)]
        self.versus_test(axelrod.Alternator(), expected_outcomes=outcomes)


class TestSuspiciousTitForTat(TestPlayer):

    name = 'Suspicious Tit For Tat'
    player = axelrod.SuspiciousTitForTat
    expected_classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by Defecting
        self.first_play_test(D)
        # Plays like TFT after the first move, repeating the opponents last
        # move.
        self.second_play_test(rCC=C, rCD=D, rDC=C, rDD=D)

        outcomes = [(D, C), (C, D)] * 8
        self.versus_test(axelrod.TitForTat(), expected_outcomes=outcomes)


class TestAntiTitForTat(TestPlayer):

    name = 'Anti Tit For Tat'
    player = axelrod.AntiTitForTat
    expected_classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by Cooperating
        self.first_play_test(C)
        # Will do opposite of what opponent does.
        self.second_play_test(D, C, D, C)

        outcomes = [(C, C), (D, C), (D, D), (C, D)] * 4
        self.versus_test(axelrod.TitForTat(), expected_outcomes=outcomes)


class TestHardTitForTat(TestPlayer):

    name = "Hard Tit For Tat"
    player = axelrod.HardTitForTat
    expected_classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating.
        self.first_play_test(C)

        opponent_sequence = [D, C, C, C, D, C]
        outcomes = [(C, D), (D, C), (D, C), (D, C), (C, D), (D, C)]
        self.versus_test(opponent_sequence, outcomes)


class TestHardTitFor2Tats(TestPlayer):

    name = "Hard Tit For 2 Tats"
    player = axelrod.HardTitFor2Tats
    expected_classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating.
        self.first_play_test(C)

        # Uses memory 3 to punish 2 consecutive defections
        opponent_sequence = [D, C, C, D, D, D, C]
        outcomes = [(C, D), (C, C), (C, C), (C, D), (C, D), (D, D), (D, C)]
        self.versus_test(opponent_sequence, outcomes)


class TestOmegaTFT(TestPlayer):

    name = "Omega TFT"
    player = axelrod.OmegaTFT

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating.
        self.first_play_test(C)

        player_history = [C, C, D, C, D, C, C, C, D, C, C, C, D, D, D, D, D, D]
        opp_history = [C, D] * 9
        expected_outcomes = list(zip(player_history, opp_history))
        self.versus_test(axelrod.Alternator(), expected_outcomes)

        player_history =  [C, D, C, D, C, C, C, C, C]
        opp_history = [D, C, D, C, D, C, C, C, C]
        expected_outcomes = list(zip(player_history, opp_history))
        self.versus_test(axelrod.SuspiciousTitForTat(), expected_outcomes)

    def test_reset(self):
        player = self.player()
        opponent = axelrod.Defector()
        [player.play(opponent) for _ in range(10)]
        player.reset()
        self.assertEqual(player.randomness_counter, 0)
        self.assertEqual(player.deadlock_counter, 0)


class TestGradual(TestPlayer):

    name = 'Gradual'
    player = axelrod.Gradual
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating.
        self.first_play_test(C)
        # Punishes defection with a growing number of defections and calms
        # the opponent with two cooperations in a row.
        opponent_sequence = [C]
        outcomes = [(C, C)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes,
                         attrs={"calming": False, "punishing": False,
                                "punishment_count": 0, "punishment_limit": 0})

        opponent_sequence = [D]
        outcomes = [(C, D)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes,
                         attrs={"calming": False, "punishing": False,
                                "punishment_count": 0, "punishment_limit": 0})

        opponent_sequence = [D, C]
        outcomes = [(C, D), (D, C)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes,
                         attrs={"calming": False, "punishing": True,
                                "punishment_count": 1, "punishment_limit": 1})

        opponent_sequence = [D, C, C]
        outcomes = [(C, D), (D, C), (C, C)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes,
                         attrs={"calming": True, "punishing": False,
                                "punishment_count": 0, "punishment_limit": 1})

        opponent_sequence = [D, C, D, C]
        outcomes = [(C, D), (D, C), (C, D), (C, C)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes,
                         attrs={"calming": False, "punishing": False,
                                "punishment_count": 0, "punishment_limit": 1})

        opponent_sequence = [D, C, D, C, C]
        outcomes = [(C, D), (D, C), (C, D), (C, C), (C, C)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes,
                         attrs={"calming": False, "punishing": False,
                                "punishment_count": 0, "punishment_limit": 1})

        opponent_sequence = [D, C, D, C, C, C]
        outcomes = [(C, D), (D, C), (C, D), (C, C), (C, C), (C, C)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes,
                         attrs={"calming": False, "punishing": False,
                                "punishment_count": 0, "punishment_limit": 1})

        opponent_sequence = [D, C, D, C, C, C, D, C]
        outcomes = [(C, D), (D, C), (C, D), (C, C),
                    (C, C), (C, C), (C, D), (D, C)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes,
                         attrs={"calming": False, "punishing": True,
                                "punishment_count": 1, "punishment_limit": 2})

        opponent_sequence = [D, C, D, C, C, D, D, D]
        outcomes = [(C, D), (D, C), (C, D), (C, C),
                    (C, C), (C, D), (D, D), (D, D)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes,
                         attrs={"calming": False, "punishing": True,
                                "punishment_count": 2, "punishment_limit": 2})

    def test_reset_cleans_all(self):
        p = axelrod.Gradual()
        p.calming = True
        p.punishing = True
        p.punishment_count = 1
        p.punishment_limit = 1
        p.reset()

        self.assertFalse(p.calming)
        self.assertFalse(p.punishing)
        self.assertEqual(p.punishment_count, 0)
        self.assertEqual(p.punishment_limit, 0)

    def test_output_from_literature(self):
        """
        This strategy is not fully described in the literature, however the
        following two results are reported in:

        Bruno Beaufils, Jean-Paul Delahaye, Philippe Mathie
        "Our Meeting With Gradual: A Good Strategy For The Iterated Prisoner's
        Dilemma" Proc. Artif. Life 1996

        This test just ensures that the strategy is as was originally defined.
        """
        player = self.player()

        opp1 = axelrod.Defector()
        match = axelrod.Match((player, opp1), 1000)
        match.play()
        self.assertEqual(match.final_score(), (915, 1340))

        opp2 = axelrod.CyclerCCD()
        match = axelrod.Match((player, opp2), 1000)
        match.play()
        self.assertEqual(match.final_score(), (3472, 767))


class TestContriteTitForTat(TestPlayer):

    name = "Contrite Tit For Tat"
    player = axelrod.ContriteTitForTat
    expected_classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    deterministic_strategies = [s for s in axelrod.strategies
                                if not s().classifier['stochastic']]

    @given(strategies=strategy_lists(strategies=deterministic_strategies,
                                     max_size=1),
           turns=integers(min_value=1, max_value=20))
    def test_is_tit_for_tat_with_no_noise(self, strategies, turns):
        tft = axelrod.TitForTat()
        ctft = self.player()
        opponent = strategies[0]()
        m1 = axelrod.Match((tft, opponent), turns)
        m2 = axelrod.Match((ctft, opponent), turns)
        self.assertEqual(m1.play(), m2.play())

    def test_strategy_with_noise(self):
        ctft = self.player()
        opponent = axelrod.Defector()
        self.assertEqual(ctft.strategy(opponent), C)
        self.assertEqual(ctft._recorded_history, [C])
        ctft.reset()  # Clear the recorded history
        self.assertEqual(ctft._recorded_history, [])

        random.seed(0)
        ctft.play(opponent, noise=.9)
        self.assertEqual(ctft.history, [D])
        self.assertEqual(ctft._recorded_history, [C])
        self.assertEqual(opponent.history, [C])

        # After noise: is contrite
        ctft.play(opponent)
        self.assertEqual(ctft.history, [D, C])
        self.assertEqual(ctft._recorded_history, [C, C])
        self.assertEqual(opponent.history, [C, D])
        self.assertTrue(ctft.contrite)

        # Cooperates and no longer contrite
        ctft.play(opponent)
        self.assertEqual(ctft.history, [D, C, C])
        self.assertEqual(ctft._recorded_history, [C, C, C])
        self.assertEqual(opponent.history, [C, D, D])
        self.assertFalse(ctft.contrite)

        # Goes back to playing tft
        ctft.play(opponent)
        self.assertEqual(ctft.history, [D, C, C, D])
        self.assertEqual(ctft._recorded_history, [C, C, C, D])
        self.assertEqual(opponent.history, [C, D, D, D])
        self.assertFalse(ctft.contrite)

    def test_reset_cleans_all(self):
        p = self.player()
        p.contrite = True
        p.reset()
        self.assertFalse(p.contrite)


class TestSlowTitForTwoTats(TestPlayer):

    name = "Slow Tit For Two Tats"
    player = axelrod.SlowTitForTwoTats
    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating.
        self.first_play_test(C)
        # If opponent plays the same move twice, repeats last action of
        # opponent history.
        opponent_sequence = [C, C, D, D, C, D, D, C, C, D, D]
        outcomes = [(C, C), (C, C), (C, D), (C, D), (D, C), (C, D), (C, D),
                    (D, C), (C, C), (C, D), (C, D)]
        self.versus_test(opponent_sequence, outcomes)


class TestAdaptiveTitForTat(TestPlayer):

    name = "Adaptive Tit For Tat: 0.5"
    player = axelrod.AdaptiveTitForTat
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Start by cooperating.
        self.first_play_test(C)
        self.second_play_test(C, D, C, D)

        outcomes = [(C, C), (C, C)]
        self.versus_test(self.player(), expected_outcomes=outcomes,
                         attrs={"world":0.75, "rate":0.5})

    def test_world_rate_reset(self):
        p1, p2 = self.player(), self.player()
        p1.play(p2)
        p1.play(p2)
        p2.reset()
        self.assertEqual(p2.world, 0.5)
        self.assertEqual(p2.rate, 0.5)


class TestSpitefulTitForTat(TestPlayer):
    name = "Spiteful Tit For Tat"
    player = axelrod.SpitefulTitForTat
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating.
        self.first_play_test(C)
        # Repeats last action of opponent history until 2 consecutive
        # defections, then always defects
        self.second_play_test(C, D, C, D)

        opponent_sequence = [C, C, C, C]
        outcomes = [(C, C)] * 5
        self.versus_test(opponent_sequence, expected_outcomes=outcomes,
                         attrs={"retaliating": False})

        opponent_sequence = [C, C, C, C, D, C]
        outcomes = [(C, C)] * 4 + [(C, D), (D, C)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes,
                         attrs={"retaliating": False})

        opponent_sequence = [C, C, D, D, C]
        outcomes = [(C, C), (C, C), (C, D), (D, D), (D, C)]
        self.versus_test(opponent_sequence, expected_outcomes=outcomes,
                         attrs={"retaliating": True})

    def test_reset_retaliating(self):
        player = self.player()
        player.retaliating = True
        player.reset()
        self.assertFalse(player.retaliating)
