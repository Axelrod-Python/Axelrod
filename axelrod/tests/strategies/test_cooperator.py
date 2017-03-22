"""Tests for the Cooperator strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestCooperator(TestPlayer):

    name = "Cooperator"
    player = axelrod.Cooperator
    expected_classifier = {
        'memory_depth': 0,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Cooperates always.
        self.first_play_test(C)
        self.second_play_test(C, C, C, C)


class TestTrickyCooperator(TestPlayer):

    name = "Tricky Cooperator"
    player = axelrod.TrickyCooperator
    expected_classifier = {
        'memory_depth': 10,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating.
        self.first_play_test(C)
        # Test if it tries to trick opponent.
        self.versus_test(axelrod.Cooperator(), [(C, C), (C, C), (C, C), (D, C), (D, C)])

        opponent_actions = [C, C, C, C, D, D]
        expected_actions = [(C, C), (C, C), (C, C), (D, C), (D, D), (C, D)]
        self.versus_test(axelrod.MockPlayer(opponent_actions), expected_actions=expected_actions)

        opponent_actions = [C, C, C, C, D] + [D] + [C] * 10
        expected_actions = [(C, C), (C, C), (C, C), (D, C), (D, D), (C, D), (C, C), (C, C), (C, C), (C, C), (C, C),
                            (C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axelrod.MockPlayer(opponent_actions), expected_actions=expected_actions)

