"""Test for the memorytwo strategies."""

import axelrod
from axelrod.strategies.memorytwo import MEM2
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
        self.responses_test([], [], [C])
        self.responses_test([C], [C], [C])
        self.responses_test([C], [D], [D])
        # TFT if mutual cooperation on first two rounds
        self.responses_test([C, C], [C, C], [C])
        self.responses_test([C, D], [D, D], [D])
        # TFTT if C, D and D, C
        self.responses_test([C, C, C, D], [C, C, D, C], [C])
        self.responses_test([C, C, C, D, C, D], [C, C, D, C, D, D], [D])
        # TFTT if D, C and C, D
        self.responses_test([C, C, D, C], [C, D, C, D], [C])
        self.responses_test([C, C, D, C, C, D], [C, C, D, C, D, D], [D])
        # ALLD Otherwise
        self.responses_test([C, D], [D, D], [D])
        self.responses_test([C, D, D], [D, D, D], [D])
        # ALLD forever if all D twice
        self.responses_test([C, D, D, D, D, D], [D, D, D, D, D, D], [D] * 10)
        self.responses_test([C] + [D] * 5 + [C] * 4, [D] * 6 + [C] * 4, [D] * 9)
