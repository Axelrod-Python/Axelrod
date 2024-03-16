"""Tests for the epsilon greedy strategy."""

import axelrod as axl

from .test_player import TestPlayer, TestMatch

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

    def test_deterministic(self):
        # cases where epsilon = 0
        actions = [(C, C), (C, C), (C, C)]
        self.versus_test(axl.Cooperator(),
                         expected_actions=actions,
                         init_kwargs={"epsilon": 0, "init_c_reward": 0, "init_d_reward": -1},
                         attrs={"_rewards": {C: 3, D: -1}})

        actions = [(D, D), (D, D), (D, D)]
        self.versus_test(axl.Defector(),
                         expected_actions=actions,
                         init_kwargs={"epsilon": 0, "init_c_reward": -1, "init_d_reward": 0},
                         attrs={"_rewards": {C: -1, D: 1}})

        # actions = [(D, C), (D, D)]
        # self.versus_test(axl.TitForTat(),
        #                  expected_actions=actions,
        #                  init_kwargs={"epsilon": 0, "init_c_reward": 3.2, "init_d_reward": 4},
        #                  attrs={"_rewards": {C: 3.2, D: 9}})

    def test_random(self):
        # case where epsilon = 1
        opponent = axl.MockPlayer()
        actions = [(C, C), (D, C), (D, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions, init_kwargs={"epsilon": 1}, seed=5)


    # def versus_test(
    #     self,
    #     opponent,
    #     expected_actions,
    #     turns=None,
    #     noise=None,
    #     seed=None,
    #     match_attributes=None,
    #     attrs=None,
    #     init_kwargs=None,
    # ):
    #
    #     if init_kwargs is None:
    #         init_kwargs = dict()
    #
    #     player = self.player(**init_kwargs)
    #
    #     test_match = TestMatch()
    #     seed = test_match.search_seeds(
    #         player,
    #         opponent,
    #         [x for (x, y) in expected_actions],
    #         [y for (x, y) in expected_actions],
    #         turns=turns,
    #         noise=noise,
    #         seed=seed,
    #         attrs=attrs,
    #         match_attributes=match_attributes,
    #     )
    #     self.assertIsNotNone(seed)
    #     print(seed)
    #
