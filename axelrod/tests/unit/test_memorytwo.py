"""Tests for the memorytwo strategies."""

import axelrod
from .test_player import TestPlayer


C, D = axelrod.Actions.C, axelrod.Actions.D


class TestMEM2(TestPlayer):

    name = "MEM2"
    player = axelrod.MEM2
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
        # Start with TFT
        self.responses_test(C)
        self.responses_test(C, C, C)
        self.responses_test(D, C, D)
        # TFT if mutual cooperation on first two rounds
        self.responses_test(C, C * 2, C * 2)
        self.responses_test(D, C + D, D * 2)
        # TFTT if C, D and D, C
        self.responses_test(C, C * 3 + D, C + C + D + C)
        self.responses_test(D, C * 3 + D + C + D, C + C + D + C + D + D)
        # TFTT if D, C and C, D
        self.responses_test(C, C + C + D + C, C + D + C + D)
        self.responses_test(D, C + C + D + C + C + D, C + C + D + C + D + D)
        # ALLD Otherwise
        self.responses_test(D, C + D, D * 2)
        self.responses_test(D, C + D + D, D * 3)
        # ALLD forever if all D twice
        self.responses_test(D * 10, C + D * 5, D * 6)
        self.responses_test(D * 9, C + D * 5 + C * 4, D * 6 + C * 4)
