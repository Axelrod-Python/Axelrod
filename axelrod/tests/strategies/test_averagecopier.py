"""Tests for the AverageCopier strategies."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestAverageCopier(TestPlayer):

    name = "Average Copier"
    player = axl.AverageCopier
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Tests that if opponent has played all C then player chooses C.
        actions = [(C, C)] * 10
        self.versus_test(axl.Cooperator(), expected_actions=actions, seed=1)
        actions = [(D, C)] + [(C, C)] * 9
        self.versus_test(axl.Cooperator(), expected_actions=actions, seed=2)

        # Tests that if opponent has played all D then player chooses D.
        actions = [(C, D)] + [(D, D)] * 9
        self.versus_test(axl.Defector(), expected_actions=actions, seed=1)
        actions = [(D, D)] + [(D, D)] * 9
        self.versus_test(axl.Defector(), expected_actions=actions, seed=2)

        # Variable behaviour based on the history and stochastic

        actions = [
            (C, C),
            (C, D),
            (D, C),
            (D, D),
            (C, C),
            (C, D),
            (C, C),
            (D, D),
            (D, C),
            (C, D),
        ]
        self.versus_test(axl.Alternator(), expected_actions=actions, seed=1)

        actions = [
            (D, C),
            (C, D),
            (D, C),
            (C, D),
            (C, C),
            (D, D),
            (D, C),
            (D, D),
            (C, C),
            (D, D),
        ]
        self.versus_test(axl.Alternator(), expected_actions=actions, seed=2)

        opponent = axl.MockPlayer(actions=[C, C, D, D, D, D])
        actions = [
            (C, C),
            (C, C),
            (C, D),
            (D, D),
            (D, D),
            (C, D),
            (D, C),
            (D, C),
            (D, D),
            (D, D),
        ]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        opponent = axl.MockPlayer(actions=[C, C, C, D, D, D])
        actions = [
            (D, C),
            (C, C),
            (C, C),
            (C, D),
            (D, D),
            (C, D),
            (C, C),
            (D, C),
            (D, C),
            (D, D),
        ]
        self.versus_test(opponent, expected_actions=actions, seed=2)


class TestNiceAverageCopier(TestPlayer):

    name = "Nice Average Copier"
    player = axl.NiceAverageCopier
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Tests that if opponent has played all C then player chooses C.
        actions = [(C, C)] * 10
        self.versus_test(axl.Cooperator(), expected_actions=actions, seed=1)

        # Tests that if opponent has played all D then player chooses D.
        actions = [(C, D)] + [(D, D)] * 9
        self.versus_test(axl.Defector(), expected_actions=actions, seed=1)

        # Variable behaviour based on the history and stochastic behaviour
        actions = [
            (C, C),
            (C, D),
            (C, C),
            (D, D),
            (D, C),
            (C, D),
            (C, C),
            (C, D),
            (D, C),
            (D, D),
        ]
        self.versus_test(axl.Alternator(), expected_actions=actions, seed=1)

        actions = [
            (C, C),
            (C, D),
            (D, C),
            (D, D),
            (C, C),
            (C, D),
            (D, C),
            (D, D),
            (D, C),
            (C, D),
        ]
        self.versus_test(axl.Alternator(), expected_actions=actions, seed=2)

        opponent = axl.MockPlayer(actions=[C, C, D, D, D, D])
        actions = [
            (C, C),
            (C, C),
            (C, D),
            (C, D),
            (D, D),
            (D, D),
            (C, C),
            (D, C),
            (C, D),
            (D, D),
        ]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        opponent = axl.MockPlayer(actions=[C, C, C, D, D, D])
        actions = [
            (C, C),
            (C, C),
            (C, C),
            (C, D),
            (D, D),
            (D, D),
            (C, C),
            (C, C),
            (D, C),
            (D, D),
        ]
        self.versus_test(opponent, expected_actions=actions, seed=2)
