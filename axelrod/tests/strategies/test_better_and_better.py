"""Tests for the BetterAndBetter strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestBetterAndBetter(TestPlayer):

    name = "Better and Better"
    player = axl.BetterAndBetter
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        """Tests that the strategy gives expected behaviour."""
        self.versus_test(
            axl.Defector(),
            expected_actions=[
                (D, D),
                (D, D),
                (D, D),
                (D, D),
                (C, D),
                (D, D),
                (D, D),
                (D, D),
                (D, D),
            ],
            seed=6,
        )
        self.versus_test(
            axl.Cooperator(),
            expected_actions=[
                (D, C),
                (D, C),
                (D, C),
                (D, C),
                (D, C),
                (D, C),
                (D, C),
                (D, C),
                (D, C),
            ],
            seed=8,
        )
        self.versus_test(
            axl.Defector(),
            expected_actions=[
                (C, D),
                (D, D),
                (D, D),
                (D, D),
                (D, D),
                (D, D),
                (D, D),
                (D, D),
                (D, D),
            ],
            seed=1514,
        )
        actions = []
        for index in range(200):
            if index in [
                64,
                79,
                91,
                99,
                100,
                107,
                111,
                119,
                124,
                127,
                137,
                141,
                144,
                154,
                192,
                196,
            ]:
                actions.append((C, D))
            else:
                actions.append((D, D))
        self.versus_test(axl.Defector(), expected_actions=actions, seed=8)
