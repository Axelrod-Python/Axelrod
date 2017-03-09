"""Tests for the golden and other mathematical strategies."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGolden(TestPlayer):

    name = '$\phi$'
    player = axelrod.Golden
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Cooperates initially.
        self.first_play_test(C)
        # If the opposing player does not defect initially then strategy
        # defects.
        self.responses_test([D], [C], [C])
        # If the ratio of Cs to Ds is greater than the golden ratio then
        # strategy defects.
        self.responses_test([D], [C] * 4, [C, C, D, D])
        # If the ratio of Cs to Ds is less than the golden ratio then strategy
        # co-operates
        self.responses_test([C], [C] * 4, [D] * 4)


class TestPi(TestPlayer):

    name = '$\pi$'
    player = axelrod.Pi
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Cooperates initially
        self.first_play_test(C)
        # If the opposing player does not defect initially then strategy
        # defects.
        self.responses_test([D], [C], [C])
        # If the ratio of Cs to Ds is greater than pi then strategy defects.
        self.responses_test([D], [C] * 4, [C, C, C, D])
        # If the ratio of Cs to Ds is less than pi then strategy co-operates.
        self.responses_test([C], [C] * 4, [C, C, D, D])


class Teste(TestPlayer):

    name = '$e$'
    player = axelrod.e
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Cooperates initially.
        self.first_play_test(C)
        # If the opposing player does not defect initially then strategy
        # defects.
        self.responses_test([D], [C], [C])
        # If the ratio of Cs to Ds is greater than e then strategy defects.
        self.responses_test([D], [C] * 4, [C, C, D, D])
        # If the ratio of Cs to Ds is less than e then strategy co-operates.
        self.responses_test([C], [C] * 4, [C, D, D, D])
