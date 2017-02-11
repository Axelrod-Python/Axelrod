"""Tests for the ShortMem strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D

class TestCooperator(TestPlayer):

    name = "ShortMem"
    player = axelrod.ShortMem
    expected_classifier = {
        'memory_depth': 10,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating for the first ten moves.
        self.responses_test([C], [C] * 4, [D] * 4)
        self.responses_test([C], [C] * 9, [D] * 9)
        self.responses_test([C], [C] * 4 + [D] *6, [D] * 4 + [C] * 6)
        
        #Cooperate if in the last ten moves, Cooperations - Defections >= 3
        self.responses_test([C], [C] * 13 + [D] * 7, [D] * 16 + [C] * 7)
            
        #Defect if in the last ten moves, Defections - Cooperations >= 3
        self.responses_test([D], [D] * 13 + [C] * 7, [C] * 12 + [D] * 8)
        
        #If neither of the above conditions are met, apply TitForTat 
        self.responses_test([D], [C] * 13 + [D] * 7, [C] * 15 + [D] * 5)
        self.responses_test([C], [C] * 17 + [D] * 7, [D] * 18 + [C] * 6)
