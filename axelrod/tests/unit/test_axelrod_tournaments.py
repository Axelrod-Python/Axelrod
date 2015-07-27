"""Test for the inverse strategy."""

import random

import axelrod

from test_player import TestPlayer

C, D = 'C', 'D'


class TestEatherly(TestPlayer):

    name = "Eatherley"
    player = axelrod.Eatherley
    stochastic = True

    def test_strategy(self):
        # Initially cooperates
        self.first_play_test(C)
        # Test cooperate after opponent cooperates
        self.responses_test([C], [C], [C])
        self.responses_test([C, C], [C, C], [C])
        self.responses_test([D, C], [D, C], [C])
        self.responses_test([D, C, C], [D, C, C], [C])
        # Test defection after opponent defection
        self.responses_test([D], [D], [D])
        self.responses_test([D, D], [D, D], [D])
        self.responses_test([D, C, C, D], [D, C, C, D], [D, C], random_seed=10)


class TestChampion(TestPlayer):
    name = "Champion"
    player = axelrod.Champion
    stochastic = True

    def test_strategy(self):
        # Initially cooperates
        self.first_play_test(C)
        # Cooperates for num_rounds / 20 (10 by default)
        random_sample = []
        for i in range(10):
            random_sample.append(random.choice([C,D]))
            self.responses_test([C] * i, random_sample, [C])

        # Mirror opponent in the next stage (15 rounds by default)
        my_responses = [C] * 10
        for i in range(15):
            self.responses_test(my_responses, random_sample,
                                [random_sample[-1]])
            my_responses.append(random_sample[-1])
            random_sample.append(random.choice([C,D]))

        # Cooperate unless the opponent defected, has defected at least 40% of
        # the time, and with a random choice
        for i in range(5):
            my_responses.append(C)
            random_sample.append(C)
            self.responses_test(my_responses, random_sample, [C])

        self.responses_test(my_responses + [C], random_sample + [D], [C], random_seed=50)
        self.responses_test(my_responses + [C] * 40, random_sample + [D] * 40,
                            [D], random_seed=40)
