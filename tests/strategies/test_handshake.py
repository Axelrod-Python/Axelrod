"""Tests for the Handshake strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestHandshake(TestPlayer):

    name = "Handshake"
    player = axl.Handshake
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (D, D)] + [(C, C), (C, D)] * 10
        self.versus_test(axl.Alternator(), expected_actions=actions)

        actions = [(C, C), (D, C)] + [(D, C)] * 20
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        opponent = axl.MockPlayer([D, C])
        actions = [(C, D), (D, C)] + [(D, D), (D, C)] * 10
        self.versus_test(opponent, expected_actions=actions)

        actions = [(C, D), (D, D)] + [(D, D)] * 20
        self.versus_test(axl.Defector(), expected_actions=actions)
