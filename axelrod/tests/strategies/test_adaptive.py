"""Tests for the Adaptive strategy."""

import axelrod as axl

from .test_player import TestMatch, TestPlayer

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
        player.play(opponent)
        player.play(opponent)
        self.assertEqual(3, player.scores[C])
        game = axl.Game(-3, 10, 10, 10)
        player.set_match_attributes(game=game)
        player.play(opponent)
        self.assertEqual(0, player.scores[C])
