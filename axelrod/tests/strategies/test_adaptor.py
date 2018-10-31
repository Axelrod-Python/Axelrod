"""Tests for the adaptor"""

import unittest

import axelrod
from axelrod import Game

from .test_player import TestPlayer, test_four_vector

C, D = axelrod.Action.C, axelrod.Action.D


class TestAdaptorBrief(TestPlayer):

    name = "AdaptorBrief"
    player = axelrod.AdaptorBrief
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # No error.
        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(
            opponent=axelrod.AdaptorBrief(), expected_actions=actions, seed=0
        )

        # Error corrected.
        actions = [(C, C), (C, D), (D, C), (C, C)]
        self.versus_test(
            opponent=axelrod.AdaptorBrief(), expected_actions=actions, seed=22
        )

        # Error corrected, example 2
        actions = [(D, C), (C, D), (D, C), (C, D), (C, C)]
        self.versus_test(
            opponent=axelrod.AdaptorBrief(), expected_actions=actions, seed=925
        )

        # Versus Cooperator
        actions = [(C, C)] * 8
        self.versus_test(
            opponent=axelrod.Cooperator(), expected_actions=actions, seed=0
        )

        # Versus Defector
        actions = [(C, D), (D, D), (D, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(
            opponent=axelrod.Defector(), expected_actions=actions, seed=0
        )


class TestAdaptorLong(TestPlayer):

    name = "AdaptorLong"
    player = axelrod.AdaptorLong
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # No error.
        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(
            opponent=axelrod.AdaptorLong(), expected_actions=actions, seed=0
        )

        # Error corrected.
        actions = [(C, C), (C, D), (D, D), (C, C), (C, C)]
        self.versus_test(
            opponent=axelrod.AdaptorLong(), expected_actions=actions, seed=22
        )

        # Versus Cooperator
        actions = [(C, C)] * 8
        self.versus_test(
            opponent=axelrod.Cooperator(), expected_actions=actions, seed=0
        )

        # Versus Defector
        actions = [(C, D), (D, D), (C, D), (D, D), (D, D), (C, D), (D, D)]
        self.versus_test(
            opponent=axelrod.Defector(), expected_actions=actions, seed=0
        )
