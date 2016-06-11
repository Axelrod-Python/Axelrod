"""Test for the Naive Prober strategy."""

import axelrod
from .test_player import TestPlayer, test_responses

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestNaiveProber(TestPlayer):

    name = "Naive Prober: 0.1"
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
        self.first_play_test(C)
        # Always retaliate a defection
        self.responses_test([C] * 2, [C, D], [D])

    def test_random_defection(self):
        # Random defection
        player = self.player(0.4)
        opponent = axelrod.Random()
        test_responses(self, player, opponent, [C], [C], [D], random_seed=1)

    def test_reduction_to_TFT(self):
        player = self.player(0)
        opponent = axelrod.Random()
        test_responses(self, player, opponent, [C], [C], [C], random_seed=1)
        test_responses(self, player, opponent, [C], [D], [D])
        test_responses(self, player, opponent, [C, D], [D, C], [C])
        test_responses(self, player, opponent, [C, D], [D, D], [D])
