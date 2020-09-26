"""Tests for the inverse strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestInverse(TestPlayer):

    name = "Inverse"
    player = axl.Inverse
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Test that as long as the opponent has not defected the player will
        # cooperate, regardless of the random seed.
        self.versus_test(axl.Cooperator(), expected_actions=[(C, C)], seed=None)

        # Tests that if opponent has played all D then player chooses D,
        # regardless of the random seed.
        self.versus_test(
            axl.Defector(), expected_actions=[(C, D)] + [(D, D)] * 9, seed=None
        )

        expected_actions = [
            (C, D),
            (D, C),
            (D, C),
            (C, D),
            (D, C),
            (C, C),
            (D, C),
            (C, C),
            (C, D),
            (D, D),
        ]
        self.versus_test(
            axl.MockPlayer(actions=[a[1] for a in expected_actions]),
            expected_actions=expected_actions,
            seed=0,
        )
