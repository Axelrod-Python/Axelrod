"""Tests for the Neg Strategy"""

import axelrod

from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D


class TestNegation(TestPlayer):

    name = "Negation"
    player = axelrod.Negation
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
            opponent=axelrod.Alternator(), expected_actions=actions, seed=1
        )
        actions = [(D, C), (D, D), (C, C)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=2
        )
        actions = [(C, C), (D, C), (D, C)]
        self.versus_test(
            opponent=axelrod.Cooperator(), expected_actions=actions, seed=1
        )
        actions = [(D, D), (C, D), (C, D)]
        self.versus_test(opponent=axelrod.Defector(), expected_actions=actions, seed=2)
