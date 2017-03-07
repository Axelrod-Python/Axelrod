"""Tests for the random strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestRandom(TestPlayer):

    name = "Random: 0.5"
    player = axelrod.Random
    expected_classifier = {
        'memory_depth': 0,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Test that strategy is randomly picked (not affected by history)."""
        self.first_play_test(C, seed=1)
        self.first_play_test(D, seed=2)

        opponent = axelrod.MockPlayer()
        outcomes = [(C, C), (D, C), (D, C), (C, C)]
        self.versus_test(opponent, expected_outcomes=outcomes, seed=1)

        opponent = axelrod.MockPlayer()
        outcomes = [(D, C), (D, C), (C, C)]
        self.versus_test(opponent, expected_outcomes=outcomes, seed=2)

        opponent = axelrod.MockPlayer()
        outcomes = [(D, C), (D, C), (D, C)]
        self.versus_test(opponent, expected_outcomes=outcomes,
                         init_kwargs={"p": 0})

        opponent = axelrod.MockPlayer()
        outcomes = [(C, C), (C, C), (C, C)]
        self.versus_test(opponent, expected_outcomes=outcomes,
                         init_kwargs={"p": 1})

    def test_deterministic_classification(self):
        """Test classification when p is 0 or 1"""
        for p in [0, 1]:
            player = axelrod.Random(p)
            self.assertFalse(player.classifier['stochastic'])
