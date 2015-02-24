"""
Test for the random strategy
"""
import unittest
import axelrod
import random

class TestRandom(unittest.TestCase):

    def test_strategy(self):
        """
        Test that strategy is randomly picked (not affected by history)
        """
        random.seed(1)
        P1 = axelrod.Random()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')
        random.seed(1)
        P1.history = ['C', 'D', 'C']
        P2.history = ['C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'C')
        random.seed(2)
        self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        P1 = axelrod.Random()
        self.assertEqual(str(P1), 'Random')

    def test_stochastic(self):
        self.assertTrue(axelrod.Random().stochastic)
