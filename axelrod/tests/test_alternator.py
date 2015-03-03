"""Test for the alternator strategy."""

import axelrod

from test_player import TestPlayer


class TestAlternator(TestPlayer):

    name = "Alternator"
    player = axelrod.Alternator

    def test_strategy(self):
        """Starts by cooperating."""
        P1 = axelrod.Alternator()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """Simply does the opposite to what the strategy did last time."""
        P1 = axelrod.Alternator()
        P2 = axelrod.Player()
        P1.history = ['C', 'D', 'D', 'D']
        P2.history = ['C', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'C', 'D', 'D', 'C']
        P2.history = ['C', 'D', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'D')
