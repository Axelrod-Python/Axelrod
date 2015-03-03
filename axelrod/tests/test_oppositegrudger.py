"""Test for the opposite grudger strategy."""

import axelrod

from test_player import TestPlayer


class TestOppositeGrudger(TestPlayer):

    name = 'Opposite Grudger'
    player = axelrod.OppositeGrudger
    stochastic = False

    def test_initial_strategy(self):
        """
        Starts by cooperating
        """
        P1 = axelrod.OppositeGrudger()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'D')

    def test_strategy(self):
        """
        If opponent cooperates at any point then the player will cooperate forever
        """
        P1 = axelrod.OppositeGrudger()
        P2 = axelrod.Player()
        P1.history = ['C', 'D', 'D', 'D']
        P2.history = ['D', 'D', 'D', 'D']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['C', 'C', 'D', 'D', 'D']
        P2.history = ['C', 'D', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
