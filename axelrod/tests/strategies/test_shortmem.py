"""Tests for the ShortMem strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestShortMem(TestPlayer):

    name = "ShortMem"
    player = axl.ShortMem
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):

        # Starts by cooperating for the first ten moves.
        actions = [(C, C)] * 10
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        actions = [(C, D)] * 10
        self.versus_test(axl.Defector(), expected_actions=actions)

        # Cooperate if in the last ten moves, Cooperations - Defections >= 3
        actions = [(C, C)] * 11 + [(C, D)] * 4
        self.versus_test(
            opponent=axl.MockPlayer(actions=[C] * 11 + [D] * 4),
            expected_actions=actions,
        )

        # Defect if in the last ten moves, Defections - Cooperations >= 3
        actions = [(C, D)] * 11 + [(D, C)] * 4
        self.versus_test(
            opponent=axl.MockPlayer(actions=[D] * 11 + [C] * 4),
            expected_actions=actions,
        )

        # If neither of the above conditions are met, apply TitForTat
        actions = (
            [(C, D)] * 5
            + [(C, C)] * 6
            + [(C, D), (D, D), (D, D), (D, C), (C, C)]
        )
        self.versus_test(
            opponent=axl.MockPlayer(
                actions=[D] * 5 + [C] * 6 + [D, D, D, C, C]
            ),
            expected_actions=actions,
        )

        actions = (
            [(C, C)] * 5
            + [(C, D)] * 6
            + [(D, C), (C, C), (C, C), (C, D), (D, D)]
        )
        self.versus_test(
            opponent=axl.MockPlayer(
                actions=[C] * 5 + [D] * 6 + [C, C, C, D, D]
            ),
            expected_actions=actions,
        )
