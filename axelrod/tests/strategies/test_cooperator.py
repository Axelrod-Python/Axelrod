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

        opponent_actions = [C, C, C, C] + [D, D] + [C] * 10
        expected_actions = [(C, C), (C, C), (C, C), (D, C)] + [(D, D), (C, D)] + [(C, C)] * 10
        self.versus_test(axelrod.MockPlayer(opponent_actions), expected_actions=expected_actions)

    def test_defects_if_last_ten_has_no_D_and_last_three_are_C(self):
        """according to doc string on strategy"""
        opponent_actions = [D] + [C] * 7 + [C] * 3 + [C]
        actions = [(C, D)] + [(C, C)] * 7 + [(C, C)] * 3 + [(D, C)]
        self.versus_test(axelrod.MockPlayer(opponent_actions), actions)

    def test_cooperates_if_last_ten_has_D(self):
        """according to doc string on strategy"""
        opponent_actions = [D] + [C] * 6 + [C] * 3 + [C]
        actions = [(C, D)] + [(C, C)] * 6 + [(C, C)] * 3 + [(C, C)]
        self.versus_test(axelrod.MockPlayer(opponent_actions), actions)

    def test_cooperates_if_last_three_are_not_C(self):
        """according to doc string on strategy"""
        opponent_actions = [D] + [C] * 7 + [C, D, C] + [C]
        actions = [(C, D)] + [(C, C)] * 7 + [(C, C), (C, D), (C, C)] + [(C, C)]
        self.versus_test(axelrod.MockPlayer(opponent_actions), actions)

    def test_cooperates_in_first_three_rounds(self):
        """according to code meaning"""
        against_defector = [(C, D)] * 3
        against_cooperator = [(C, C)] * 3
        against_alternator = [(C, C), (C, D), (C, C)]
        self.versus_test(axelrod.Defector(), against_defector)
        self.versus_test(axelrod.Cooperator(), against_cooperator)
        self.versus_test(axelrod.Alternator(), against_alternator)

    def test_defects_after_three_rounds_if_opponent_only_cooperated_in_max_history_depth_ten(self):
        """according to code meaning"""
        against_cooperator = [(C, C)] * 3 + [(D, C)] * 20
        self.versus_test(axelrod.Cooperator(), against_cooperator)

    def test_defects_when_opponent_has_no_defections_to_history_depth_ten(self):
        """according to code meaning"""
        opponent_actions = [D] + [C] * 10 + [D, C]
        expected_actions = [(C, D)] + [(C, C)] * 10 + [(D, D), (C, C)]
        self.versus_test(axelrod.MockPlayer(opponent_actions), expected_actions)
