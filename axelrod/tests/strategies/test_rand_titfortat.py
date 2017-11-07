"""Tests for the random tit for tat strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D


class TestRandomTitForTat(TestPlayer):
    """Tests for random tit for tat strategy."""

    name = "Random Tit for Tat"
    player = axelrod.RandomTitForTat
    expected_classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Test that strategy is randomly picked (not affected by history)."""
        opponent = axelrod.MockPlayer()
        actions = [(C, C), (D, C), (D, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer()
        actions = [(D, C), (D, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer()
        actions = [(D, C), (D, C), (D, C)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer()
        actions = [(C, C), (C, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions)
