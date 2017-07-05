"""Tests for the Memorytwo strategies."""

import axelrod
from .test_player import TestPlayer


C, D = axelrod.Action.C, axelrod.Action.D


class TestMEM2(TestPlayer):

    name = "MEM2"
    player = axelrod.MEM2
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Start with TFT
        actions = [(C, C), (C, C)]
        self.versus_test(opponent=axelrod.Cooperator(),
                         expected_actions=actions,
                         attrs={"play_as": "TFT", "shift_counter": 1,
                                "alld_counter": 0})
        actions = [(C, D), (D, D)]
        self.versus_test(opponent=axelrod.Defector(), expected_actions=actions,
                         attrs={"play_as": "TFT", "shift_counter": 1,
                                "alld_counter": 0})
        # TFTT if C, D and D, C
        opponent = axelrod.MockPlayer([D, C, D, D])
        actions = [(C, D), (D, C), (C, D), (C, D)]
        self.versus_test(opponent=opponent, expected_actions=actions,
                         attrs={"play_as": "TFTT", "shift_counter": 1,
                                "alld_counter": 0})

        opponent = axelrod.MockPlayer([D, C, D, D])
        actions = [(C, D), (D, C), (C, D), (C, D), (D, D),
                   (D, C), (D, D), (D, D), (D, D), (D, C)]
        self.versus_test(opponent=opponent, expected_actions=actions,
                         attrs={"play_as": "ALLD", "shift_counter": -1,
                                "alld_counter": 2})
