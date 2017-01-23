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
        self.first_play_test(D, seed=3)  # D is very unlikely
        self.responses_test([D, D, D, D, C, D, D, D, D, D], seed=6)
        self.responses_test([D, D, D, D, D, D, D, D, D, D], seed=8)
