"""Tests for the random strategy."""

import axelrod
from axelrod.classifier import Classifiers
from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D


class TestRandom(TestPlayer):

    name = "Random: 0.5"
    player = axelrod.Random
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        """Test that strategy is randomly picked (not affected by history)."""
        opponent = axelrod.MockPlayer()
        actions = [(C, C), (D, C), (D, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        opponent = axelrod.MockPlayer()
        actions = [(D, C), (D, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        opponent = axelrod.MockPlayer()
        actions = [(D, C), (D, C), (D, C)]
        self.versus_test(opponent, expected_actions=actions, init_kwargs={"p": 0})

        opponent = axelrod.MockPlayer()
        actions = [(C, C), (C, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions, init_kwargs={"p": 1})

    def test_deterministic_classification(self):
        """Test classification when p is 0 or 1"""
        for p in [0, 1]:
            player = axelrod.Random(p=p)
            self.assertFalse(Classifiers().get("stochastic", player))
