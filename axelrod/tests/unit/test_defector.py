"""Test for the defector strategy."""

import axelrod

from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestDefector(TestPlayer):

    name = "Defector"
    player = axelrod.Defector
    expected_classifier = {
        'memory_depth': 0,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_state': False,
        'manipulates_source': False
    }

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(D)

    def test_effect_of_strategy(self):
        """Test that always defects."""
        self.markov_test([D, D, D, D])


class TestTrickyDefector(TestPlayer):

    name = "Tricky Defector"
    player = axelrod.TrickyDefector
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(D)

    def test_effect_of_strategy(self):
        """Test if it tries to trick opponent"""
        self.markov_test([D, D, D, D])
        self.responses_test([C, C, C], [C, C, C], [D])
        self.responses_test([C, C, C, D, D], [C, C, C, C, D], [D])
        history = [C, C, C, D, D] + [C] * 11
        opponent_history = [C, C, C, C, D] + [D] + [C] * 10
        self.responses_test(history, opponent_history,[D])
