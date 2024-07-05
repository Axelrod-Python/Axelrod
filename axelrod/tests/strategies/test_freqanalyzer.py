"""Tests for the FrequencyAnalyzer strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class Test(TestPlayer):

    name = "FrequencyAnalyzer"
    player = axl.FreqAnalyzer
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        pass