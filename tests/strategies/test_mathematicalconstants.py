"""Tests for the golden and other mathematical strategies."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestGolden(TestPlayer):

    name = "$\phi$"
    player = axl.Golden
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (D, D), (C, C), (D, D), (C, C)]
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)

        actions = [(C, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        actions = [(C, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(opponent=axl.Defector(), expected_actions=actions)


class TestPi(TestPlayer):

    name = "$\pi$"
    player = axl.Pi
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (D, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)

        actions = [(C, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        actions = [(C, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(opponent=axl.Defector(), expected_actions=actions)


class Teste(TestPlayer):

    name = "$e$"
    player = axl.e
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (D, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)

        actions = [(C, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        actions = [(C, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(opponent=axl.Defector(), expected_actions=actions)
