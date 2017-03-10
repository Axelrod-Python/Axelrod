"""Tests for the Alternator strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestAlternator(TestPlayer):

    name = "Alternator"
    player = axelrod.Alternator
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating.
        self.first_play_test(C)

        opponent = axelrod.MockPlayer()
        actions = [(C, C), (D, C)] * 5
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer(D)
        actions = [(C, D), (D, D)] * 5
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer([D, C])
        actions = [(C, D), (D, C)] * 5
        self.versus_test(opponent, expected_actions=actions)
