"""Tests for calculator strategies."""

import random

import axelrod

from .test_player import TestPlayer

C, D = 'C', 'D'


class TestCalculator(TestPlayer):

    name = "Calculator"
    player = axelrod.Calculator
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
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
        self.assertEqual('D', P1.strategy(P2))

        # Test non-cycle response
        history = [C, C, D, C, C, D, C, C, C, D, C, C, C, C, D, C, C, C, C, C]
        P2.history = history
        self.assertEqual('C', P1.strategy(P2))
