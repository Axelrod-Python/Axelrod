"""Tests for grudger strategies."""

import random

import axelrod

from test_player import TestPlayer

C, D = 'C', 'D'


class TestCalculator(TestPlayer):

    name = "Calculator"
    player = axelrod.Calculator
    stochastic = False

    def test_cycle_detection(self):
        P1 = axelrod.Calculator()
        P1.history = [C] * 20
        P2 = axelrod.Player()
        P2.history = [C] * 20
        self.assertTrue(P1.detect_cycle(P2.history))
        #P2.history = [D] * 20
        self.assertTrue(P1.detect_cycle(P2.history))
        P2.history = [C, D] * 10
        self.assertTrue(P1.detect_cycle(P2.history))
        P2.history = [C, D, D, C] * 5
        self.assertTrue(P1.detect_cycle(P2.history))

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
        self.assertFalse(P1.detect_cycle(P2.history))
        self.assertEqual('C', P1.strategy(P2))

