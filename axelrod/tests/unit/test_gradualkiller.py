"""Tests for the gradual killer strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGradualKiller(TestPlayer):

    name = "Gradual Killer"
    player = axelrod.GradualKiller
    expected_classifier = {
        'memory_depth': float('Inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by Defecting."""
        self.first_play_test(D)
        self.second_play_test(D, D, D, D)
        self.responses_test(D * 5 + C * 2)

        self.responses_test(C * 4, D * 5 + C * 2, C * 7)

        self.responses_test(C, D * 5 + C * 2, C * 6 + D)
        self.responses_test(C, D * 5 + C * 3, C * 6 + D * 2)
        self.responses_test(C, D * 5 + C * 4, C * 6 + D * 2 + C)
        self.responses_test(C, D * 5 + C * 5, C * 6 + D * 2 + C + C)

        self.responses_test(C, D * 5 + C * 2, C * 5 + D + C)
        self.responses_test(C, D * 5 + C * 3, C * 5 + D + C * 2)
        self.responses_test(C, D * 5 + C * 4, C * 5 + D + C * 2 + D)
        self.responses_test(C, D * 5 + C * 5, C * 5 + D + C * 2 + D * 2)

        self.responses_test(D, D * 5 + C * 2, C * 5 + D * 2)
        self.responses_test(D, D * 5 + C * 2 + D, C * 5 + D * 2 + C)
        self.responses_test(D, D * 5 + C * 2 + D * 2, C * 5 + D * 2 + C * 2)
        self.responses_test(D, D * 5 + C * 2 + D * 3, C * 5 + D * 2 + C * 2 + D)
