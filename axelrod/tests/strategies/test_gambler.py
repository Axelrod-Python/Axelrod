"""Test for the Gambler strategy.
Most tests come form the LookerUp test suite.
"""

import copy

import axelrod
from .test_player import TestPlayer, TestMatch

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGambler(TestPlayer):

    name = "Gambler"
    player = axelrod.Gambler

    expected_classifier = {
        'memory_depth': 1,  # Default TFT table
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    expected_class_classifier = copy.copy(expected_classifier)
    expected_class_classifier['memory_depth'] = float('inf')

    def test_init(self):
        # Test empty table
        player = self.player(lookup_table=dict())
        opponent = axelrod.Cooperator()
        self.assertEqual(player.strategy(opponent), C)
        # Test default table
        tft_table = {
            ('', 'C', 'D'): 0,
            ('', 'D', 'D'): 0,
            ('', 'C', 'C'): 1,
            ('', 'D', 'C'): 1,
        }
        player = self.player(lookup_table=tft_table)
        opponent = axelrod.Defector()
        player.play(opponent)
        self.assertEqual(player.history[-1], C)
        player.play(opponent)
        self.assertEqual(player.history[-1], D)
        # Test malformed tables
        table = {(C, C, C): 1, ('DD', 'DD', 'C'): 1}
        with self.assertRaises(ValueError):
            player = self.player(lookup_table=table)

    def test_strategy(self):
        self.responses_test([C], [C] * 4, [C, C, C, C])
        self.responses_test([D], [C] * 5, [C, C, C, C, D])

    def test_defector_table(self):
        """
        Testing a lookup table that always defects if there is enough history.
        In order for the testing framework to be able to construct new player
        objects for the test, self.player needs to be callable with no
        arguments, thus we use a lambda expression which will call the
        constructor with the lookup table we want.
        """
        defector_table = {
            ('', C, D): 0,
            ('', D, D): 0,
            ('', C, C): 0,
            ('', D, C): 0,
        }
        self.player = lambda : axelrod.Gambler(lookup_table=defector_table)
        self.responses_test([D], [C, C], [C, C])
        self.responses_test([D], [C, D], [D, C])
        self.responses_test([D], [D, D], [D, D])


class TestPSOGamblerMem1(TestPlayer):

    name = "PSO Gambler Mem1"
    player = axelrod.PSOGamblerMem1

    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    expected_class_classifier = copy.copy(expected_classifier)
    expected_class_classifier['memory_depth'] = float('inf')

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)
        self.responses_test([C], [C] * 197, [C] * 197)


class TestPSOGambler2_2_2(TestPlayer):

    name = "PSO Gambler 2_2_2"
    player = axelrod.PSOGambler2_2_2

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_init(self):
        # Check for a few known keys
        known_pairs = {('CD', 'DD', 'DD'): 0.24523149,
                       ('CD', 'CC', 'DD'): 0.}
        player = self.player()
        for k, v in known_pairs.items():
            self.assertEqual(player.lookup_table[k], v)

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)
        self.responses_test([C], [C] * 197, [C] * 197)


class TestPSOGambler1_1_1(TestPlayer):

    name = "PSO Gambler 1_1_1"
    player = axelrod.PSOGambler1_1_1

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)
        self.responses_test([C], [C] * 197, [C] * 197)


class TestPSOGambler2_2_2_Noise05(TestPlayer):
    name = "PSO Gambler 2_2_2 Noise 05"
    player = axelrod.PSOGambler2_2_2_Noise05

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)
        self.responses_test([C], [C] * 197, [C] * 197)


# Some heads up tests for PSOGambler
class PSOGambler2_2_2vsDefector(TestMatch):
    def test_vs(self):
        self.versus_test(axelrod.PSOGambler2_2_2(), axelrod.Defector(),
                         [C, C, D, D], [D, D, D, D])


class PSOGambler2_2_2vsCooperator(TestMatch):
    def test_vs(self):
        self.versus_test(axelrod.PSOGambler2_2_2(), axelrod.Cooperator(),
                         [C, C, C, C], [C, C, C, C])


class PSOGambler2_2_2vsTFT(TestMatch):
    def test_vs(self):
        self.versus_test(axelrod.PSOGambler2_2_2(), axelrod.TitForTat(),
                         [C, C, C, C], [C, C, C, C])


class PSOGambler2_2_2vsAlternator(TestMatch):
    def test_vs(self):
        axelrod.seed(10)
        self.versus_test(axelrod.PSOGambler2_2_2(), axelrod.Alternator(),
                         [C, C, C, C, C, C, C], [C, D, C, D, C, D, C])
