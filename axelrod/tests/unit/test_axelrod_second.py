"""Tests for the Axelrod second tournament strategies."""

import random

import axelrod
from axelrod import History
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestChampion(TestPlayer):
    name = "Champion"
    player = axelrod.Champion
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(["length"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Initially cooperates
        self.first_play_test(C)
        # Cooperates for num_rounds / 20 (10 by default)
        random.seed(3)
        random_sample = History()
        for i in range(10):
            random_sample.append(random.choice([C, D]))
            self.responses_test(C, C * i, random_sample)

        # Mirror opponent in the next stage (15 rounds by default)
        my_responses = History(C * 10)
        for i in range(15):
            self.responses_test(random_sample[-1], my_responses, random_sample)
            my_responses.append(random_sample[-1])
            random_sample.append(random.choice([C, D]))

        # Cooperate unless the opponent defected, has defected at least 40% of
        # the time, and with a random choice
        for i in range(5):
            my_responses.append(C)
            random_sample.append(C)
            self.responses_test(C, my_responses, random_sample)

        self.responses_test(C, my_responses + C, random_sample + D,
                            random_seed=1)
        self.responses_test(D, my_responses + C, random_sample + D,
                            random_seed=50)
        self.responses_test(D, my_responses + C, random_sample + D,
                            random_seed=30)
        self.responses_test(D, my_responses + C * 40, random_sample + D * 40,
                            random_seed=50)


class TestEatherley(TestPlayer):

    name = "Eatherley"
    player = axelrod.Eatherley
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Initially cooperates
        self.first_play_test(C)
        # Test cooperate after opponent cooperates
        self.responses_test(C, C, C)
        self.responses_test(C, C * 2, C * 2)
        self.responses_test(C, D + C, D + C)
        self.responses_test(C, D + C + C, D + C + C)
        # Test defection after opponent defection
        self.responses_test(D, D, D)
        self.responses_test(D, D + D, D + D)
        self.responses_test(C + C, D + C + C + D, D + C + C + D, random_seed=8)


class TestTester(TestPlayer):

    name = "Tester"
    player = axelrod.Tester
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by defecting."""
        self.first_play_test(D)

    def test_effect_of_strategy(self):

        # Test Alternating CD
        self.responses_test(C, D, C)
        self.responses_test(C, D + C, C + C)
        self.responses_test(D, D + C + C, C * 3)
        self.responses_test(C, D + C + C + D, C * 4)
        self.responses_test(D, D + C + C + D + C, C * 5)

        # Test cooperation after opponent defection
        self.responses_test(C, D + C, D + C)

        # Test TFT after defection
        self.responses_test(C, D + C + C, D + C + C)
        self.responses_test(C, D + C * 3, D + C * 3)
        self.responses_test(D, D + C + D, D * 3)
        self.responses_test(D, D + C + C, D + C + D)
