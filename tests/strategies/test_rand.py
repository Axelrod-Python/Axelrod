"""Tests for the random strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestRandom(TestPlayer):

    name = "Random: 0.5"
    player = axl.Random
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_deterministic(self):
        actions = [(D, C), (D, C), (D, C)]
        self.versus_test(
            axl.Cooperator(), expected_actions=actions, init_kwargs={"p": 0}
        )

        actions = [(C, C), (C, C), (C, C)]
        self.versus_test(
            axl.Cooperator(), expected_actions=actions, init_kwargs={"p": 1}
        )

    def test_stochastic_behavior1(self):
        """Test that strategy is randomly picked (not affected by history)."""
        opponent = axl.MockPlayer()
        actions = [(C, C), (D, C), (D, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

    def test_stochastic_behavior2(self):
        opponent = axl.MockPlayer()
        actions = [(D, C), (C, C), (D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

    def test_deterministic_classification(self):
        """Test classification when p is 0 or 1"""
        for p in [0, 1]:
            player = axl.Random(p=p)
            self.assertFalse(axl.Classifiers["stochastic"](player))
