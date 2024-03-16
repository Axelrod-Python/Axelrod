"""Tests for the epsilon greedy strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestEpsilonGreedy(TestPlayer):

    name = "$\varepsilon$-greedy"
    player = axl.EpsilonGreedy
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": {"game"},
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_random(self):
        """Test that strategy is randomly picked (not affected by history)."""
        opponent = axl.MockPlayer()
        actions = [(C, C), (C, D), (C, D), (C, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions, seed=0, init_kwargs={"epsilon": 1})
