"""Tests for prober strategies."""

import random

import axelrod

from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestProber(TestPlayer):

    name = "Prober"
    player = axelrod.Prober
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """Starts by playing DCC."""
        self.responses_test([], [], [D, C, C])

    def test_strategy(self):
        # Defects forever if opponent cooperated in moves 2 and 3
        self.responses_test([D, C, C], [C, C, C], [D] * 10)
        self.responses_test([D, C, C], [D, C, C], [D] * 10)

        # Otherwise it plays like TFT
        self.responses_test([D, C, C], [C, D, C], [C])
        self.responses_test([D, C, C], [C, D, D], [D])
        self.responses_test([D, C, C, C], [C, D, C, D], [D])
        self.responses_test([D, C, C, D], [C, D, D], [D])


class TestProber2(TestPlayer):

    name = "Prober 2"
    player = axelrod.Prober2
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """Starts by playing DCC."""
        self.responses_test([], [], [D, C, C])

    def test_strategy(self):
        # Cooperates forever if opponent played D, C in moves 2 and 3
        self.responses_test([D, C, C], [C, D, C], [C] * 10)
        self.responses_test([D, C, C], [D, D, C], [C] * 10)

        # Otherwise it plays like TFT
        self.responses_test([D, C, C], [C, C, C], [C])
        self.responses_test([D, C, C], [C, D, D], [D])
        self.responses_test([D, C, C, D], [C, D, D, D], [D])
        self.responses_test([D, C, C, D], [C, D, D, C], [C])


class TestProber3(TestPlayer):

    name = "Prober 3"
    player = axelrod.Prober3
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """Starts by playing DC."""
        self.responses_test([], [], [D, C])

    def test_strategy(self):
        # Defects forever if opponent played C in move 2
        self.responses_test([D, C], [C, C], [D] * 10)
        self.responses_test([D, C], [D, C], [D] * 10)

        # Otherwise it plays like TFT
        self.responses_test([D, C, C], [C, D], [D])
        self.responses_test([D, C, C], [D, D], [D])
        self.responses_test([D, C, C, D], [C, D, C], [C])
        self.responses_test([D, C, C, D], [D, D, D], [D])
        self.responses_test([D, C, C, D, C], [C, D, C, C], [C])


class TestHardProber(TestPlayer):

    name = "Hard Prober"
    player = axelrod.HardProber
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """Starts by playing DC."""
        self.responses_test([], [], [D, D, C, C])

    def test_strategy(self):
        # Cooperates forever if opponent played C in moves 2 and 3
        self.responses_test([D, D, C, C], [C, C, C, C], [D] * 10)
        self.responses_test([D, D, C, C], [C, C, C, D], [D] * 10)
        self.responses_test([D, D, C, C], [D, C, C, C], [D] * 10)
        self.responses_test([D, D, C, C], [D, C, C, D], [D] * 10)

        # Otherwise it plays like TFT
        self.responses_test([D, D, C, C], [C, C, D, C], [C, C])
        self.responses_test([D, D, C, C], [C, C, D, D], [D])
        self.responses_test([D, D, C, C], [D, D, C, C], [C, C])
        self.responses_test([D, D, C, C], [D, D, C, D], [D])
        self.responses_test([D, D, C, C, D], [C, C, D, D], [D])
        self.responses_test([D, D, C, C, D], [D, D, C, C], [C])
