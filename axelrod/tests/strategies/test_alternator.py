"""Tests for the Alternator strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestAlternator(TestPlayer):

    name = "Alternator"
    player = axelrod.Alternator
    expected_classifier = {
        'memory_depth': 1,
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
        for i in range(10):
            self.responses_test([C, D] * i)
        self.responses_test([C], [C, D, C, D], [C, C, C, C])
        self.responses_test([D], [C, D, C, D, C], [C, C, C, C, C])
