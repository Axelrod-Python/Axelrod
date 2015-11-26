"""Test for the inverse strategy."""

import random

import axelrod

from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestChampion(TestPlayer):
    name = "Champion"
    player = axelrod.Champion
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(["length"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }


    def test_strategy(self):
        # Initially cooperates
        self.first_play_test(C)
        # Cooperates for num_rounds / 20 (10 by default)
        random.seed(3)
        random_sample = []
        for i in range(10):
            random_sample.append(random.choice([C, D]))
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

        self.responses_test(my_responses + [C], random_sample + [D], [C],
                            random_seed=50)
        self.responses_test(my_responses + [C], random_sample + [D], [C],
                            random_seed=30)
        self.responses_test(my_responses + [C] * 40, random_sample + [D] * 40,
                            [D], random_seed=40)


class TestEatherley(TestPlayer):

    name = "Eatherley"
    player = axelrod.Eatherley
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

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
        self.responses_test([D, C, C, D], [D, C, C, D], [D, C], random_seed=8)


class TestTester(TestPlayer):

    name = "Tester"
    player = axelrod.Tester
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by defecting."""
        self.first_play_test(D)

    def test_effect_of_strategy(self):

        # Test Alternating CD
        self.responses_test([D], [C], [C])
        self.responses_test([D, C], [C, C], [C])
        self.responses_test([D, C, C], [C, C, C], [D])
        self.responses_test([D, C, C, D], [C, C, C, C], [C])
        self.responses_test([D, C, C, D, C], [C, C, C, C, C], [D])

        # Test cooperation after opponent defection
        self.responses_test([D, C], [D, C], [C])

        # Test TFT after defection
        self.responses_test([D, C, C], [D, C, C], [C])
        self.responses_test([D, C, C, C], [D, C, C, C], [C])
        self.responses_test([D, C, D], [D, D, D], [D])
        self.responses_test([D, C, C], [D, C, D], [D])
