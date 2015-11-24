"""Test for the random strategy."""

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
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Test that strategy is randomly picked (not affected by history)."""
        response_1 = [C, D, C]
        response_2 = [C, C, D]

        self.first_play_test(C, random_seed=1)
        self.first_play_test(D, random_seed=2)
        self.responses_test(response_1, response_2, [C], random_seed=1)
