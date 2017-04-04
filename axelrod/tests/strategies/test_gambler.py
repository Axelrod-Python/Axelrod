"""Test for the Gambler strategy.
Most tests come form the LookerUp test suite.
"""

import copy

import axelrod
from .test_player import TestPlayer, TestMatch
from .test_lookerup import convert_original_to_current

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
            ((C,), (D,), ()): 0,
            ((D,), (D,), ()): 0,
            ((C,), (C,), ()): 1,
            ((D,), (C,), ()): 1
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
            ((C,), (D,), ()): 0,
            ((D,), (D,), ()): 0,
            ((C,), (C,), ()): 0,
            ((D,), (C,), ()): 0
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

    def test_new_data(self):
        original_data = {
            ('', 'C', 'C'): 1.0,
            ('', 'C', 'D'): 0.52173487,
            ('', 'D', 'C'): 0.0,
            ('', 'D', 'D'): 0.12050939}
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_table, converted_original)

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

    def test_new_data(self):
        original_data = {
            ('C', 'C', 'C'): 1.0,
            ('C', 'C', 'D'): 0.12304797,
            ('C', 'D', 'C'): 0.0,
            ('C', 'D', 'D'): 0.13581423,
            ('D', 'C', 'C'): 1.0,
            ('D', 'C', 'D'): 0.57740178,
            ('D', 'D', 'C'): 0.0,
            ('D', 'D', 'D'): 0.11886807}
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_table, converted_original)

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

    def test_new_data(self):
        original_data = {
            ('CC', 'CC', 'CC'): 1.0,
            ('CC', 'CC', 'CD'): 1.0,
            ('CC', 'CC', 'DC'): 0.0,
            ('CC', 'CC', 'DD'): 0.02126434,
            ('CC', 'CD', 'CC'): 0.0,
            ('CC', 'CD', 'CD'): 1.0,
            ('CC', 'CD', 'DC'): 1.0,
            ('CC', 'CD', 'DD'): 0.0,
            ('CC', 'DC', 'CC'): 0.0,
            ('CC', 'DC', 'CD'): 0.0,
            ('CC', 'DC', 'DC'): 0.0,
            ('CC', 'DC', 'DD'): 0.0,
            ('CC', 'DD', 'CC'): 0.0,
            ('CC', 'DD', 'CD'): 0.0,
            ('CC', 'DD', 'DC'): 0.0,
            ('CC', 'DD', 'DD'): 1.0,
            ('CD', 'CC', 'CC'): 1.0,
            ('CD', 'CC', 'CD'): 0.95280465,
            ('CD', 'CC', 'DC'): 0.80897541,
            ('CD', 'CC', 'DD'): 0.0,
            ('CD', 'CD', 'CC'): 0.0,
            ('CD', 'CD', 'CD'): 0.0,
            ('CD', 'CD', 'DC'): 0.0,
            ('CD', 'CD', 'DD'): 0.65147565,
            ('CD', 'DC', 'CC'): 0.15412392,
            ('CD', 'DC', 'CD'): 0.24922166,
            ('CD', 'DC', 'DC'): 0.0,
            ('CD', 'DC', 'DD'): 0.0,
            ('CD', 'DD', 'CC'): 0.0,
            ('CD', 'DD', 'CD'): 0.0,
            ('CD', 'DD', 'DC'): 0.0,
            ('CD', 'DD', 'DD'): 0.24523149,
            ('DC', 'CC', 'CC'): 1.0,
            ('DC', 'CC', 'CD'): 0.0,
            ('DC', 'CC', 'DC'): 0.0,
            ('DC', 'CC', 'DD'): 0.43278586,
            ('DC', 'CD', 'CC'): 1.0,
            ('DC', 'CD', 'CD'): 0.0,
            ('DC', 'CD', 'DC'): 0.23563137,
            ('DC', 'CD', 'DD'): 1.0,
            ('DC', 'DC', 'CC'): 1.0,
            ('DC', 'DC', 'CD'): 1.0,
            ('DC', 'DC', 'DC'): 0.00227615,
            ('DC', 'DC', 'DD'): 0.0,
            ('DC', 'DD', 'CC'): 0.0,
            ('DC', 'DD', 'CD'): 0.0,
            ('DC', 'DD', 'DC'): 0.0,
            ('DC', 'DD', 'DD'): 1.0,
            ('DD', 'CC', 'CC'): 0.0,
            ('DD', 'CC', 'CD'): 0.0,
            ('DD', 'CC', 'DC'): 0.0,
            ('DD', 'CC', 'DD'): 0.0,
            ('DD', 'CD', 'CC'): 0.15140743,
            ('DD', 'CD', 'CD'): 0.0,
            ('DD', 'CD', 'DC'): 0.0,
            ('DD', 'CD', 'DD'): 0.0,
            ('DD', 'DC', 'CC'): 0.0,
            ('DD', 'DC', 'CD'): 0.0,
            ('DD', 'DC', 'DC'): 0.0,
            ('DD', 'DC', 'DD'): 1.0,
            ('DD', 'DD', 'CC'): 0.0,
            ('DD', 'DD', 'CD'): 1.0,
            ('DD', 'DD', 'DC'): 0.77344942,
            ('DD', 'DD', 'DD'): 0.0}
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_table, converted_original)

    def test_init(self):
        # Check for a few known keys
        known_pairs = {
            ((D, D), (D, D), (C, D)): 0.24523149,
            ((D, D), (C, C), (C, D)): 0,
        }
        player = self.player()
        for k, v in known_pairs.items():
            self.assertEqual(player.lookup_table[k], v)

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

    def test_new_data(self):
        original_data = {
            ('CC', 'CC', 'CC'): 1.0,
            ('CC', 'CC', 'CD'): 0.0,
            ('CC', 'CC', 'DC'): 1.0,
            ('CC', 'CC', 'DD'): 0.63548102,
            ('CC', 'CD', 'CC'): 1.0,
            ('CC', 'CD', 'CD'): 1.0,
            ('CC', 'CD', 'DC'): 1.0,
            ('CC', 'CD', 'DD'): 0.0,
            ('CC', 'DC', 'CC'): 0.0,
            ('CC', 'DC', 'CD'): 1.0,
            ('CC', 'DC', 'DC'): 0.0,
            ('CC', 'DC', 'DD'): 0.0,
            ('CC', 'DD', 'CC'): 1.0,
            ('CC', 'DD', 'CD'): 0.0,
            ('CC', 'DD', 'DC'): 0.0,
            ('CC', 'DD', 'DD'): 0.0,
            ('CD', 'CC', 'CC'): 1.0,
            ('CD', 'CC', 'CD'): 1.0,
            ('CD', 'CC', 'DC'): 0.0,
            ('CD', 'CC', 'DD'): 0.0,
            ('CD', 'CD', 'CC'): 0.0,
            ('CD', 'CD', 'CD'): 0.13863175,
            ('CD', 'CD', 'DC'): 1.0,
            ('CD', 'CD', 'DD'): 0.7724137,
            ('CD', 'DC', 'CC'): 0.0,
            ('CD', 'DC', 'CD'): 1.0,
            ('CD', 'DC', 'DC'): 0.0,
            ('CD', 'DC', 'DD'): 0.07127653,
            ('CD', 'DD', 'CC'): 0.0,
            ('CD', 'DD', 'CD'): 1.0,
            ('CD', 'DD', 'DC'): 0.28124022,
            ('CD', 'DD', 'DD'): 0.0,
            ('DC', 'CC', 'CC'): 0.0,
            ('DC', 'CC', 'CD'): 0.98603825,
            ('DC', 'CC', 'DC'): 0.0,
            ('DC', 'CC', 'DD'): 0.0,
            ('DC', 'CD', 'CC'): 1.0,
            ('DC', 'CD', 'CD'): 0.06434619,
            ('DC', 'CD', 'DC'): 1.0,
            ('DC', 'CD', 'DD'): 1.0,
            ('DC', 'DC', 'CC'): 1.0,
            ('DC', 'DC', 'CD'): 0.50999729,
            ('DC', 'DC', 'DC'): 0.00524508,
            ('DC', 'DC', 'DD'): 1.0,
            ('DC', 'DD', 'CC'): 1.0,
            ('DC', 'DD', 'CD'): 1.0,
            ('DC', 'DD', 'DC'): 1.0,
            ('DC', 'DD', 'DD'): 1.0,
            ('DD', 'CC', 'CC'): 0.0,
            ('DD', 'CC', 'CD'): 1.0,
            ('DD', 'CC', 'DC'): 0.16240799,
            ('DD', 'CC', 'DD'): 0.0,
            ('DD', 'CD', 'CC'): 0.0,
            ('DD', 'CD', 'CD'): 1.0,
            ('DD', 'CD', 'DC'): 1.0,
            ('DD', 'CD', 'DD'): 0.0,
            ('DD', 'DC', 'CC'): 0.0,
            ('DD', 'DC', 'CD'): 1.0,
            ('DD', 'DC', 'DC'): 0.87463905,
            ('DD', 'DC', 'DD'): 0.0,
            ('DD', 'DD', 'CC'): 0.0,
            ('DD', 'DD', 'CD'): 1.0,
            ('DD', 'DD', 'DC'): 0.0,
            ('DD', 'DD', 'DD'): 0.0}
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_table, converted_original)

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
