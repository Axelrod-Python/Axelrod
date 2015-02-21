"""
Test for the appeaser strategy
"""
import unittest
import axelrod

class TestAppeaser(unittest.TestCase):

    def test_strategy(self):
        P1 = axelrod.Appeaser()
        P2 = axelrod.Player()
	P1.str = 'C';
        self.assertEqual(P1.strategy(P2), 'C')
	P1.history = ['C']
	P1.history = ['C']
	self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'D', 'C']
        P2.history = ['C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        P1 = axelrod.Appeaser()
        self.assertEqual(str(P1), 'Appeaser')
