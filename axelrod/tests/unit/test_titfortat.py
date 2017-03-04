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
        self.second_play_test(C, D, C, D)

        outcomes = [(C, C), (C, D), (D, C), (C, D)]
        match = axelrod.Match((self.player(), axelrod.Alternator()), turns=4)
        self.assertEqual(match.play(), outcomes)

        outcomes = [(C, C), (C, C), (C, C), (C, C)]
        match = axelrod.Match((self.player(), axelrod.Cooperator()), turns=4)
        self.assertEqual(match.play(), outcomes)

        outcomes = [(C, D), (D, D), (D, D), (D, D)]
        match = axelrod.Match((self.player(), axelrod.Defector()), turns=4)
        self.assertEqual(match.play(), outcomes)


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
        # Starts by cooperating.
        self.first_play_test(C)
        # Will defect only when last two turns of opponent were defections.
        self.responses_test([D], [C, C, C], [D, D, D])
        self.responses_test([C], [C, C, D, D], [D, D, D, C])


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
        # Starts by cooperating.
        self.first_play_test(C)
        # Will defect twice when last turn of opponent was defection.
        self.responses_test([D], [C], [D])
        self.responses_test([D], [C, C], [D, D])
        self.responses_test([D], [C, C, C], [D, D, C])
        self.responses_test([C], [C, C, D, D], [D, D, C, C])


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
        self.second_play_test(D, C, D, C)


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
        # Will try defecting after two turns of cooperation, but will stop
        # if punished.
        self.responses_test([D], [C, C], [C, C])
        self.responses_test([C], [C, C, D, D], [C, C, C, D])


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
        self.second_play_test(C, D, C, D)


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


class TestHardTitForTat(TestPlayer):

    name = "Hard Tit For Tat"
    player = axelrod.HardTitForTat
    expected_classifier = {
        'memory_depth': 3,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating.
        self.first_play_test(C)
        # Repeats last action of opponent history.
        self.responses_test([C], [C, C, C], [C, C, C])
        self.responses_test([D], [C, C, C], [D, C, C])
        self.responses_test([D], [C, C, C], [C, D, C])
        self.responses_test([D], [C, C, C], [C, C, D])
        self.responses_test([C], [C, C, C, C], [D, C, C, C])


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
        # Repeats last action of opponent history.
        self.responses_test([C], [C, C, C], [C, C, C])
        self.responses_test([C], [C, C, C], [D, C, C])
        self.responses_test([C], [C, C, C], [C, D, C])
        self.responses_test([C], [C, C, C], [C, C, D])

        self.responses_test([C], [C, C, C], [D, C, D])
        self.responses_test([D], [C, C, C], [D, D, C])
        self.responses_test([D], [C, C, C], [C, D, D])

        self.responses_test([C], [C, C, C, C], [D, C, C, C])
        self.responses_test([C], [C, C, C, C], [D, D, C, C])
        self.responses_test([D], [C, C, C, C], [C, D, D, C])


class OmegaTFT(TestPlayer):

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
        for i in range(10):
            self.responses_test([C], [C] * i, [C] * i)

    def test_reset(self):
        player = self.player()
        opponent = axelrod.Defector()
        [player.play(opponent) for _ in range(10)]
        player.reset()
        self.assertEqual(player.randomness_counter, 0)
        self.assertEqual(player.deadlock_counter, 0)


class TestOmegaTFTvsSTFT(TestMatch):
    def test_rounds(self):
        self.versus_test(
            axelrod.OmegaTFT(), axelrod.SuspiciousTitForTat(),
            [C, D, C, D, C, C, C, C, C],
            [D, C, D, C, D, C, C, C, C]
        )


class TestOmegaTFTvsAlternator(TestMatch):
    def test_rounds(self):
        self.versus_test(
            axelrod.OmegaTFT(), axelrod.Alternator(),
            [C, C, D, C, D, C, C, C, D, C, C, C, D, D, D, D, D, D],
            [C, D, C, D, C, D, C, D, C, D, C, D, C, D, C, D, C, D]
        )


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
        self.responses_test([C], [C], [C], attrs={
            "calming": False,
            "punishing": False,
            "punishment_count": 0,
            "punishment_limit": 0
        })
        self.responses_test([D], [C], [D], attrs={
            "calming": False,
            "punishing": True,
            "punishment_count": 1,
            "punishment_limit": 1
        })
        self.responses_test([C], [C, D], [D, C], attrs={
            "calming": True,
            "punishing": False,
            "punishment_count": 0,
            "punishment_limit": 1
        })
        self.responses_test([C], [C, D, C], [D, C, D], attrs={
            "calming": False,
            "punishing": False,
            "punishment_count": 0,
            "punishment_limit": 1
        })
        self.responses_test([C], [C, D, C, C], [D, C, D, C], attrs={
            "calming": False,
            "punishing": False,
            "punishment_count": 0,
            "punishment_limit": 1
        })
        self.responses_test([C], [C, D, C, D, C], [D, C, D, C, C], attrs={
            "calming": False,
            "punishing": False,
            "punishment_count": 0,
            "punishment_limit": 1
        })
        self.responses_test([D], [C, D, C, D, C, C], [D, C, D, C, C, D], attrs={
            "calming": False,
            "punishing": True,
            "punishment_count": 1,
            "punishment_limit": 2
        })
        self.responses_test([D], [C, D, C, D, D, C, D], [D, C, D, C, C, D, C],
                            attrs={
                                "calming": False,
                                "punishing": True,
                                "punishment_count": 2,
                                "punishment_limit": 2
                            })
        self.responses_test([C], [C, D, C, D, D, C, D, D],
                            [D, C, D, C, C, D, C, C], attrs={
                "calming": True,
                "punishing": False,
                "punishment_count": 0,
                "punishment_limit": 2
            })
        self.responses_test([C], [C, D, C, D, D, C, D, D, C],
                            [D, C, D, C, C, D, C, C, C], attrs={
                "calming": False,
                "punishing": False,
                "punishment_count": 0,
                "punishment_limit": 2
            })

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
        player = axelrod.Gradual()

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
        self.responses_test([C], [C] * 2, [C, C])
        self.responses_test([C], [C] * 3, [C, D, C])
        self.responses_test([D], [C] * 3, [C, D, D])


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

        p1, p2 = self.player(), self.player()
        p1.play(p2)
        p1.play(p2)
        self.assertEqual(p2.world, 0.75)

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
        self.responses_test([C], [C] * 4, [C, C, C, C],
                            attrs={"retaliating": False})
        self.responses_test([D], [C] * 5, [C, C, C, C, D],
                            attrs={"retaliating": False})
        self.responses_test([D], [C] * 5, [C, C, D, D, C],
                            attrs={"retaliating": True})

    def test_reset_retaliating(self):
        player = self.player()
        player.retaliating = True
        player.reset()
        self.assertFalse(player.retaliating)
