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
        expected_actions = [(D, D)] * 90 + [(C, D)]
        self.versus_test(
            axl.Defector(),
            expected_actions=expected_actions,
            seed=6,
        )
        expected_actions = [(D, C)] * 10
        self.versus_test(
            axl.Cooperator(),
            expected_actions=expected_actions,
            seed=8,
        )
        expected_actions = [(D, D)] * 41 + [(C, D)]
        self.versus_test(
            axl.Defector(),
            expected_actions=expected_actions,
            seed=13,
        )
        expected_indices = [18, 39, 49, 67, 77, 116, 139, 142, 149]
        m = axl.Match((self.player(), axl.Defector()), turns=150, seed=111)
        result = m.play()
        indices = []
        for index, actions in enumerate(result):
            if actions == (C, D):
                indices.append(index)
        self.assertEqual(expected_indices, indices)
