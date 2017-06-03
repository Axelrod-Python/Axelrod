"""Tests for the Appeaser strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestAppeaser(TestPlayer):

    name = "Appeaser"
    player = axelrod.Appeaser
    expected_classifier = {
        'memory_depth': float('inf'),  # Depends on internal memory.
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):

        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D), (C, D), (D, D), (C, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[C, C, D, D])
        actions = [(C, C), (C, C), (C, D), (D, D), (C, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[C, C, D, D, D])
        actions = [(C, C), (C, C), (C, D), (D, D), (C, D), (D, C), (D, C)]
        self.versus_test(opponent, expected_actions=actions)
