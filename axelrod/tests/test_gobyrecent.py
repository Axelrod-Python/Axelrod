"""
Test for the go by recent strategy
"""
import unittest
import axelrod

class TestGoByRecent(unittest.TestCase):

    def test_initial_strategy(self):
        """
        Starts by cooperating
        """
        P1 = axelrod.GoByRecentMajority10()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """
        If opponent cooperates at least as often as they defect in the last ten turns then the player cooperates
        """
        P1 = axelrod.GoByRecentMajority10()
        P2 = axelrod.Player()
        P1.history = ['D'] * 15
        P2.history = ['D'] * 10 + ['C'] * 5
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C'] * 15
        P2.history = ['C'] * 9 + ['D'] * 6
        self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        P1 = axelrod.GoByRecentMajority10()
        self.assertEqual(str(P1), 'Go By Recent Majority 10')
