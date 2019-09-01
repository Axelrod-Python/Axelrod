"""Tests for the ANN strategy."""
import unittest

import axelrod
from axelrod.load_data_ import load_weights
from axelrod.strategies.ann import split_weights
from .test_player import TestPlayer
from .test_evolvable_player import TestEvolvablePlayer


C, D = axelrod.Action.C, axelrod.Action.D
nn_weights = load_weights()
num_features, num_hidden, weights = nn_weights["Evolved ANN 5"]


class TestSplitWeights(unittest.TestCase):
    def test_split_weights(self):
        with self.assertRaises(ValueError):
            split_weights([0] * 20, 12, 10)
    # Doesn't Raise
    split_weights([0] * 70, 5, 10)
    split_weights([0] * 12, 10, 1)


class TestEvolvableANN(TestEvolvablePlayer):
    name = "EvolvableANN"
    player_class = axelrod.EvolvableANN
    init_parameters = {"num_features": 17, "num_hidden": 8}


class TestEvolvableANN2(TestEvolvablePlayer):
    name = "EvolvableANN"
    player_class = axelrod.EvolvableANN
    init_parameters = {
        "num_features": nn_weights["Evolved ANN 5"][0],
        "num_hidden": nn_weights["Evolved ANN 5"][1],
        "weights": nn_weights["Evolved ANN 5"][2]
    }


class TestEvolvedANN(TestPlayer):

    name = "Evolved ANN"
    player = axelrod.EvolvedANN
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C)] * 5
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D)] + [(D, D)] * 5
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        actions = [(C, C)] * 5
        self.versus_test(axelrod.TitForTat(), expected_actions=actions)


class TestEvolvedANN5(TestPlayer):

    name = "Evolved ANN 5"
    player = axelrod.EvolvedANN5
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C)] * 5
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D)] + [(D, D)] * 4
        self.versus_test(axelrod.Defector(), expected_actions=actions)


class TestEvolvedANNNoise05(TestPlayer):

    name = "Evolved ANN 5 Noise 05"
    player = axelrod.EvolvedANNNoise05
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C)] * 5
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)
