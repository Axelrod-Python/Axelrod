"""Tests for the Doubler strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestDoubler(TestPlayer):

    name = "Doubler"
    player = axl.Doubler
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_defects_if_opponent_last_play_is_D_and_defections_gt_two_times_cooperations(
        self,
    ):
        opponent_plays = [C] * 7 + [D] * 4 + [C]
        actions = [(C, C)] * 7 + [(C, D)] * 4 + [(D, C)]
        self.versus_test(
            axl.MockPlayer(actions=opponent_plays), expected_actions=actions
        )

    def test_defects_if_opponent_last_play_D_and_defections_equal_two_times_cooperations(
        self,
    ):
        opponent_plays = [C] * 8 + [D] * 4 + [C]
        actions = [(C, C)] * 8 + [(C, D)] * 4 + [(D, C)]
        self.versus_test(
            axl.MockPlayer(actions=opponent_plays), expected_actions=actions
        )

    def test_cooperates_if_opponent_last_play_is_C(self):
        opponent_first_five = [D] * 5
        actions_first_five = [(C, D)] + [(D, D)] * 4
        opponent_plays = opponent_first_five + [C] + [D]
        actions = actions_first_five + [(D, C)] + [(C, D)]
        self.versus_test(
            axl.MockPlayer(actions=opponent_plays), expected_actions=actions
        )
