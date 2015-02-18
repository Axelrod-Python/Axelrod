"""
Test for the grudger strategy
"""
import unittest
import axelrod

class TestTitForTat(unittest.TestCase):

    def test_initial_strategy(self):
        """
        Starts by cooperating
        """
        P1 = axelrod.TitForTat()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """
        Repeats last action of opponent history
        """
        P1 = axelrod.TitForTat()
        P2 = axelrod.Player()
        P1.history = ['C', 'D', 'D', 'D']
        P2.history = ['C', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'D', 'D', 'D', 'C']
        P2.history = ['C', 'C', 'C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        P1 = axelrod.TitForTat()
        self.assertEqual(str(P1), 'Tit For Tat')
