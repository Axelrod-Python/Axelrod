"""Test for the grudger strategy."""

import axelrod

from test_player import TestPlayer


class TestGrudger(TestPlayer):

    name = "Grudger"
    player = axelrod.Grudger
    stochastic = False

    def test_initial_strategy(self):
        """
        Starts by cooperating
        """
        P1 = axelrod.Grudger()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_strategy(self):
        """
        If opponent defects at any point then the player will defect forever
        """
        P1 = axelrod.Grudger()
        P2 = axelrod.Player()
        P1.history = ['C', 'D', 'D', 'D']
        P2.history = ['C', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'C', 'D', 'D', 'D']
        P2.history = ['C', 'D', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'D')
