"""Test for the inverse strategy."""

import random

import axelrod

from .test_player import TestPlayer

C, D = 'C', 'D'


class TestInverse(TestPlayer):

    name = "Inverse"
    player = axelrod.Inverse
    behaviour = {
        'stochastic': True
    }

    def test_strategy(self):
        """
        Test that initial strategy cooperates.
        """
        self.first_play_test(C)

    def test_that_cooperate_if_opponent_has_not_defected(self):
        """
        Test that as long as the opponent has not defected the player will cooperate.
        """
        self.responses_test([C] * 4, [C] * 4, [C])
        self.responses_test([C] * 5, [C] * 5, [C])

    def test_when_opponent_has_all_Ds(self):
        """
        Tests that if opponent has played all D then player chooses D
        """
        self.responses_test([C], [D], [D], random_seed=5)
        self.responses_test([C], [D, D], [D])
        self.responses_test([C] * 8, [D] * 8, [D])

    def test_when_opponent_som_Ds(self):
        """
        Tests that if opponent has played all D then player chooses D
        """
        random.seed(5)
        P1 = axelrod.Inverse()
        P2 = axelrod.Player()

        self.responses_test([C] * 4, [C, D, C, D], [C], random_seed=5)
        self.responses_test([C] * 6, [C, C, C, C, D, D], [C])
        self.responses_test([C] * 9, [D] * 8 + [C], [D])
        self.responses_test([C] * 9, [D] * 8 + [C], [D], random_seed=5)
