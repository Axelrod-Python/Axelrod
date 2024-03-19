"""Tests for the SelfSteem strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestSelfSteem(TestPlayer):

    name = "SelfSteem"
    player = axl.SelfSteem
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy1(self):
        # Check for f > 0.95, defect
        actions = (
            [(C, C), (C, C), (D, C), (D, C), (C, C), (D, C)]
            + [(C, C)] * 4
            + [(D, C)]
        )
        self.versus_test(axl.Cooperator(), expected_actions=actions, seed=1)

    def test_strategy2(self):
        # Check for f < -0.95, cooperate
        actions = [
            (D, C),
            (C, C),
            (D, C),
            (D, C),
            (C, C),
            (D, C),
            (C, C),
            (C, C),
        ]
        self.versus_test(
            opponent=axl.Cooperator(), expected_actions=actions, seed=10
        )

    def test_strategy3(self):
        actions = [(D, D)] + [(D, D)] * 5 + [(D, D), (C, D), (C, D)]
        self.versus_test(
            opponent=axl.Defector(), expected_actions=actions, seed=10
        )

    def test_strategy4(self):
        # Check for -0.3 < f < 0.3, random
        actions = (
            [(D, C), (C, C), (D, C), (D, C), (C, C), (D, C)]
            + [(C, C)] * 6
            + [(D, C), (D, C)]
            + [(C, C)] * 7
        )
        self.versus_test(
            opponent=axl.Cooperator(), expected_actions=actions, seed=10
        )

    def test_strategy5(self):
        actions = (
            [(D, D)] * 7
            + [(C, D), (C, D)]
            + [(D, D)] * 8
            + [(C, D), (C, D), (D, D), (D, D), (D, D)]
        )
        self.versus_test(
            opponent=axl.Defector(), expected_actions=actions, seed=32
        )

    def test_strategy6(self):
        # Check for 0.95 > abs(f) > 0.3, follows TitForTat
        actions = (
            [(D, D)] * 5
            + [(C, D), (D, D), (C, D), (C, D), (D, D), (C, D)]
            + [(D, D)] * 5
        )
        self.versus_test(
            opponent=axl.Defector(), expected_actions=actions, seed=17
        )

    def test_strategy7(self):
        actions = [
            (D, C),
            (C, C),
            (D, C),
            (D, C),
            (C, C),
            (D, C),
            (C, C),
            (C, C),
            (C, C),
            (C, C),
        ]
        self.versus_test(
            opponent=axl.Cooperator(), expected_actions=actions, seed=10
        )
