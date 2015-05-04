"""Test for the random strategy."""

import random

import axelrod

from test_player import TestPlayer, C, D


class TestRandom(TestPlayer):

    name = "Random"
    player = axelrod.Random
    stochastic = True

    def test_strategy(self):
        """Test that strategy is randomly picked (not affected by history)."""
        self.first_play_test(C, random_seed=1)
        self.first_play_test(D, random_seed=2)
        self.responses_test([C, D, C], [C, C, D], [C], random_seed=1)
