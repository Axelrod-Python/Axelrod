"""Test for the forgiver strategies."""

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
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_strategy(self):
        """If opponent has defected more than 10 percent of the time, defect."""
        self.responses_test([C, C, C, C], [C, C, C, C], [C])
        self.responses_test([C, C, C, C, D], [C, C, C, D, C], [D])
        self.responses_test([C] * 11, [C] * 10 + [D], [C])


class TestForgivingTitForTat(TestPlayer):

    name = "Forgiving Tit For Tat"
    player = axelrod.ForgivingTitForTat
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_strategy(self):
        self.responses_test([C, C, C, C], [C, C, C, C], [C])
        self.responses_test([C, C, C, C, D], [C, C, C, D, C], [C])
        self.responses_test([C] * 11, [C] * 9 + [D] * 2, [D])
