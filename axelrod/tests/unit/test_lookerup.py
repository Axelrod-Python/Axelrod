"""Test for the Looker Up strategy."""

import axelrod
from .test_player import TestPlayer, TestHeadsUp

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestLookerUp(TestPlayer):

    name = "LookerUp"
    player = axelrod.LookerUp

    expected_classifier = {
        'memory_depth': 1, # Default TFT table
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_init(self):
        # Test empty table
        player = self.player(dict())
        opponent = axelrod.Cooperator()
        self.assertEqual(player.strategy(opponent), C)
        # Test default table
        player = self.player()
        expected_lookup_table = {
            ('', 'C', 'D') : D,
            ('', 'D', 'D') : D,
            ('', 'C', 'C') : C,
            ('', 'D', 'C') : C,
        }
        self.assertEqual(player.lookup_table, expected_lookup_table)
        # Test malformed tables
        table = {(C, C): C, ('DD', 'DD'): C}
        with self.assertRaises(ValueError):
            player = self.player(table)
        table = {(C, C): C, (C, D): 'CD'}
        with self.assertRaises(ValueError):
            player = self.player(table)

    def test_strategy(self):
        self.markov_test([C, D, C, D]) # TFT
        self.responses_test([C] * 4, [C, C, C, C], [C])
        self.responses_test([C] * 5, [C, C, C, C, D], [D])

    def test_defector_table(self):
        """
        Testing a lookup table that always defects if there is enough history.
        In order for the testing framework to be able to construct new player
        objects for the test, self.player needs to be callable with no
        arguments, thus we use a lambda expression which will call the
        constructor with the lookup table we want.
        """
        defector_table = {
            ('', C, D) : D,
            ('', D, D) : D,
            ('', C, C) : D,
            ('', D, C) : D,
        }
        self.player = lambda : axelrod.LookerUp(defector_table)
        self.responses_test([C, C], [C, C], [D])
        self.responses_test([C, D], [D, C], [D])
        self.responses_test([D, D], [D, D], [D])

    def test_starting_move(self):
        """A lookup table that always repeats the opponent's first move."""

        first_move_table = {
            # If oppponent starts by cooperating:
            (C, C, D) : C,
            (C, D, D) : C,
            (C, C, C) : C,
            (C, D, C) : C,
            # If opponent starts by defecting:
            (D, C, D) : D,
            (D, D, D) : D,
            (D, C, C) : D,
            (D, D, C) : D,
        }

        self.player = lambda : axelrod.LookerUp(first_move_table)

        # if the opponent started by cooperating, we should always cooperate
        self.responses_test([C, C, C], [C, C, C], [C])
        self.responses_test([D, D, D], [C, C, C], [C])
        self.responses_test([C, C, C], [C, D, C], [C])
        self.responses_test([C, C, D], [C, D, C], [C])

        # if the opponent started by defecting, we should always defect
        self.responses_test([C, C, C], [D, C, C], [D])
        self.responses_test([D, D, D], [D, C, C], [D])
        self.responses_test([C, C, C], [D, D, C], [D])
        self.responses_test([C, C, D], [D, D, C], [D])


class TestEvolvedLookerUp(TestPlayer):

    name = "EvolvedLookerUp"
    player = axelrod.EvolvedLookerUp

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_init(self):
        # Check for a few known keys
        known_pairs = {('DD', 'CC', 'CD'): 'D', ('DC', 'CD', 'CD'): 'C',
                        ('DD', 'CD', 'CD'): 'D', ('DC', 'DC', 'DC'): 'C',
                        ('DD', 'DD', 'CC'): 'D', ('CD', 'CC', 'DC'): 'C'}
        player = self.player()
        for k, v in known_pairs.items():
            self.assertEqual(player.lookup_table[k], v)

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)


# Some heads up tests for EvolvedLookerUp
class EvolvedLookerUpvsDefector(TestHeadsUp):
    def test_vs(self):
        self.versus_test(axelrod.EvolvedLookerUp(), axelrod.Defector(),
                         [C, C, D], [D, D, D])


class EvolvedLookerUpvsCooperator(TestHeadsUp):
    def test_vs(self):
        self.versus_test(axelrod.EvolvedLookerUp(), axelrod.Cooperator(),
                         [C] * 10, [C] * 10)


class EvolvedLookerUpvsTFT(TestHeadsUp):
    def test_vs(self):
        outcomes = zip()
        self.versus_test(axelrod.EvolvedLookerUp(), axelrod.TitForTat(),
                         [C] * 10, [C] * 10)


class EvolvedLookerUpvsAlternator(TestHeadsUp):
    def test_vs(self):
        self.versus_test(axelrod.EvolvedLookerUp(), axelrod.Alternator(),
                         [C, C, D, D, D, D], [C, D, C, D, C, D])
