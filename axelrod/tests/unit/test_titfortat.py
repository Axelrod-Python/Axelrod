"""Test for the tit for tat strategies."""

import axelrod
from .test_player import TestHeadsUp, TestPlayer

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
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Repeats last action of opponent history."""
        self.markov_test([C, D, C, D])
        self.responses_test([C] * 4, [C, C, C, C], [C])
        self.responses_test([C] * 5, [C, C, C, C, D], [D])


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
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Will defect only when last two turns of opponent were defections."""
        self.responses_test([C, C, C], [D, D, D], [D])
        self.responses_test([C, C, D, D], [D, D, D, C], [C])


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
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Will defect twice when last turn of opponent was defection."""
        self.responses_test([C], [D], [D])
        self.responses_test([C, C], [D, D], [D])
        self.responses_test([C, C, C], [D, D, C], [D])
        self.responses_test([C, C, D, D], [D, D, C, C], [C])


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
        """Starts by defecting"""
        self.first_play_test(D)

    def test_affect_of_strategy(self):
        """Will do opposite of what opponent does."""
        self.markov_test([D, C, D, C])


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
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Will try defecting after two turns of cooperation, but will stop if punished."""
        self.responses_test([C, C], [C, C], [D])
        self.responses_test([C, C, D, D], [C, C, C, D], [C])


class TestSuspiciousTitForTat(TestPlayer):

    name = 'Suspicious Tit For Tat'
    player = axelrod.SuspiciousTitForTat
    expected_classifier = {
        'memory_depth': 1, # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by Defecting"""
        self.first_play_test(D)

    def test_affect_of_strategy(self):
        """Plays like TFT after the first move, repeating the opponents last move."""
        self.markov_test([C, D, C, D])


class TestAntiTitForTat(TestPlayer):

    name = 'Anti Tit For Tat'
    player = axelrod.AntiTitForTat
    expected_classifier = {
        'memory_depth': 1, # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by Cooperating"""
        self.first_play_test(C)

    def test_affect_of_strategy(self):
        """Will do opposite of what opponent does."""
        self.markov_test([D, C, D, C])


class TestHardTitForTat(TestPlayer):

    name = "Hard Tit For Tat"
    player = axelrod.HardTitForTat
    expected_classifier = {
        'memory_depth': 3, # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Repeats last action of opponent history."""
        self.responses_test([C, C, C], [C, C, C], [C])
        self.responses_test([C, C, C], [D, C, C], [D])
        self.responses_test([C, C, C], [C, D, C], [D])
        self.responses_test([C, C, C], [C, C, D], [D])
        self.responses_test([C, C, C, C], [D, C, C, C], [C])


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
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Repeats last action of opponent history."""
        self.responses_test([C, C, C], [C, C, C], [C])
        self.responses_test([C, C, C], [D, C, C], [C])
        self.responses_test([C, C, C], [C, D, C], [C])
        self.responses_test([C, C, C], [C, C, D], [C])

        self.responses_test([C, C, C], [D, C, D], [C])
        self.responses_test([C, C, C], [D, D, C], [D])
        self.responses_test([C, C, C], [C, D, D], [D])

        self.responses_test([C, C, C, C], [D, C, C, C], [C])
        self.responses_test([C, C, C, C], [D, D, C, C], [C])
        self.responses_test([C, C, C, C], [C, D, D, C], [D])


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
        """Starts by cooperating."""
        self.first_play_test(C)
        for i in range(10):
            self.responses_test([C] * i, [C] * i, [C])

    def test_reset(self):
        player = self.player()
        opponent = axelrod.Defector()
        [player.play(opponent) for _ in range(10)]
        player.reset()
        self.assertEqual(player.randomness_counter, 0)
        self.assertEqual(player.deadlock_counter, 0)


class TestOmegaTFTvsSTFT(TestHeadsUp):
    def test_rounds(self):
        outcomes = zip()
        self.versus_test(axelrod.OmegaTFT(), axelrod.SuspiciousTitForTat(),
                         [C, D, C, D, C, C, C, C, C],
                         [D, C, D, C, D, C, C, C, C])

class TestOmegaTFTvsAlternator(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.OmegaTFT(), axelrod.Alternator(),
                         [C, C, D, C, D, C, C, C, D, C, C, C, D, D, D, D, D, D],
                         [C, D, C, D, C, D, C, D, C, D, C, D, C, D, C, D, C, D])


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
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Punishes defection with a growing number of defections and calms
        the opponent with two Cooperations in a row"""
        self.responses_test([C], [C], [C], attrs={"calming": False,
                            "punishing": False, "punishment_count": 0,
                            "punishment_limit": 0})
        self.responses_test([C], [D], [D], attrs={"calming": False,
                            "punishing": True, "punishment_count": 1,
                            "punishment_limit": 1})
        self.responses_test([C, D], [D, C], [C], attrs={"calming": True,
                            "punishing": False, "punishment_count": 0,
                            "punishment_limit": 1})
        self.responses_test([C, D, C], [D, C, D], [C], attrs={"calming": False,
                            "punishing": False, "punishment_count": 0,
                            "punishment_limit": 1})
        self.responses_test([C, D, C, C], [D, C, D, C], [C],
                            attrs={"calming": False, "punishing": False,
                            "punishment_count": 0, "punishment_limit": 1})
        self.responses_test([C, D, C, D, C], [D, C, D, C, C], [C],
                            attrs={"calming": False, "punishing": False,
                            "punishment_count": 0, "punishment_limit": 1})
        self.responses_test([C, D, C, D, C, C], [D, C, D, C, C, D], [D],
                            attrs={"calming": False, "punishing": True,
                            "punishment_count": 1, "punishment_limit": 2})
        self.responses_test([C, D, C, D, D, C, D], [D, C, D, C, C, D, C], [D],
                            attrs={"calming": False, "punishing": True,
                            "punishment_count": 2, "punishment_limit": 2})
        self.responses_test([C, D, C, D, D, C, D, D],
                            [D, C, D, C, C, D, C, C], [C],
                            attrs={"calming": True, "punishing": False,
                            "punishment_count": 0, "punishment_limit": 2})
        self.responses_test([C, D, C, D, D, C, D, D, C],
                            [D, C, D, C, C, D, C, C, C], [C],
                            attrs={"calming": False, "punishing": False,
                            "punishment_count": 0, "punishment_limit": 2})

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

        This test just ensures that the strategy is as was originally defined
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
