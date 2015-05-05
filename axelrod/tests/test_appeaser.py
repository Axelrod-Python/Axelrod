"""Test for the appeaser strategy."""

import axelrod

from test_player import TestPlayer

C, D = 'C', 'D'


class TestAppeaser(TestPlayer):

    name = "Appeaser"
    player = axelrod.Appeaser

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        P1 = axelrod.Appeaser()
        P2 = axelrod.Player()
        P1.str = 'C';
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C']
        P2.history = ['C']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'D', 'C']
        P2.history = ['C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'D')
