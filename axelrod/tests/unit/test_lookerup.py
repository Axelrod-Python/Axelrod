"""Test for the Looker Up strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestLookerUp(TestPlayer):

    name = "LookerUp"
    player = axelrod.LookerUp

    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Repeats last action of opponent history."""
        self.markov_test([C, D, C, D])
        self.responses_test([C] * 4, [C, C, C, C], [C])
        self.responses_test([C] * 5, [C, C, C, C, D], [D])

    def test_defector_table(self):
        """Testing a lookup table that always defects if there is enough history"""
        defector_table = { 
            ('', 'C', 'D') : 'D',         
            ('', 'D', 'D') : 'D',         
            ('', 'C', 'C') : 'D',
            ('', 'D', 'C') : 'D',     
        }
        self.player = lambda : axelrod.LookerUp(defector_table)
        self.responses_test([C,C], [C,C], [D]) 
        self.responses_test([C,D], [D,C], [D]) 
        self.responses_test([D,D], [D,D], [D]) 