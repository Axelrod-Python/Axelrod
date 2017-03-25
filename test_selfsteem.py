"""Tests for the SelfSteem strategy."""

import axelrod
import random
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D

class TestSelfSteem(TestPlayer):

    name = "SelfSteem"
    player = axelrod.SelfSteem
    expected_classifier = {
        'memory_depth': float("inf"),
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):

        # Check for f > 0.95, defect
        actions = [(C, C), (C, C), (D, C), (D, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions = actions)

        actions = [(C, C), (C, C), (D, C), 
                   (D, C), (C, C), (D, C)] + [(C, C)] * 6 + [(D, C)]
	    self.versus_test(axelrod.Cooperator(), expected_actions = actions)

	    # Check for f < -0.95, cooperate
	    actions = [(D, C), (C, C), (D, C),v(D, C), 
                   (C, C), (D, C), (C, C), (C, C)]
	    self.versus_test(opponent=axelrod.MockPlayer([C]), expected_actions = actions)

	    actions = [(C, D)] + [(D, D)] * 6 + [(C, D), 
                   (C, D)] + [(D, D)] * 6 + [(C, D)]
	    self.versus_test(opponent=axelrod.MockPlayer([D]), expected_actions = actions)

	    # Check for -0.3 < f < 0.3, random
	    actions = [(D, C), (C, C), (D, C), (D, C), 
                   (C, C), (D, C)] + [(C, C)] * 6 + [(D, C),(D, C)] + [(C, C)] * 7
	    self.versus_test(opponent=axelrod.MockPlayer([C]), expected_actions = actions, seed=6)

	    actions = [(D, D)] * 7 + [(C, D), (C, D)] + [(D, D)] * 8 + [(C, D), 
                   (C, D), (D, D), (D, D), (D, D)]
	    self.versus_test(opponent=axelrod.MockPlayer([D]), expected_actions = actions, seed=5)

	    # Check for 0.95 > abs(f) > 0.3, follows TitForTat
	    actions = [(D, D)] * 5 + [(C, D), (D, D), (C, D), 
                   (C, D), (D, D), (C, D)] + [(D, D)] * 5
	    self.versus_test(opponent=axelrod.MockPlayer([D]), expected_actions = actions)

	    actions = [(D, C), (C, C), (D, C), (D, C), 
                   (C, C), (D, C), (C, C), (C, C), (C, C), (C, C)]
	    self.versus_test(opponent=axelrod.MockPlayer([C]), expected_actions = actions)
