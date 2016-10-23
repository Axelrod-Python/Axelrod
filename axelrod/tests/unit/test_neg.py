"""Test for the Neg Strategy"""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D

class TestNeg(TestPlayer):

    name = "Neg"
    player = axelrod.Neg
    expected_classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_effect_of_strategy(self):
        """Repeats opposite of opponents last action."""
        self.markov_test([D, C, D, C])
		