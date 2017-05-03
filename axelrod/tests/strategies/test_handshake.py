"""Tests for the Handshake strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestHandshake(TestPlayer):

    name = "Handshake"
    player = axelrod.Handshake
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test first play
        self.first_play_test(C)

        actions = [(C, C), (D, D)] + [(C, C), (C, D)] * 10
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        actions = [(C, C), (D, C)] + [(D, C)] * 20
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        opponent = axelrod.MockPlayer([D, C])
        actions = [(C, D), (D, C)] + [(D, D), (D, C)] * 10
        self.versus_test(opponent, expected_actions=actions)

        actions = [(C, D), (D, D)] + [(D, D)] * 20
        self.versus_test(axelrod.Defector(), expected_actions=actions)
