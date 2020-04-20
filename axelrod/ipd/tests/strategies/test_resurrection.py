"""Test for the Resurrection strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class Resurrection(TestPlayer):

    name = "Resurrection"
    player = axl.Resurrection
    expected_classifier = {
        "memory_depth": 5,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Check if the turns played are greater than 5
        actions = [(C, C), (C, C), (C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D), (D, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(axl.Defector(), expected_actions=actions)

        # Check for TFT behavior after 5 rounds
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(axl.Alternator(), expected_actions=actions)


class TestDoubleResurrection(TestPlayer):

    name = "DoubleResurrection"
    player = axl.DoubleResurrection
    expected_classifier = {
        "memory_depth": 5,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D)]
        self.versus_test(axl.Alternator(), expected_actions=actions)

        actions = [(C, C), (C, C), (C, C), (C, C), (C, C), (D, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D), (D, D), (D, D), (D, D), (D, D), (C, D)]
        self.versus_test(axl.Defector(), expected_actions=actions)
