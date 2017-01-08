"""Tests for calculator strategies."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestCalculator(TestPlayer):

    name = "Calculator"
    player = axelrod.Calculator
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
        self.first_play_test(C)
        # Test cycle detection
        self.responses_test(D, C * 20, (C + D) * 10)
        # Test non-cycle response
        history = C * 2 + D + C * 2 + D + C * 3 + D + C * 4 + D + C * 5
        self.responses_test(C, C * 20, history)
        # Test post 20 rounds responses
        self.responses_test(D, C * 21, C * 21)
        history = C * 2 + D + C * 2 + D + C * 3 + D + C * 4 + D + C * 5 + D
        self.responses_test(D, C * 21, history)
        history += C
        self.responses_test(C, C * 22, history)
