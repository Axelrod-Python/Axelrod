"""Test for the random strategy."""

import random

import axelrod

from test_player import TestPlayer


class TestRandom(TestPlayer):

    name = "Random"
    player = axelrod.Random
    stochastic = True

    def test_strategy(self):
        """Test that strategy is randomly picked (not affected by history)."""
        random.seed(1)
        P1 = axelrod.Random()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')
        random.seed(1)
        P1.history = ['C', 'D', 'C']
        P2.history = ['C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'C')
        random.seed(2)
        self.assertEqual(P1.strategy(P2), 'D')
