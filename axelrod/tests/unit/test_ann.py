"""Test for the Adaptive strategy."""

import axelrod

from .test_player import TestHeadsUp, TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestEvolvedANN(TestPlayer):

    name = "EvolvedANN"
    player = axelrod.EvolvedANN
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(["length"]),
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
                         [C, D, D, C, D], [C] * 5)
