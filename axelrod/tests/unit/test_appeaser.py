"""Tests for the appeaser strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestAppeaser(TestPlayer):

    name = "Appeaser"
    player = axelrod.Appeaser
    expected_classifier = {
        'memory_depth': float('inf'),  # Depends on internal memory.
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating.
        self.first_play_test(C)
        self.responses_test(C * 3)
        self.responses_test(D, (C + D) * 2, C + C + D)
        self.responses_test(C, (C + D) * 2 + C, C * 2 + D * 2)
        self.responses_test(D, (C + D) * 3, C * 2 + D * 3 + C)
