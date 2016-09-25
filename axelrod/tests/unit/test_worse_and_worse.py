"""Test for the Worse and Worse strategy."""

import sys
import axelrod

from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestWorseAndWorse(TestPlayer):

    name = "Worse and worse"
    player = axelrod.WorseAndWorse
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(['length']),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """
        Test that the stratergy chooses to defect according to the correct
        probability.
        """
        if sys.version_info[0] == 2:
            # Python 2.x

            self.responses_test([], [], [D, C, C, D, D], random_seed=1,
            tournament_length=5)

            self.responses_test([], [], [C, C, D, D, C], random_seed=2,
            tournament_length=5)

        elif sys.version_info[0] == 3:
            # Python 3.x

            self.responses_test([], [], [C, C, D, D, D], random_seed=1,
            tournament_length=5)

            self.responses_test([], [], [D, D, D, D, D], random_seed=2,
            tournament_length=5)
