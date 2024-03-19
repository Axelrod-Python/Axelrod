"""Tests for the QLearner strategies."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestRiskyQLearner(TestPlayer):

    name = "Risky QLearner"
    player = axl.RiskyQLearner
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": {"game"},
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_payoff_matrix(self):
        (R, P, S, T) = axl.Game().RPST()
        payoff_matrix = {C: {C: R, D: S}, D: {C: T, D: P}}
        player = self.player()
        self.assertEqual(player.payoff_matrix, payoff_matrix)

    def test_strategy(self):
        actions = [(C, C), (D, C), (C, C), (C, C)]
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            seed=32,
            attrs={
                "Qs": {
                    "": {C: 0, D: 0.9},
                    "0.0": {C: 2.7, D: 0},
                    "C1.0": {C: 0, D: 4.5},
                    "CC2.0": {C: 2.7, D: 0},
                    "CCC3.0": {C: 0, D: 0},
                },
                "Vs": {
                    "": 0.9,
                    "0.0": 2.7,
                    "C1.0": 4.5,
                    "CC2.0": 2.7,
                    "CCC3.0": 0,
                },
                "prev_state": "CCC3.0",
            },
        )


class TestArrogantQLearner(TestPlayer):

    name = "Arrogant QLearner"
    player = axl.ArrogantQLearner
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "makes_use_of": {"game"},
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (D, C), (C, C), (C, C)]
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            seed=32,
            attrs={
                "Qs": {
                    "": {C: 0, D: 0.9},
                    "0.0": {C: 2.7, D: 0},
                    "C1.0": {C: 0, D: 4.5},
                    "CC2.0": {C: 2.7, D: 0},
                    "CCC3.0": {C: 0, D: 0},
                },
                "Vs": {
                    "": 0.9,
                    "0.0": 2.7,
                    "C1.0": 4.5,
                    "CC2.0": 2.7,
                    "CCC3.0": 0,
                },
                "prev_state": "CCC3.0",
            },
        )


class TestHesitantQLearner(TestPlayer):

    name = "Hesitant QLearner"
    player = axl.HesitantQLearner
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "makes_use_of": {"game"},
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, D), (D, D), (C, D), (C, D)]
        self.versus_test(
            opponent=axl.Defector(),
            expected_actions=actions,
            seed=32,
            attrs={
                "Qs": {
                    "": {C: 0, D: 0.1},
                    "0.0": {C: 0, D: 0},
                    "D0.0": {C: 0, D: 0.1},
                    "DD0.0": {C: 0, D: 0},
                    "DDD0.0": {C: 0, D: 0},
                },
                "Vs": {
                    "": 0.1,
                    "0.0": 0.0,
                    "D0.0": 0.1,
                    "DD0.0": 0.0,
                    "DDD0.0": 0,
                },
                "prev_state": "DDD0.0",
            },
        )


class TestCautiousQLearner(TestPlayer):

    name = "Cautious QLearner"
    player = axl.CautiousQLearner
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "makes_use_of": {"game"},
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, D), (D, D), (C, D), (C, D)]
        self.versus_test(
            opponent=axl.Defector(),
            expected_actions=actions,
            seed=32,
            attrs={
                "Qs": {
                    "": {C: 0, D: 0.1},
                    "0.0": {C: 0, D: 0},
                    "D0.0": {C: 0, D: 0.1},
                    "DD0.0": {C: 0, D: 0},
                    "DDD0.0": {C: 0, D: 0},
                },
                "Vs": {
                    "": 0.1,
                    "0.0": 0.0,
                    "D0.0": 0.1,
                    "DD0.0": 0.0,
                    "DDD0.0": 0,
                },
                "prev_state": "DDD0.0",
            },
        )
