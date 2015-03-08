"""Test for the memoryone strategies."""

import axelrod

from test_player import TestPlayer


class TestWinStayLostShift(TestPlayer):

    name = "Win-Stay Lose-Shift"
    player = axelrod.WinStayLoseShift

    def test_strategy(self):
        """Starts by cooperating"""
        P1 = self.player()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """Check that switches if does not get best payoff."""
        P1 = self.player()
        P2 = axelrod.Player()
        P1.history = ['C']
        P2.history = ['C']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C']
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['D']
        P2.history = ['C']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['D']
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'C')
