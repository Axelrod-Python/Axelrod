"""Test for the random strategy."""

from mock import patch

import axelrod
from axelrod.tests.test_player import TestPlayer

C, D = 'C', 'D'


class TestRandom(TestPlayer):

    name = "Random"
    player = axelrod.Random
    stochastic = True

    @patch('random.choice')
    def test_strategy(self, mocked_random):
        """Test that strategy is randomly picked (not affected by history)."""
        response_1 = [C, D, C]
        response_2 = [C, C, D]
        mocked_random.side_effect = response_1 + response_2

        self.first_play_test(C, random_seed=1)
        self.first_play_test(D, random_seed=2)
        self.responses_test(response_1, response_2, [C], random_seed=1)
