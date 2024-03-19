"""Tests for the adaptor"""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestAdaptorBrief(TestPlayer):

    name = "AdaptorBrief"
    player = axl.AdaptorBrief
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy_no_error(self):
        # No error.
        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(
            opponent=axl.AdaptorBrief(), expected_actions=actions, seed=1
        )

    def test_strategy_error_corrected(self):
        # Error corrected.
        actions = [(C, C), (C, D), (D, C), (C, C)]
        self.versus_test(
            opponent=axl.AdaptorBrief(), expected_actions=actions, seed=245
        )

    def test_strategy_error_corrected2(self):
        # Error corrected, example 2
        actions = [(D, C), (C, D), (D, C), (C, D), (C, C)]
        self.versus_test(
            opponent=axl.AdaptorBrief(), expected_actions=actions, seed=7935
        )

    def test_strategy_versus_cooperator(self):
        # Versus Cooperator
        actions = [(C, C)] * 8
        self.versus_test(
            opponent=axl.Cooperator(), expected_actions=actions, seed=1
        )

    def test_strategy_versus_defector(self):
        # Versus Defector
        actions = [(C, D), (D, D), (D, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(
            opponent=axl.Defector(), expected_actions=actions, seed=1
        )


class TestAdaptorLong(TestPlayer):

    name = "AdaptorLong"
    player = axl.AdaptorLong
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy_no_error(self):
        # No error.
        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(
            opponent=axl.AdaptorLong(), expected_actions=actions, seed=1
        )

    def test_strategy_error_corrected(self):
        # Error corrected.
        actions = [(C, C), (C, D), (D, D), (C, C), (C, C)]
        self.versus_test(
            opponent=axl.AdaptorLong(), expected_actions=actions, seed=245
        )

    def test_strategy_versus_cooperator(self):
        # Versus Cooperator
        actions = [(C, C)] * 8
        self.versus_test(
            opponent=axl.Cooperator(), expected_actions=actions, seed=1
        )

    def test_strategy_versus_defector(self):
        # Versus Defector
        actions = [(C, D), (D, D), (C, D), (D, D), (D, D), (C, D), (D, D)]
        self.versus_test(
            opponent=axl.Defector(), expected_actions=actions, seed=1
        )
