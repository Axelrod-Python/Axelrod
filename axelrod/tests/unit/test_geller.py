"""Test for the geller strategy."""

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
        'inspects_source': True,  # Finds out what opponent will do
        'manipulates_state': False,
        'manipulates_source': False
    }

    def test_strategy(self):
        """Should cooperate against cooperaters and defect against defectors."""

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
        'inspects_source': True,  # Finds out what opponent will do
        'manipulates_source': False,
        'manipulates_state': False
    }

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
        'inspects_source': True,  # Finds out what opponent will do
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_against_self(self):
        P1 = self.player()
        P2 = self.player()
        self.assertEqual(P1.strategy(P2), D)
