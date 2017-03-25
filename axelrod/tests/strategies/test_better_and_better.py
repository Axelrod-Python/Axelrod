"""Tests for the BetterAndBetter strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestBetterAndBetter(TestPlayer):

    name = "Better and Better"
    player = axelrod.BetterAndBetter
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
        """Tests that the strategy gives expected behaviour."""

        self.first_play_test(D, seed=3)  # C is very unlikely
        self.first_play_test(C, seed=1514)  # first seed (starting from seed=0) that cooperates on first round
        self.versus_test(axelrod.Defector(), [(D, D), (D, D), (D, D), (D, D), (C, D), (D, D), (D, D), (D, D), (D, D)],
                         seed=6)
        self.versus_test(axelrod.Cooperator(), [(D, C), (D, C), (D, C), (D, C), (D, C), (D, C), (D, C), (D, C), (D, C)],
                         seed=8)
        actions = []
        for index in range(200):
            if index in [64, 79, 91, 99, 100, 107, 111, 119, 124, 127, 137, 141, 144, 154, 192, 196]:
                actions.append((C, D))
            else:
                actions.append((D, D))
        self.versus_test(axelrod.Defector(), expected_actions=actions, seed=8)
