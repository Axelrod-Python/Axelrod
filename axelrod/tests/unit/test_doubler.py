"""Test for the doubler strategy."""

import axelrod

from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestDoubler(TestPlayer):

    name = "Doubler"
    player = axelrod.Doubler
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating
        self.first_play_test(C)

        # Defects when the opponent has defected and
        # the opponent's cooperation count
        # is less than twice their defection count
        self.responses_test([C], [D], [D])
        self.responses_test([D, D], [D, D], [D])
        self.responses_test([C, D], [C, D], [D])
        self.responses_test([C, C, D], [C, C, D], [D])

        # Cooperates otherwise
        self.responses_test([C], [C], [C])
        self.responses_test([C, C, C, C], [C, C, C, D], [C])
