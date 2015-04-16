"""Test for the inverse strategy."""

import random

import axelrod

from test_player import TestPlayer


class TestInverse(TestPlayer):

    name = "Inverse"
    player = axelrod.Inverse
    stochastic = True

    def test_strategy(self):
        """
        Test that initial strategy cooperates.
        """
        P1 = axelrod.Inverse()
        P2 = axelrod.Player()
        P2.history = []
        self.assertEqual(P1.strategy(P2), 'C')

    def test_that_cooperate_if_opponent_has_not_defected(self):
        """
        Test that as long as the opponent has not defected the player will cooperate.
        """
        P1 = axelrod.Inverse()
        P2 = axelrod.Player()
        P2.history = ['C', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        P2.history.append('C')
        self.assertEqual(P1.strategy(P2), 'C')

    def test_when_opponent_has_all_Ds(self):
        """
        Tests that if opponent has played all D then player chooses D
        """
        random.seed(5)
        P1 = axelrod.Inverse()
        P2 = axelrod.Player()
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'D')
        P2.history = ['D', 'D']
        self.assertEqual(P1.strategy(P2), 'D')
        P2.history = ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D']
        self.assertEqual(P1.strategy(P2), 'D')

    def test_when_opponent_som_Ds(self):
        """
        Tests that if opponent has played all D then player chooses D
        """
        random.seed(5)
        P1 = axelrod.Inverse()
        P2 = axelrod.Player()
        P2.history = ['C', 'D', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'C')
        P2.history = ['C', 'C', 'C', 'C', 'D', 'D']
        self.assertEqual(P1.strategy(P2), 'C')
        P2.history = ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C']
        self.assertEqual(P1.strategy(P2), 'D')
        random.seed(5)
        self.assertEqual(P1.strategy(P2), 'D')
