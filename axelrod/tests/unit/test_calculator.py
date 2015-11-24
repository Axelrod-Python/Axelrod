"""Tests for calculator strategies."""

import random

import axelrod

from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestCalculator(TestPlayer):

    name = "Calculator"
    player = axelrod.Calculator
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)

        P1 = axelrod.Calculator()
        P1.history = [C] * 20
        P2 = axelrod.Player()
        P2.history = [C, D] * 10
        # Defects on cycle detection
        self.assertEqual(D, P1.strategy(P2))

        # Test non-cycle response
        history = [C, C, D, C, C, D, C, C, C, D, C, C, C, C, D, C, C, C, C, C]
        P2.history = history
        self.assertEqual(C, P1.strategy(P2))

        # Test post 20 rounds responses
        self.responses_test([C] * 21, [C] * 21, [D])
        history = [C, C, D, C, C, D, C, C, C, D, C, C, C, C, D, C, C, C, C, C, D]
        self.responses_test([C] * 21, history, [D])
        history = [C, C, D, C, C, D, C, C, C, D, C, C, C, C, D, C, C, C, C, C, D, C]
        self.responses_test([C] * 22, history, [C])

