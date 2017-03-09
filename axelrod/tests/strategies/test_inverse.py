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
        # Cooperate initially.
        self.first_play_test(C)
        # Test that as long as the opponent has not defected the player will
        # cooperate.
        self.responses_test([C], [C] * 4, [C] * 4)
        self.responses_test([C], [C] * 5, [C] * 5)
        # Tests that if opponent has played all D then player chooses D.
        self.responses_test([D], [C], [D], seed=5)
        self.responses_test([D], [C], [D, D])
        self.responses_test([D], [C] * 8, [D] * 8)
        # Tests that if opponent has played all D then player chooses D.
        self.responses_test([C], [C] * 4, [C, D, C, D], seed=6)
        self.responses_test([C], [C] * 6, [C, C, C, C, D, D])
        self.responses_test([D], [C] * 9, [D] * 8 + [C])
        self.responses_test([D], [C] * 9, [D] * 8 + [C], seed=6)
