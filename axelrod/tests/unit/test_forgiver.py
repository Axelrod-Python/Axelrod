"""Tests for the forgiver strategies."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestForgiver(TestPlayer):

    name = "Forgiver"
    player = axelrod.Forgiver
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """If opponent has defected more than 10 percent of the time, defect."""
        self.first_play_test(C)
        self.responses_test(C, C * 4, C * 4)
        self.responses_test(D, C * 4 + D, C * 3 + D + C)
        self.responses_test(C, C * 11, C * 10 + D)


class TestForgivingTitForTat(TestPlayer):

    name = "Forgiving Tit For Tat"
    player = axelrod.ForgivingTitForTat
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        self.responses_test(C, C * 4, C * 4)
        self.responses_test(C, C * 4 + D, C * 3 + D + C)
        self.responses_test(D, C * 11, C * 9 + D * 2)
