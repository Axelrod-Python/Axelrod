"""Test for the average_copier strategy."""

import random

import axelrod

from test_player import TestPlayer


class TestAverageCopier(TestPlayer):

    name = "Average Copier"
    player = axelrod.AverageCopier
    stochastic = True

    def test_strategy(self):
        """Test that the first strategy is picked randomly."""
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


class TestNiceAverageCopier(TestPlayer):

    name = "Nice Average Copier"
    player = axelrod.NiceAverageCopier
    stochastic = True

    def test_strategy(self):
        """Test that the first strategy is cooperation."""
        P1 = axelrod.NiceAverageCopier()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_when_oppenent_all_Cs(self):
        """
        Tests that if opponent has played all C then player chooses C
        """
        random.seed(5)
        P1 = axelrod.NiceAverageCopier()
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
        P1 = axelrod.NiceAverageCopier()
        P2 = axelrod.Player()
        P2.history = ['D', 'D', 'D', 'D']
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')