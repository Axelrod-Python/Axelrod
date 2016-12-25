"""Test for the Adaptive strategy."""

import axelrod

from .test_player import TestHeadsUp, TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestEvolvedANN2(TestPlayer):

    name = "EvolvedANN2"
    player = axelrod.EvolvedANN2
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
        self.versus_test(axelrod.EvolvedANN2(), axelrod.Cooperator(),
                         [C, C, C, C, C], [C] * 5)


class TestEvolvedANNvsDefector(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.EvolvedANN2(), axelrod.Defector(),
                         [C, C, D, D, D], [D] * 5)

class TestEvolvedANNvsTFT(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.EvolvedANN2(), axelrod.TitForTat(),
                         [C] * 5, [C] * 5)
