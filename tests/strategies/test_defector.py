"""Tests for the Defector strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestDefector(TestPlayer):

    name = "Defector"
    player = axl.Defector
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_state": False,
        "manipulates_source": False,
    }

    def test_strategy(self):
        # Test that always defects.
        actions = [(D, C)] + [(D, D), (D, C)] * 9
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)


class TestTrickyDefector(TestPlayer):

    name = "Tricky Defector"
    player = axl.TrickyDefector
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_cooperates_if_opponent_history_has_C_and_last_three_are_D(self):
        opponent_actions = [D, C] + [D] * 5
        actions = [(D, D), (D, C)] + [(D, D)] * 3 + [(C, D)] * 2
        self.versus_test(
            axl.MockPlayer(actions=opponent_actions), expected_actions=actions
        )

    def test_defects_if_opponent_never_cooperated(self):
        opponent_actions = [D] * 7
        actions = [(D, D)] * 7
        self.versus_test(
            axl.MockPlayer(actions=opponent_actions), expected_actions=actions
        )

    def test_defects_if_opponent_last_three_are_not_D(self):
        opponent_actions = [C] + [D] * 3 + [C, D]
        actions = [(D, C)] + [(D, D)] * 3 + [(C, C), (D, D)]
        self.versus_test(
            axl.MockPlayer(actions=opponent_actions), expected_actions=actions
        )
