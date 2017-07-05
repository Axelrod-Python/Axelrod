"""Tests for the Adaptive strategy."""

import axelrod
from .test_player import TestMatch, TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D


class TestAdaptive(TestPlayer):

    name = "Adaptive"
    player = axelrod.Adaptive
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        actions = [(C, C)] * 6 + [(D, C)] * 8
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D)] * 6 + [(D, D)] * 8
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        actions = [(C, C), (C, D)] * 3 + [(D, C), (D, D)] * 4
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        actions = [(C, C)] * 6 + [(D, C)] + [(D, D)] * 4 + [(C, D), (C, C)]
        self.versus_test(axelrod.TitForTat(), expected_actions=actions)

    def test_scoring(self):
        player = axelrod.Adaptive()
        opponent = axelrod.Cooperator()
        player.play(opponent)
        player.play(opponent)
        self.assertEqual(3, player.scores[C])
        game = axelrod.Game(-3, 10, 10, 10)
        player.set_match_attributes(game=game)
        player.play(opponent)
        self.assertEqual(0, player.scores[C])
