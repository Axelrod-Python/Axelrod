"""
Test for the opposite grudger strategy
"""
import unittest
import axelrod

class TestOppositeGrudger(unittest.TestCase):

    def test_initial_strategy(self):
        """
        Starts by cooperating
        """
        P1 = axelrod.OppositeGrudger()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'D')

    def test_effect_of_strategy(self):
        """
        If opponent cooperates at any point then the player will cooperate forever
        """
        P1 = axelrod.OppositeGrudger()
        P2 = axelrod.Player()
        P1.history = ['C', 'D', 'D', 'D']
        P2.history = ['D', 'D', 'D', 'D']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['C', 'C', 'D', 'D', 'D']
        P2.history = ['C', 'D', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')

    def test_representation(self):
        P1 = axelrod.OppositeGrudger()
        self.assertEqual(str(P1), 'Opposite Grudger')
