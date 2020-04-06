"""Tests for the tit for tat strategies."""

import copy

import random

import axelrod as axl
from axelrod.tests.property import strategy_lists

from hypothesis import given
from hypothesis.strategies import integers

from .test_player import TestMatch, TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestTitForTat(TestPlayer):
    """
    Note that this test is referred to in the documentation as an example on
    writing tests.  If you modify the tests here please also modify the
    documentation.
    """

    name = "Tit For Tat"
    player = axl.TitForTat
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Play against opponents
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(axl.Alternator(), expected_actions=actions)

        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(axl.Defector(), expected_actions=actions)

        # This behaviour is independent of knowledge of the Match length
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(
            axl.Alternator(),
            expected_actions=actions,
            match_attributes={"length": float("inf")},
        )

        # We can also test against random strategies
        actions = [(C, D), (D, D), (D, C), (C, C), (C, D)]
        self.versus_test(axl.Random(), expected_actions=actions, seed=0)

        actions = [(C, C), (C, D), (D, D), (D, C)]
        self.versus_test(axl.Random(), expected_actions=actions, seed=1)

        #  If you would like to test against a sequence of moves you should use
        #  a MockPlayer
        opponent = axl.MockPlayer(actions=[C, D])
        actions = [(C, C), (C, D), (D, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.MockPlayer(actions=[C, C, D, D, C, D])
        actions = [(C, C), (C, C), (C, D), (D, D), (D, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)
