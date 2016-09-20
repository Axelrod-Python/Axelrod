"""Test for the Worse and Worse strategy."""

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
        self.responses_test([], [], [C, C, D, D, D], random_seed=1,
        tournament_length=5)

        self.responses_test([], [], [D, D, D, D, D], random_seed=2,
        tournament_length=5)
