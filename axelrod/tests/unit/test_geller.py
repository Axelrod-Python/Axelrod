"""Tests for the geller strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGeller(TestPlayer):

    name = "Geller"
    player = axelrod.Geller
    expected_classifier = {
        'memory_depth': -1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,  # Finds out what opponent will do
        'manipulates_state': False,
        'manipulates_source': False
    }

    def test_strategy(self):
        """Should cooperate against cooperators and defect against defectors."""
        player1 = self.player()
        player2 = axelrod.Cooperator()
        self.assertEqual(player1.strategy(player2), C)
        player1 = self.player()
        player2 = axelrod.Defector()
        self.assertEqual(player1.strategy(player2), D)


class TestGellerCooperator(TestGeller):

    name = "Geller Cooperator"
    player = axelrod.GellerCooperator
    expected_classifier = {
        'memory_depth': -1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,  # Finds out what opponent will do
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_against_self(self):
        player1 = self.player()
        player2 = self.player()
        self.assertEqual(player1.strategy(player2), C)


class TestGellerDefector(TestGeller):

    name = "Geller Defector"
    player = axelrod.GellerDefector
    expected_classifier = {
        'memory_depth': -1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,  # Finds out what opponent will do
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_against_self(self):
        player1 = self.player()
        player2 = self.player()
        self.assertEqual(player1.strategy(player2), D)
