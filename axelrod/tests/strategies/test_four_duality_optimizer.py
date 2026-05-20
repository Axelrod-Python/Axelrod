"""Tests for the FourDualityOptimizer strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestFourDualityOptimizer1(TestPlayer):

    name = "4-Duality Optimizer 1"
    player = axl.FourDualityOptimizer1
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):

        actions = [(C, C), (C, C)] + [(C, C)] * 20
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        actions = [(C, C), (C, C)] + [(C, C)] * 20
        self.versus_test(axl.TitForTat(), expected_actions=actions)

        actions = [(C, C), (C, C)] + [(C, C)] * 20
        self.versus_test(axl.Retaliate(), expected_actions=actions)

        actions = [(C, D), (C, D)] + [(D, D)]
        self.versus_test(axl.Defector(), expected_actions=actions)


