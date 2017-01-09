"""Tests for the Adaptive strategy."""
import unittest

import axelrod
from .test_player import TestHeadsUp, TestPlayer
from axelrod.strategies.ann import split_weights

C, D = axelrod.Actions.C, axelrod.Actions.D


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
        # Test initial play sequence
        self.first_play_test(C)


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
        # Test initial play sequence
        self.first_play_test(C)


class TestEvolvedANNNoise05(TestPlayer):

    name = "Evolved ANN 5 Noise 05"
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
        # Test initial play sequence
        self.first_play_test(C)


class TestEvolvedANNvsCooperator(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.EvolvedANN(), axelrod.Cooperator(),
                         C * 5, C * 5)


class TestEvolvedANNvsDefector(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.EvolvedANN(), axelrod.Defector(),
                         C * 2 + D * 3, D * 5)


class TestEvolvedANNvsTFT(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.EvolvedANN(), axelrod.TitForTat(),
                         C * 5, C * 5)


class TestEvolvedANN5vsCooperator(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.EvolvedANN5(), axelrod.Cooperator(),
                         C * 5, C * 5)


class TestEvolvedANN5vsDefector(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.EvolvedANN5(), axelrod.Defector(),
                         C * 5 + D, D * 6)


class TestEvolvedANNNoise05vsCooperator(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.EvolvedANNNoise05(), axelrod.Cooperator(),
                         C * 5, C * 5)


class TestEvolvedANNNoise05vsDefector(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.EvolvedANNNoise05(), axelrod.Defector(),
                         C * 10, D * 10)
