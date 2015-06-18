"""Test for the random strategy."""

import random

import axelrod

from test_player import TestPlayer

C, D = 'C', 'D'


class TestRandom(TestPlayer):

    name = "Random"
    player = axelrod.Random
    stochastic = True

    def test_strategy(self):
        """Test that strategy is randomly picked (not affected by history)."""
        self.first_play_test(C, random_seed=1)
        self.first_play_test(D, random_seed=2)
        self.responses_test([C, D, C], [C, C, D], [C], random_seed=1)


class TestTullock(TestPlayer):

    name = "Tullock"
    player = axelrod.Tullock
    stochastic = True

    def test_strategy(self):
        """Cooperates for first ten rounds"""
        self.first_play_test(C)
        for i in range(10):
            history_1 = [C]*i
            history_2 = [C]*i
            self.responses_test(history_1, history_2, [C])
        # Now cooperate 10% less than opponent
        history_1 = [C]*11
        history_2 = [D]*11
        self.responses_test(history_1, history_2, [D], random_seed=10)
        history_1 = [C]*11
        history_2 = [D]*10 + [C]
        self.responses_test(history_1, history_2, [D], random_seed=10)

        history_1 = [C]*11
        history_2 = [D]*5 + [C]*6
        self.responses_test(history_1, history_2, [D, D, D, D],
                            random_seed=20)

        history_1 = [C]*11
        history_2 = [C]*9 + [D]*2
        self.responses_test(history_1, history_2, [C, D, D, C],
                            random_seed=25)

