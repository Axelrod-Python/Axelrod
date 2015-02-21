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