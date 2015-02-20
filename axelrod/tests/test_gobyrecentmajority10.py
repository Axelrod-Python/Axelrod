"""
Test for the go by recent majority 10 strategy
"""
import unittest
import axelrod

class TestGoByRecentMajority10(unittest.TestCase):

    def test_initial_strategy(self):
        """
        Starts by cooperating
        """
        P1 = axelrod.GoByRecentMajority10()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """
        Defect if last ten opponents moves have majority of defects
        """
        P1 = axelrod.GoByRecentMajority10()
        P2 = axelrod.Player()
        P2.history = ['D' for k in range(20)] + ['C' for k in range(10)]
        self.assertEqual(P1.strategy(P2), 'C')
        P2.history += ['D' for k in range(6)]
        self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        P1 = axelrod.GoByRecentMajority10()
        self.assertEqual(str(P1), 'Go By Recent Majority 10')
