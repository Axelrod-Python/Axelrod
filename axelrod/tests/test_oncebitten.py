"""
Test for the once bitten strategy
"""
import unittest
import axelrod

class TestOnceBitten(unittest.TestCase):

    def test_initial_strategy(self):
        """
        Starts by cooperating
        """
        P1 = axelrod.OnceBitten()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """
        If opponent defects at any point then the player will defect forever
        """
        P1 = axelrod.OnceBitten()
        P2 = axelrod.Player()
        P1.history = ['C', 'D', 'D', 'D']
        P2.history = ['C', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'C', 'D', 'D', 'D']
        P2.history = ['C', 'D', 'C', 'D', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        P2.history = ['C', 'D', 'C', 'D', 'D']
        self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        P1 = axelrod.OnceBitten()
        self.assertEqual(str(P1), 'Once Bitten')

    def test_stochastic(self):
        self.assertFalse(axelrod.OnceBitten().stochastic)
