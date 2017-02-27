"""Tests for the VeryBad strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D

class TestCooperator(TestPlayer):

    name = "VeryBad"
    player = axelrod.VeryBad
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):        
        # Starts by cooperating for the first 3 moves.
        self.first_play_test(C)
        self.responses_test([C], [C] * 2, [C] * 2)
        self.responses_test([C], [C] * 3, [D] * 3)

        #Cooperate if opponent's probable action to Defect
        self.responses_test([D], [C] * 13 + [D] * 7, [D] * 16 + [C] * 4)
            
        #Cooperate if opponent's probable action to Cooperate
        self.responses_test([C], [D] * 13 + [C] * 7, [C] * 12 + [D] * 8)
        
        #TitForTat if opponent's equally probable to Cooperate or Defect
        self.responses_test([D], [D] * 13 + [C] * 11, [C] * 12 + [D] * 12)
        self.responses_test([C], [D] * 13 + [C] * 11, [D] * 12 + [C] * 12)
