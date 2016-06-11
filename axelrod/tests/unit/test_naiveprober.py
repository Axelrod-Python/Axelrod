"""Test for the Naive Prober strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestNaiveProber(TestPlayer):

    name = "RUA Naive Prober: 0.1"
    player = axelrod.NaiveProber
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        "Randomly defects and always retaliates like tit for tat."
        self.first_play_test(C, random_seed=1)
        self.first_play_test(D, random_seed=2)
        # Random defection
        self.responses_test([C] * 10, [C] * 10, [D], random_seed=3)
        # Always retaliate a defection
        self.responses_test([C] * 2, [C, D], [D])
