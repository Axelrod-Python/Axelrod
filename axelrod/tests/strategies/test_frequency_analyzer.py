"""Tests for the FrequencyAnalyzer strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class Test(TestPlayer):

    name = "FrequencyAnalyzer"
    player = axl.FrequencyAnalyzer
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy_early(self):
        # Test games that end while still in dataset generation phase (<30 turns)
        opponent_actions = [C, C, D, C, D]
        expected = [(C, C), (C, C), (C, D), (D, C), (C, D)]
        self.versus_test(
            axl.MockPlayer(opponent_actions), expected_actions=expected, seed=4
        )

    def test_strategy_defector(self):
        # Test against all defections
        opponent_actions = [D] * 30
        expected = [(C, D)] + [(D, D)] * 29
        self.versus_test(
            axl.MockPlayer(opponent_actions), expected_actions=expected, seed=4
        )

    def test_strategy_cooperator(self):
        # Test games that end while still in dataset generation phase (<30 turns)
        opponent_actions = [C] * 30
        expected = [(C, C)] * 30
        self.versus_test(
            axl.MockPlayer(opponent_actions), expected_actions=expected, seed=4
        )

    def test_strategy_random(self):
        # Test of 50 turns against random strategy
        opponent_actions = [
            C,
            D,
            D,
            D,
            D,
            D,
            D,
            C,
            D,
            C,
            D,
            C,
            D,
            C,
            D,
            D,
            C,
            D,
            C,
            D,
            D,
            C,
            D,
            D,
            D,
            D,
            D,
            C,
            C,
            D,
            D,
            C,
            C,
            C,
            D,
            D,
            C,
            D,
            C,
            C,
            C,
            D,
            D,
            C,
            C,
            C,
            D,
            C,
            D,
            D,
        ]
        expected = [
            (C, C),
            (C, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (C, D),
            (D, C),
            (C, D),
            (D, C),
            (C, D),
            (D, C),
            (C, D),
            (D, D),
            (D, C),
            (C, D),
            (D, C),
            (C, D),
            (D, D),
            (D, C),
            (C, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (C, C),
            (C, D),  # rd 30 (end of dataset generation phase)
            (D, D),
            (D, C),
            (
                D,
                C,
            ),  # example of non TFT (by this point, FrequencyAnalyzer is generally distrustful of opponent)
            (C, C),
            (D, D),
            (D, D),
            (D, C),
            (D, D),
            (D, C),
            (D, C),
            (D, C),
            (D, D),
            (D, D),
            (D, C),
            (D, C),
            (D, C),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
        ]
        self.versus_test(
            axl.MockPlayer(opponent_actions), expected_actions=expected, seed=4
        )
