"""Tests for the AverageCopier strategies."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestAverageCopier(TestPlayer):

    name = "Average Copier"
    player = axelrod.AverageCopier
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test that the first strategy is picked randomly.
        self.responses_test([C], seed=1)
        self.responses_test([D], seed=2)
        # Tests that if opponent has played all C then player chooses C.
        self.responses_test([C, C, C], [C, C, C, C], [C, C, C, C], seed=5)
        # Tests that if opponent has played all D then player chooses D.
        self.responses_test([D, D, D], [C, C, C, C], [D, D, D, D], seed=5)


class TestNiceAverageCopier(TestPlayer):

    name = "Nice Average Copier"
    player = axelrod.NiceAverageCopier
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Cooperates initially.
        self.first_play_test(C)
        # If opponent has played all C then player chooses C.
        self.responses_test([C, C, C], [C, C, C, C], [C, C, C, C], seed=5)
        # If opponent has played all D then player chooses D.
        self.responses_test([D, D, D], [D, D, D, D], [D, D, D, D], seed=5)
