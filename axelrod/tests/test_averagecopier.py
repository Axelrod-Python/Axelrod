"""
Test for the average_copier strategy
"""
import unittest
import axelrod
import random

class TestAverageCopier(unittest.TestCase):

    def test_initial_strategy(self):
        """
        Test that the first strategy is picked randomly
        """
        random.seed(1)
        P1 = axelrod.AverageCopier()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')

    def test_when_oppenent_all_Cs(self):
        """
        Tests that if opponent has played all C then player chooses C
        """
        random.seed(5)
        P1 = axelrod.AverageCopier()
        P2 = axelrod.Player()
        P2.history = ['C', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')

    def test_when_opponent_all_Ds(self):
        """
        Tests that if opponent has played all D then player chooses D
        """
        random.seed(5)
        P1 = axelrod.AverageCopier()
        P2 = axelrod.Player()
        P2.history = ['D', 'D', 'D', 'D']
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        P1 = axelrod.AverageCopier()
        self.assertEqual(str(P1), 'Average Copier')
