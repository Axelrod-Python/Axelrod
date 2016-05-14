"""Test for the Handshake strategy."""

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
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.responses_test([], [], [C, D])

        self.responses_test([C, D], [C, D], [C])
        self.responses_test([C, D], [C, C], [D])
        self.responses_test([C, D], [D, C], [D])
        self.responses_test([C, D], [D, D], [D])
