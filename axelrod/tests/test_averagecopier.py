"""Test for the average_copier strategy."""

import random
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

import axelrod

from test_player import TestPlayer

C, D = 'C', 'D'


class TestAverageCopier(TestPlayer):

    name = "Average Copier"
    player = axelrod.AverageCopier
    stochastic = True

    @patch('random.choice')
    def test_strategy(self, mocked_random):
        """Test that the first strategy is picked randomly."""
        mocked_random.side_effect = responses = [C, D, D, C, C, C, D, D, C, C]
        self.responses_test([], [], responses, random_seed=1)

    def test_when_oppenent_all_Cs(self):
        """
        Tests that if opponent has played all C then player chooses C
        """
        self.responses_test([], [C, C, C, C], [C, C, C], random_seed=5)

    def test_when_opponent_all_Ds(self):
        """
        Tests that if opponent has played all D then player chooses D
        """
        self.responses_test([], [D, D, D, D], [D, D, D], random_seed=5)

class TestNiceAverageCopier(TestPlayer):

    name = "Nice Average Copier"
    player = axelrod.NiceAverageCopier
    stochastic = True

    def test_strategy(self):
        """Test that the first strategy is cooperation."""
        self.first_play_test(C)

    def test_when_oppenent_all_Cs(self):
        """
        Tests that if opponent has played all C then player chooses C
        """
        self.responses_test([], [C, C, C, C], [C, C, C], random_seed=5)

    def test_when_opponent_all_Ds(self):
        """
        Tests that if opponent has played all D then player chooses D
        """
        self.responses_test([], [D, D, D, D], [D, D, D], random_seed=5)
