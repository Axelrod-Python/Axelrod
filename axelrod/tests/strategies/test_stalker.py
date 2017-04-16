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
        actions = [(C, D), (C, D), (C, C), (D, C), (C, C), (D, D)]
        self.versus_test(opponent=axelrod.MockPlayer([D] * 2 + [C] * 3), expected_actions=actions)
        
        actions = [(C, C), (C, C), (C, D), (D, D), (D, D), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.MockPlayer([C] * 2 + [D] * 4), expected_actions=actions)
        
        # wish_score < current_average_score < very_good_score
        actions = [(C, C)] * 7 + [(C, D), (C, D), (C, C), (C, C), (D, C)]
        self.versus_test(opponent=axelrod.MockPlayer([C] * 7 + [D] * 2), expected_actions=actions)
        
        actions = [(C, C)] * 7 + [(C, D), (C, C), (D, C)]
        self.versus_test(opponent=axelrod.MockPlayer([C] * 7 + [D]), expected_actions=actions)
       
        # current_average_score > 2
        actions = [(C, C)] * 9 + [(D, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)
    
        # 1 < current_average_score < 2
        actions = [(C, C)] * 7 + [(C, D)] * 4 + [(D, D)]
        self.versus_test(opponent=axelrod.MockPlayer([C] * 7 + [D] * 5), expected_actions=actions)

        # current_average_score < 1
        actions = [(C, D)] + [(D, D)] * 2 + [(C, D)] * 3 + [(D, D),
                   (C, D), (D, D), (C, D), (D, D), (C, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions, seed=6)
        
        actions = [(C, D)] * 3 + [(D, D), (C, D), (D, D), (C, D),
                   (C, D), (D, D), (C, D), (C, D), (C, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions, seed=7)
       
        # defect in last round
        actions = [(C, C)] * 199 + [(D, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, match_attributes={"length": 200})
        
        # length unknown will not defect in last round
        actions = [(C, C)] * 6
        self.versus_test(opponent=axelrod.MockPlayer([C]), expected_actions=actions, match_attributes={"length":-1})
