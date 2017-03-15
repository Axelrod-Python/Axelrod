"""Test for the Looker Up strategy."""
import copy

import axelrod
from axelrod.strategies.lookerup import (
    create_lookup_table_keys, create_lookup_table_from_pattern)
from .test_player import TestPlayer, TestMatch

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestLookerUp(TestPlayer):

    name = "LookerUp"
    player = axelrod.LookerUp

    expected_classifier = {
        'memory_depth': 1,  # Default TFT
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    expected_class_classifier = copy.copy(expected_classifier)
    expected_class_classifier['memory_depth'] = float('inf')

    def test_create_lookup_table_keys(self):
        expected = [
            (C, C, C), (C, C, D), (C, D, C), (C, D, D),
            (D, C, C), (D, C, D), (D, D, C), (D, D, D)
        ]
        actual = create_lookup_table_keys(1, 1, 1)
        self.assertEqual(actual, expected)

    def test_create_lookup_table_from_pattern(self):
        expected = {
            (C, C, C): C,
            (C, C, D): C,
            (C, D, C): D,
            (C, D, D): C,
            (D, C, C): C,
            (D, C, D): D,
            (D, D, C): C,
            (D, D, D): C
        }
        actual = create_lookup_table_from_pattern(1, 1, 1, 'CCDCCDCC')
        self.assertEqual(actual, expected)

        with self.assertRaises(ValueError):
            create_lookup_table_from_pattern(2, 2, 2, 'CCC')

    def test_init(self):
        # Test empty table
        player = self.player(dict())
        opponent = axelrod.Cooperator()
        self.assertEqual(player.strategy(opponent), C)
        # Test default table
        player = self.player()
        expected_lookup_table = {
            ('', C, D): D,
            ('', D, D): D,
            ('', C, C): C,
            ('', D, C): C,
        }
        self.assertEqual(player.lookup_table, expected_lookup_table)
        # Test malformed tables
        table = {('', C, C): C, ('', 'DD', 'DD'): C}
        with self.assertRaises(ValueError):
            player = self.player(table)

    def test_pattern_init(self):
        # Test empty table
        pattern = "CCCC"
        parameters = (1, 1, 0)
        # Test default table
        player = self.player(lookup_pattern=pattern, parameters=parameters)
        expected_lookup_table = {
            ('', C, D): C,
            ('', D, D): C,
            ('', C, C): C,
            ('', D, C): C,
        }
        self.assertEqual(player.lookup_table, expected_lookup_table)

    def test_strategy(self):
        self.first_play_test(C)
        self.second_play_test(C, D, C, D)  # TFT
        self.responses_test([C], [C] * 4, [C, C, C, C])
        self.responses_test([D], [C] * 5, [C, C, C, C, D])

        opponent = axelrod.MockPlayer()
        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            init_kwargs={'parameters': (1, 0, 1)}
        )

        lookup_table = {
            ('', '', ''): C,
        }
        opponent = axelrod.MockPlayer()
        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            init_kwargs={'lookup_table': lookup_table})

    def test_defector_table(self):
        """
        Testing a lookup table that always defects if there is enough history.
        In order for the testing framework to be able to construct new player
        objects for the test, self.player needs to be callable with no
        arguments, thus we use a lambda expression which will call the
        constructor with the lookup table we want.
        """
        defector_table = {
            ('', C, D): D,
            ('', D, D): D,
            ('', C, C): D,
            ('', D, C): D,
        }
        self.player = lambda : axelrod.LookerUp(defector_table)
        self.responses_test([D], [C, C], [C, C])
        self.responses_test([D], [C, D], [D, C])
        self.responses_test([D], [D, D], [D, D])

    def test_zero_tables(self):
        """Test the corner case where n=0."""
        pattern = "CD"
        lookup_table_keys = create_lookup_table_keys(
            plays=0, op_plays=2, op_start_plays=0)

        lookup_table = dict(zip(lookup_table_keys, pattern))
        player = axelrod.LookerUp(lookup_table)
        self.assertEqual(player.plays, 0)
        opp = axelrod.Cooperator()
        # This shouldn't throw an exception.
        for _ in range(5):
            player.play(opp)


    def test_starting_move(self):
        """A lookup table that always repeats the opponent's first move."""

        first_move_table = {
            # If opponent starts by cooperating:
            (C, C, D): C,
            (C, D, D): C,
            (C, C, C): C,
            (C, D, C): C,
            # If opponent starts by defecting:
            (D, C, D): D,
            (D, D, D): D,
            (D, C, C): D,
            (D, D, C): D,
        }

        self.player = lambda: axelrod.LookerUp(first_move_table)

        # if the opponent started by cooperating, we should always cooperate
        self.responses_test([C], [C, C, C], [C, C, C])
        self.responses_test([C], [D, D, D], [C, C, C])
        self.responses_test([C], [C, C, C], [C, D, C])
        self.responses_test([C], [C, C, D], [C, D, C])

        # if the opponent started by defecting, we should always defect
        self.responses_test([D], [C, C, C], [D, C, C])
        self.responses_test([D], [D, D, D], [D, C, C])
        self.responses_test([D], [C, C, C], [D, D, C])
        self.responses_test([D], [C, C, D], [D, D, C])


class TestEvolvedLookerUp1_1_1(TestPlayer):

    name = "EvolvedLookerUp1_1_1"
    player = axelrod.EvolvedLookerUp1_1_1

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)


class TestEvolvedLookerUp2_2_2(TestPlayer):

    name = "EvolvedLookerUp2_2_2"
    player = axelrod.EvolvedLookerUp2_2_2

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_init(self):
        # Check for a few known keys
        known_pairs = {('DD', 'CC', 'CD'): D, ('DC', 'CD', 'CD'): C,
                       ('DD', 'CD', 'CD'): C, ('DC', 'DC', 'DC'): C,
                       ('DD', 'DD', 'CC'): D, ('CD', 'CC', 'DC'): D}
        player = self.player()
        for k, v in known_pairs.items():
            self.assertEqual(player.lookup_table[k], v)

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)


# Some heads up tests for EvolvedLookerUp
class EvolvedLookerUpvsDefector(TestMatch):
    def test_vs(self):
        self.versus_test(axelrod.EvolvedLookerUp2_2_2(), axelrod.Defector(),
                         [C, C, D], [D, D, D])


class EvolvedLookerUpvsCooperator(TestMatch):
    def test_vs(self):
        self.versus_test(axelrod.EvolvedLookerUp2_2_2(), axelrod.Cooperator(),
                         [C] * 10, [C] * 10)


class EvolvedLookerUpvsTFT(TestMatch):
    def test_vs(self):
        outcomes = zip()
        self.versus_test(axelrod.EvolvedLookerUp2_2_2(), axelrod.TitForTat(),
                         [C] * 10, [C] * 10)


class EvolvedLookerUpvsAlternator(TestMatch):
    def test_vs(self):
        self.versus_test(axelrod.EvolvedLookerUp2_2_2(), axelrod.Alternator(),
                         [C, C, C, D, D, D], [C, D, C, D, C, D])


class TestWinner12(TestPlayer):
    name = "Winner12"
    player = axelrod.Winner12

    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    expected_class_classifier = copy.copy(expected_classifier)
    expected_class_classifier['memory_depth'] = float('inf')

    def test_strategy(self):
        """Starts by cooperating twice."""
        self.responses_test([C, C])


class TestWinner21(TestPlayer):
    name = "Winner21"
    player = axelrod.Winner21

    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    expected_class_classifier = copy.copy(expected_classifier)
    expected_class_classifier['memory_depth'] = float('inf')

    def test_strategy(self):
        """Starts by cooperating twice."""
        self.responses_test([D, C])
