"""Tests for the Geller strategy."""

import axelrod
from .test_player import TestPlayer
from axelrod.random_ import seed

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

    def test_foil_strategy_inspection(self):
        seed(2)
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), D)
        self.assertEqual(player.foil_strategy_inspection(), D)
        self.assertEqual(player.foil_strategy_inspection(), C)

    def test_strategy(self):
        """Should cooperate against cooperators and defect against defectors."""
        P1 = self.player()
        P2 = axelrod.Cooperator()
        self.assertEqual(P1.strategy(P2), C)

        P1 = self.player()
        P2 = axelrod.Defector()
        self.assertEqual(P1.strategy(P2), D)


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

    def test_foil_strategy_inspection(self):
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), C)

    def test_against_self(self):
        P1 = self.player()
        P2 = self.player()
        self.assertEqual(P1.strategy(P2), C)


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

    def test_foil_strategy_inspection(self):
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), D)

    def test_against_self(self):
        P1 = self.player()
        P2 = self.player()
        self.assertEqual(P1.strategy(P2), D)
