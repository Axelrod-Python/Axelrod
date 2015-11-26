"""Test for the average_copier strategy."""

import random

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
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Test that the first strategy is picked randomly."""
        self.responses_test([], [], [C], random_seed=1)
        self.responses_test([], [], [D], random_seed=2)

    def test_when_oppenent_all_Cs(self):
        """
        Tests that if opponent has played all C then player chooses C
        """
        self.responses_test([C, C, C, C], [C, C, C, C], [C, C, C],
                            random_seed=5)

    def test_when_opponent_all_Ds(self):
        """
        Tests that if opponent has played all D then player chooses D
        """
        self.responses_test([C, C, C, C], [D, D, D, D], [D, D, D], random_seed=5)


class TestNiceAverageCopier(TestPlayer):

    name = "Nice Average Copier"
    player = axelrod.NiceAverageCopier
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Test that the first strategy is cooperation."""
        self.first_play_test(C)

    def test_when_oppenent_all_Cs(self):
        """
        Tests that if opponent has played all C then player chooses C
        """
        self.responses_test([C, C, C, C], [C, C, C, C], [C, C, C],
                            random_seed=5)

    def test_when_opponent_all_Ds(self):
        """
        Tests that if opponent has played all D then player chooses D
        """
        self.responses_test([D, D, D, D], [D, D, D, D], [D, D, D],
                            random_seed=5)
