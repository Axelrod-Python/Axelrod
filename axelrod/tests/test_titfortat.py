"""
Test for the tit for tat strategies
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

    def test_stochastic(self):
        self.assertFalse(axelrod.TitForTat().stochastic)

class TestTitFor2Tats(unittest.TestCase):

    def test_initial_strategy(self):
        """
        Starts by cooperating
        """
        P1 = axelrod.TitFor2Tats()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """
        Will defect only when last two turns of opponent were defections.
        """
        P1 = axelrod.TitFor2Tats()
        P2 = axelrod.Player()
        P1.history = ['C', 'C', 'C']
        P2.history = ['C', 'D', 'D']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['C', 'C', 'D', 'D']
        P2.history = ['D', 'D', 'D', 'C']
        self.assertEqual(P1.strategy(P2), 'C')

    def test_representation(self):
        P1 = axelrod.TitFor2Tats()
        self.assertEqual(str(P1), 'Tit For 2 Tats')

    def test_stochastic(self):
        self.assertFalse(axelrod.TitFor2Tats().stochastic)

class TestTwoTitsForTat(unittest.TestCase):

    def test_initial_strategy(self):
        """
        Starts by cooperating
        """
        P1 = axelrod.TwoTitsForTat()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """
        Will defect only when last two turns of opponent were defections.
        """
        P1 = axelrod.TwoTitsForTat()
        P2 = axelrod.Player()
        P1.history = ['C', 'C']
        P2.history = ['D', 'D']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['C', 'C', 'D']
        P2.history = ['D', 'D', 'C']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['C', 'C', 'D', 'D']
        P2.history = ['D', 'D', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')

    def test_representation(self):
        P1 = axelrod.TwoTitsForTat()
        self.assertEqual(str(P1), 'Two Tits For Tat')

    def test_stochastic(self):
        self.assertFalse(axelrod.TwoTitsForTat().stochastic)

class TestAntiTitForTat(unittest.TestCase):

    def test_initial_strategy(self):
        """Starts by defecting"""
        P1 = axelrod.AntiTitForTat()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'D')

    def test_affect_of_strategy(self):
        """Will do opposite of what opponent does."""
        P1 = axelrod.AntiTitForTat()
        P2 = axelrod.Player()
        P1.history = ['D']
        P2.history = ['C']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history.append('D')
        P2.history.append('D')
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history.append('C')
        P2.history.append('D')
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history.append('C')
        P2.history.append('C')
        self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        P1 = axelrod.AntiTitForTat()
        self.assertEqual(str(P1), "Anti Tit For Tat")

    def test_stochastic(self):
        self.assertFalse(axelrod.AntiTitForTat().stochastic)
