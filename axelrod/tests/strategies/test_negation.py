"""Tests for the Neg Strategy"""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestNegation(TestPlayer):

    name = "Negation"
    player = axl.Negation
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # First move is random.
        actions = [(C, C), (D, D), (C, C)]
        self.versus_test(
            opponent=axl.Alternator(), expected_actions=actions, seed=1
        )
        actions = [(D, C), (D, D), (C, C)]
        self.versus_test(
            opponent=axl.Alternator(), expected_actions=actions, seed=2
        )
        actions = [(C, C), (D, C), (D, C)]
        self.versus_test(
            opponent=axl.Cooperator(), expected_actions=actions, seed=1
        )
        actions = [(D, D), (C, D), (C, D)]
        self.versus_test(
            opponent=axl.Defector(), expected_actions=actions, seed=2
        )
