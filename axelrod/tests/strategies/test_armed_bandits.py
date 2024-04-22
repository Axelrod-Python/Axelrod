"""Tests for the armed bandits strategies."""

import axelrod as axl

from .test_player import TestPlayer, TestMatch

C, D = axl.Action.C, axl.Action.D


class TestEpsilonGreedy(TestPlayer):

    name = "$\varepsilon$-greedy: 0.1, 0.0, 0.0, inf"
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

    def test_deterministic(self):
        # cases where epsilon = 0
        actions = [(C, C), (C, C), (C, C)]
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            init_kwargs={"epsilon": 0, "init_c_reward": 0, "init_d_reward": -1},
            attrs={"_rewards": {C: 3, D: -1}},
        )

        actions = [(D, D), (D, D), (D, D)]
        self.versus_test(
            axl.Defector(),
            expected_actions=actions,
            init_kwargs={"epsilon": 0, "init_c_reward": -1, "init_d_reward": 0},
            attrs={"_rewards": {C: -1, D: 1}},
        )

        actions = [(D, C), (D, D), (C, D)]
        self.versus_test(
            axl.TitForTat(),
            expected_actions=actions,
            init_kwargs={"epsilon": 0, "init_c_reward": 3.2, "init_d_reward": 4.0},
            attrs={"_rewards": {C: 3.2, D: 3.0}},
        )

    def test_random(self):
        # cases where epsilon = 1
        opponent = axl.MockPlayer()
        actions = [(C, C), (D, C), (D, C), (C, C)]
        self.versus_test(
            opponent, expected_actions=actions, init_kwargs={"epsilon": 1}, seed=5
        )

        opponent = axl.MockPlayer(actions=[C, D, C])
        actions = [(D, C), (C, D), (C, C)]
        self.versus_test(
            opponent, expected_actions=actions, init_kwargs={"epsilon": 1.0}, seed=1
        )

    def test_strategy(self):
        # sometimes explores
        actions = [(C, C), (D, C), (D, C)]
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            init_kwargs={"epsilon": 0.5},
            attrs={"_rewards": {C: 3, D: 5}},
            seed=2,
        )

        # always explores
        actions = [(D, D), (C, D), (C, D)]
        self.versus_test(
            axl.Defector(),
            expected_actions=actions,
            attrs={"_rewards": {C: 0, D: 1}},
            seed=13741,
        )

        # never explores/always exploits
        actions = [(C, C), (C, C), (C, C)]
        self.versus_test(
            axl.TitForTat(),
            expected_actions=actions,
            attrs={"_rewards": {C: 3, D: 0}},
            seed=1,
        )
