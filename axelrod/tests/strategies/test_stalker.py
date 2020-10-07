"""Tests for the Stalker strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestStalker(TestPlayer):

    name = "Stalker: (D,)"
    player = axl.Stalker
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": {"game", "length"},
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C)] * 3 + [(D, C)]
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        # wish_score < current_average_score < very_good_score
        actions = [(C, C)] * 7 + [(C, D), (C, D), (C, C), (C, C), (D, C)]
        self.versus_test(
            opponent=axl.MockPlayer(actions=[C] * 7 + [D] * 2),
            expected_actions=actions,
        )

        actions = [(C, C)] * 7 + [(C, D), (C, C), (D, C)]
        self.versus_test(
            opponent=axl.MockPlayer(actions=[C] * 7 + [D]),
            expected_actions=actions,
        )

        # current_average_score > 2
        actions = [(C, C)] * 9 + [(D, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        # 1 < current_average_score < 2
        actions = [(C, C)] * 7 + [(C, D)] * 4 + [(D, D)]
        self.versus_test(
            opponent=axl.MockPlayer(actions=[C] * 7 + [D] * 5),
            expected_actions=actions,
        )

    def test_strategy2(self):
        # current_average_score < 1
        actions = (
            [(C, D)]
            + [(D, D)] * 2
            + [(C, D)] * 3
            + [(D, D), (C, D), (D, D), (C, D), (D, D), (C, D), (D, D)]
        )
        self.versus_test(axl.Defector(), expected_actions=actions, seed=3222)

    def test_strategy3(self):
        actions = [(C, D)] * 3 + [
            (D, D),
            (C, D),
            (D, D),
            (C, D),
            (C, D),
            (D, D),
            (C, D),
            (C, D),
            (C, D),
            (D, D),
        ]
        self.versus_test(axl.Defector(), expected_actions=actions, seed=649)

    def test_strategy4(self):
        # defect in last round
        actions = [(C, C)] * 199 + [(D, C)]
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            match_attributes={"length": 200},
        )

        # Force a defection before the end of the actual match which ensures
        # that current_average_score > very_good_score
        actions = [(C, C)] * 3 + [(D, C)] * 3
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            match_attributes={"length": 4},
        )
