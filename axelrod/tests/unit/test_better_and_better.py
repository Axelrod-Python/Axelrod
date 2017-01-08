"""Tests for the Better and Better strategy."""
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
        self.responses_test(D * 4 + C + D * 5, random_seed=6)
        self.responses_test(D * 10, random_seed=8)
