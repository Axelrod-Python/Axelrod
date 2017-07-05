"""Tests for the golden and other mathematical strategies."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D


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
        actions = [(C, C), (D, D), (C, C), (D, D), (C, C)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions)

        actions = [(C, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(opponent=axelrod.Cooperator(),
                         expected_actions=actions)

        actions = [(C, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(opponent=axelrod.Defector(),
                         expected_actions=actions)


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
        actions = [(C, C), (D, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions)

        actions = [(C, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(opponent=axelrod.Cooperator(),
                         expected_actions=actions)

        actions = [(C, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(opponent=axelrod.Defector(),
                         expected_actions=actions)


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
        actions = [(C, C), (D, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions)

        actions = [(C, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(opponent=axelrod.Cooperator(),
                         expected_actions=actions)

        actions = [(C, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(opponent=axelrod.Defector(),
                         expected_actions=actions)
