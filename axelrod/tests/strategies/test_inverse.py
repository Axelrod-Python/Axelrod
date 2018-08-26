"""Tests for the inverse strategy."""

import axelrod

from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D


class TestInverse(TestPlayer):

    name = "Inverse"
    player = axelrod.Inverse
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
        # cooperate.
        self.versus_test(axelrod.Cooperator(), expected_actions=[(C, C)])

        # Tests that if opponent has played all D then player chooses D.
        self.versus_test(axelrod.Defector(), expected_actions=[(C, D)] + [(D, D)] * 9)

        expected_actions = [
            (C, D),
            (D, C),
            (D, C),
            (D, D),
            (D, C),
            (C, C),
            (C, C),
            (C, C),
            (C, D),
            (D, D),
        ]
        self.versus_test(
            axelrod.MockPlayer(actions=[a[1] for a in expected_actions]),
            expected_actions=expected_actions,
            seed=0,
        )
