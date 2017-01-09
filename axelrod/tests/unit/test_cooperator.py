"""Tests for the cooperator strategy."""

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
        self.second_play_test(C, C, C, C)


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
        self.first_play_test(C)
        self.responses_test(D, C * 3, C * 3)
        self.responses_test(C, C * 3 + D * 2 + C * 5)
        history = C * 3 + D * 2 + C * 11
        opponent_history = C * 4 + D * 2 + C * 10
        self.responses_test(D, history, opponent_history)
