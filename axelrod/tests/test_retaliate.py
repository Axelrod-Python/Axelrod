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
        If opponent has defected more than 10 percent of the time, defect.
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
        """If opponent has never defected, co-operate"""
        P1 = axelrod.LimitedRetaliate()
        P2 = axelrod.Player()
        P1.history = ['C', 'C', 'C', 'C']
        P2.history = ['C', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertFalse(P1.retaliating)

        """If opponent has previously defected and won, defect and be retaliating"""
        P1.history = ['C', 'C', 'C', 'C', 'D']
        P2.history = ['C', 'C', 'C', 'D', 'C']
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertTrue(P1.retaliating)

        """If opponent has just defected and won, defect and be retaliating"""
        P1.history = ['C', 'C', 'C', 'C', 'C', 'C']
        P2.history = ['C', 'C', 'C', 'C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertTrue(P1.retaliating)

        """If I've hit the limit for retaliation attempts, co-operate"""
        P1.history = ['C', 'C', 'C', 'C', 'D']
        P2.history = ['C', 'C', 'C', 'D', 'C']
        P1.retaliation_count = 20
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertFalse(P1.retaliating)

    def test_reset(self):
        P1 = axelrod.LimitedRetaliate()
        P1.history = ['C', 'C', 'C', 'C', 'D']
        P1.retaliating = True
        P1.retaliation_count = 4
        P1.reset()
        self.assertEqual(P1.history, [])
        self.assertFalse(P1.retaliating)
        self.assertEqual(P1.retaliation_count, 0)

    def test_representation(self):
        P1 = axelrod.LimitedRetaliate()
        self.assertEqual(str(P1), 'Limited Retaliate (0.1/20)')

    def test_stochastic(self):
        self.assertFalse(axelrod.LimitedRetaliate().stochastic)


class TestRandomLimitedRetaliate(unittest.TestCase):
        def test_stochastic(self):
            self.assertTrue(axelrod.RandomLimitedRetaliate().stochastic)
