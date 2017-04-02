"""Tests for the Stalker strategy."""

import axelrod
import random
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D

class TestStalker(TestPlayer):

    name = "Stalker: D"
    player = axelrod.Stalker
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(["game", "length"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Start with cooperation
        self.first_play_test(C)

        # current_average_score > very_good_score
        self.responses_test([D], [C] * 2 + [D] * 4, [D] * 2 + [C] * 4)
        self.responses_test([D], [D] * 2 + [C] * 4, [C] * 6)

        # wish_score < current_average_score < very_good_score
        self.responses_test([C], [C] * 7 + [D] * 2, [C] * 7 + [D] * 2)
        self.responses_test([C], [C] * 7 + [C], [C] * 7 + [D])

        # current_average_score > 2
        self.responses_test([C], [C] * 10, [C] * 10)

        # 1 < current_average_score < 2
        self.responses_test([D], [C] * 7 + [C] * 5, [C] * 7 + [D] * 5)

        # current_average_score < 1
        self.responses_test([D], [D] * 7 + [C] * 5, [D] * 7 + [D] * 5, seed = 6)
        self.responses_test([C], [D] * 7 + [C] * 5, [D] * 7 + [D] * 5, seed = 7)

        # defect in last round
        self.responses_test([C, D], [C] * 198, [C] * 198, length=200)
