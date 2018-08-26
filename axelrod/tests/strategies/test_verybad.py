"""Tests for the VeryBad strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D


class TestVeryBad(TestPlayer):

    name = "VeryBad"
    player = axelrod.VeryBad
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # axelrod.Defector -
        #   cooperates for the first three, defects for the rest P(C) < .5
        self.versus_test(
            axelrod.Defector(), expected_actions=([(C, D)] * 3 + [(D, D)] * 7)
        )

        # axelrod.Cooperator -
        #   cooperate for all, P(C) == 1
        self.versus_test(axelrod.Cooperator(), expected_actions=[(C, C)])

        expected_actions = [
            (C, C),  # first three cooperate
            (C, D),
            (C, D),
            (D, C),  # P(C) = .33
            (C, C),  # P(C) = .5 (last move C)
            (C, D),  # P(C) = .6
            (D, D),  # P(C) = .5 (last move D)
            (D, D),  # P(C) = .43
            (D, C),  # P(C) = .375
            (D, D),  # P(C) = .4
        ]
        mock_player = axelrod.MockPlayer(actions=[a[1] for a in expected_actions])
        self.versus_test(mock_player, expected_actions=expected_actions)
