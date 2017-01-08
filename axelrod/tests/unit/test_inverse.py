"""Tests for the inverse strategy."""
import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestInverse(TestPlayer):

    name = "Inverse"
    player = axelrod.Inverse
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
        self.first_play_test(C)

        self.responses_test(C, C * 4, C * 4)
        self.responses_test(C, C * 5, C * 5)

        self.responses_test(D, C, D, random_seed=5)
        self.responses_test(D, C + D, D + D)
        self.responses_test(D, C + D * 7, D * 8)

        self.responses_test(C, C * 4, (C + D) * 2, random_seed=6)
        self.responses_test(C, C * 6, C * 4 + D * 2)
        self.responses_test(D, C * 9, D * 8 + C)
        self.responses_test(D, C * 9, D * 8 + C, random_seed=6)
