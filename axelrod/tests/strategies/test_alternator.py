"""Tests for the Alternator strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestAlternator(TestPlayer):

    name = "Alternator"
    player = axl.Alternator
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (D, C)] * 5
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D)] * 5
        self.versus_test(axl.Defector(), expected_actions=actions)

        opponent = axl.MockPlayer(actions=[D, C])
        actions = [(C, D), (D, C)] * 5
        self.versus_test(opponent, expected_actions=actions)
