"""Tests for the SelfSteem strategy."""

import axelrod
import random
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D

class TestSelfSteem(TestPlayer):

    name = "SelfSteem"
    player = axelrod.SelfSteem
    expected_classifier = {
        'memory_depth': float("inf"),
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Check for f > 0.95
        self.responses_test([D], [C] * 2 , [C] * 2)
        self.responses_test([D], [C] * 13, [C] * 13)

        # Check for f < -0.95
        self.responses_test([C], [C] * 7, [C] * 7)
        self.responses_test([C], [C] * 18, [D] * 18)

        # Check for -0.3 < f < 0.3
        self.responses_test([C], [C] * 20, [C] * 20, seed=6)
        self.responses_test([D], [C] * 20, [D] * 20, seed=5)

        # Check for 0.95 > abs(f) > 0.3
        self.responses_test([C], [C], [C])
        self.responses_test([D], [C] * 16, [D] * 16)
        self.responses_test([C], [D] * 9, [C] * 9)
