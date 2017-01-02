"""Test for the Adaptive strategy."""
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

    name = "EvolvedANN"
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


class TestEvolvedANNvsCooperator(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.EvolvedANN(), axelrod.Cooperator(),
                         [C, C, C, C, C], [C] * 5)


class TestEvolvedANNvsDefector(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.EvolvedANN(), axelrod.Defector(),
                         [C, C, D, D, D], [D] * 5)

class TestEvolvedANNvsTFT(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.EvolvedANN(), axelrod.TitForTat(),
                         [C] * 5, [C] * 5)
