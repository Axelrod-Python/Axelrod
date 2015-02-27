"""
Test for the retaliate strategy
"""
import unittest
import axelrod

class TestRetaliate(unittest.TestCase):

    def test_initial_strategy(self):
        """
        Starts by cooperating
        """
        P1 = axelrod.Retaliate()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """
        If opponent has defected and won more than 10 percent of the times that I have, defect.
        """
        P1 = axelrod.Retaliate()
        P2 = axelrod.Player()
        P1.history = ['C', 'C', 'C', 'C']
        P2.history = ['C', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'C', 'C', 'C', 'D']
        P2.history = ['C', 'C', 'C', 'D', 'C']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['C', 'C', 'C', 'C', 'C', 'C']
        P2.history = ['C', 'C', 'C', 'C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        P1 = axelrod.Retaliate()
        self.assertEqual(str(P1), 'Retaliate')

    def test_stochastic(self):
        self.assertFalse(axelrod.Retaliate().stochastic)


class TestLimitedRetaliate(unittest.TestCase):
    def test_initial_strategy(self):
        """
        Starts by cooperating
        """
        P1 = axelrod.LimitedRetaliate()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        P1 = axelrod.LimitedRetaliate()
        P2 = axelrod.Player()
        P1.history = ['C', 'C', 'C', 'C']
        P2.history = ['C', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'C', 'C', 'C', 'D']
        P2.history = ['C', 'C', 'C', 'D', 'C']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['C', 'C', 'C', 'C', 'C', 'C']
        P2.history = ['C', 'C', 'C', 'C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        P1 = axelrod.LimitedRetaliate()
        self.assertEqual(str(P1), 'Limited Retaliate')

    def test_stochastic(self):
        self.assertFalse(axelrod.LimitedRetaliate().stochastic)
