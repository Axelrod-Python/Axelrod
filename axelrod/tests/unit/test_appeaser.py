"""Tests for the Appeaser strategy."""

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
        self.responses_test([C, C, C], [C], [C])
        self.responses_test([D], [C, D, C, D], [C, C, D])
        self.responses_test([C], [C, D, C, D, C], [C, C, D, D])
        self.responses_test([D], [C, D, C, D, C, D], [C, C, D, D, D])

