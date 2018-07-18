"""Tests for the ANN strategy."""
import unittest

import axelrod
from axelrod.strategies.ann import split_weights
from .test_player import TestMatch, TestPlayer


C, D = axelrod.Action.C, axelrod.Action.D


class TestSplitWeights(unittest.TestCase):
    def test_split_weights(self):
        with self.assertRaises(ValueError):
            split_weights([0] * 20, 12, 10)
    # Doesn't Raise
    split_weights([0] * 70, 5, 10)
    split_weights([0] * 12, 10, 1)


class TestEvolvedANN(TestPlayer):

    name = "Evolved ANN"
    player = axelrod.EvolvedANN
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
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        actions = [(C, C)] * 5
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D)] + [(D, D)] * 4
        self.versus_test(axelrod.Defector(), expected_actions=actions)


class TestEvolvedANNNoise05(TestPlayer):

    name = "Evolved ANN 10 Noise 05"
    player = axelrod.EvolvedANNNoise05
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
        actions = [(C, C)] * 5
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D), (C, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)
