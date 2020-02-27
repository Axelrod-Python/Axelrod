"""Tests for the Adaptive strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestAdaptive(TestPlayer):

    name = "Adaptive"
    player = axl.Adaptive
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(["game"]),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C)] * 6 + [(D, C)] * 8
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        actions = [(C, D)] * 6 + [(D, D)] * 8
        self.versus_test(axl.Defector(), expected_actions=actions)

        actions = [(C, C), (C, D)] * 3 + [(D, C), (D, D)] * 4
        self.versus_test(axl.Alternator(), expected_actions=actions)

        actions = [(C, C)] * 6 + [(D, C)] + [(D, D)] * 4 + [(C, D), (C, C)]
        self.versus_test(axl.TitForTat(), expected_actions=actions)

    def test_scoring(self):
        player = axl.Adaptive()
        opponent = axl.Cooperator()
        match = axl.Match((player, opponent), turns=2, seed=9)
        match.play()
        self.assertEqual(3, player.scores[C])

        match = axl.Match((player, opponent), turns=1, reset=True, seed=9,
                          game=axl.Game(-3, 10, 10, 10))
        match.play()
        self.assertEqual(0, player.scores[C])
