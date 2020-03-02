"""
Tests for the Exponential strategy

"""

import axelrod
from test_player import TestPlayer


C, D = axelrod.Action.C, axelrod.Action.D


class Exponential(TestPlayer):
    

    name = "Exponential"

    player = axelrod.Exponential

    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        self.first_play_test(C)

        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        actions = [(C, C), (C, D), (D, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

  
        
        opponent = axelrod.MockPlayer(actions=[C, D, C, D, C, C, C, D, D, C])
        actions = [
            (C, C),
            (C, D),
            (D, C),
            (C, D),
            (D, C),
            (D, C),
            (D, C),
            (D, D),
            (D, D),
            (D, C),
        ]
        
        self.versus_test(opponent, expected_actions=actions)

