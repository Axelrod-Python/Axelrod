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
        "memory_depth": 1,
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
        actions = [(C, C), (D, C), (C, D), (C, C)]
        self.versus_test(
            opponent=axelrod.AdaptorBrief(), expected_actions=actions, seed=1
        )


class TestAdaptorLong(TestPlayer):

    name = "AdaptorLong"
    player = axelrod.AdaptorLong
    expected_classifier = {
        "memory_depth": 1,
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
        actions = [(C, C), (D, C), (D, D), (D, D), (C, C)]
        self.versus_test(
            opponent=axelrod.AdaptorLong(), expected_actions=actions, seed=1
        )
