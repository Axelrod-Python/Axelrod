"""Tests for the Neg Strategy"""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestNegation(TestPlayer):

    name = "Negation"
    player = axelrod.Negation
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # First move is random.
        self.first_play_test(C, seed=1)
        self.first_play_test(D, seed=2)
        # Repeats opposite of opponents last action.
        self.second_play_test(D, C, D, C)
