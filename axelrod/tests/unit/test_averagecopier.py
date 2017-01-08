"""Tests for the average_copier strategy."""

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
        """Test that the first strategy is picked randomly."""
        self.responses_test(C, random_seed=1)
        self.responses_test(D, random_seed=2)

    def test_when_oppenent_all_Cs(self):
        """Tests that if opponent has played all C then player chooses C."""
        self.responses_test(C * 3, C * 4, C * 4, random_seed=5)

    def test_when_opponent_all_Ds(self):
        """Tests that if opponent has played all D then player chooses D."""
        self.responses_test(D * 4, C * 4, D * 4, random_seed=5)


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
        # First move is cooperate.
        self.first_play_test(C)
        # If opponent has played all C then player chooses C.
        self.responses_test(C * 3, C * 4, C * 4, random_seed=5)
        # If opponent has played all D then player chooses D.
        self.responses_test(D * 3, D * 4, D * 4, random_seed=5)
