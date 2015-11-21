"""Test for the cooperator strategy."""

import axelrod

from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestCooperator(TestPlayer):

    name = "Cooperator"
    player = axelrod.Cooperator
    expected_classifier = {
        'memory_depth': 0,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Simply does the opposite to what the strategy did last time."""
        self.markov_test([C, C, C, C])


class TestTrickyCooperator(TestPlayer):

    name = "Tricky Cooperator"
    player = axelrod.TrickyCooperator
    expected_classifier = {
        'memory_depth': 10,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Test if it tries to trick opponent"""
        self.responses_test([C, C, C], [C, C, C], [D])
        self.responses_test([C, C, C, D, D], [C, C, C, C, D], [C])
        history = [C, C, C, D, D] + [C] * 11
        opponent_histroy = [C, C, C, C, D] + [D] + [C] * 10
        self.responses_test(history, opponent_histroy,[D])
