"""
Test for the defector strategy
"""
import unittest
import axelrod

class TestDefector(unittest.TestCase):

    def test_strategy(self):
        """
        Test that always defects
        """
        P1 = axelrod.Defector()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['C', 'D', 'C']
        P2.history = ['C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        P1 = axelrod.Defector()
        self.assertEqual(str(P1), 'Defector')
