"""
Test for the cooperator strategy
"""
import unittest
import axelrod

class TestCooperator(unittest.TestCase):

    def test_strategy(self):
        """
        Test that always cooperates
        """
        P1 = axelrod.Cooperator()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'D', 'C']
        P2.history = ['C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'C')

    def test_representation(self):
        P1 = axelrod.Cooperator()
        self.assertEqual(str(P1), 'Cooperator')

