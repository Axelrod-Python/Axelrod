"""
Test for the Gambler strategy.
Most tests come form the LookerUp test suite
"""

import axelrod
import random
from .test_player import TestPlayer, TestHeadsUp
from axelrod import random_choice, Actions

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGambler(TestPlayer):

    name = "Gambler"
    player = axelrod.Gambler

    expected_classifier = {
        'memory_depth': 1, # Default TFT table
        'stochastic': True,
        'makes_use_of': set(['length']),
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
            ('', 'C', 'D') : 0,
            ('', 'D', 'D') : 0,
            ('', 'C', 'C') : 1,
            ('', 'D', 'C') : 1,
        }
        self.assertEqual(player.lookup_table, expected_lookup_table)
        # Test malformed tables
        table = {(C, C): 1, ('DD', 'DD'): 1}
        with self.assertRaises(ValueError):
            player = self.player(table)


    def test_strategy(self):
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
            ('', C, D) : 0,
            ('', D, D) : 0,
            ('', C, C) : 0,
            ('', D, C) : 0,
        }
        self.player = lambda : axelrod.Gambler(defector_table)
        self.responses_test([C, C], [C, C], [D])
        self.responses_test([C, D], [D, C], [D])
        self.responses_test([D, D], [D, D], [D])



class TestPSOGambler(TestPlayer):

    name = "PSO Gambler"
    player = axelrod.PSOGambler

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(['length']),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_init(self):
        # Check for a few known keys
        known_pairs = { ('CD', 'DD', 'DD'): 0.48, ('CD', 'CC', 'DD'): 0.67}
        player = self.player()
        for k, v in known_pairs.items():
            self.assertEqual(player.lookup_table[k], v)

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)
        # Defects on the last two rounds no matter what, from Backstabber test suite
        self.responses_test([C] * 197 , [C] * 197, [C, D, D],
                            tournament_length=200)

    # Test from Random test suite
    def test_return_values(self):
        self.assertEqual(random_choice(1), C)
        self.assertEqual(random_choice(0), D)
        random.seed(1)
        self.assertEqual(random_choice(), C)
        random.seed(2)
        self.assertEqual(random_choice(), D)

# Some heads up tests for PSOGambler
class PSOGamblervsDefector(TestHeadsUp):
    def test_vs(self):
        self.versus_test(axelrod.PSOGambler(), axelrod.Defector(),
                         [C, C, D, D], [D, D, D, D])


class PSOGamblervsCooperator(TestHeadsUp):
    def test_vs(self):
        self.versus_test(axelrod.PSOGambler(), axelrod.Cooperator(),
                         [C, C, D, D], [C, C, C, C])


class PSOGamblervsTFT(TestHeadsUp):
    def test_vs(self):
        outcomes = zip()
        self.versus_test(axelrod.PSOGambler(), axelrod.TitForTat(),
                         [C, C, D, D] , [C, C, C, D])


class PSOGamblervsAlternator(TestHeadsUp):
    def test_vs(self):
        self.versus_test(axelrod.PSOGambler(), axelrod.Alternator(),
                         [C, C, D, D, D, D], [C, D, C, D, C, D])
