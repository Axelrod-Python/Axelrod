"""Test for the geller strategy."""

import axelrod

from .test_player import TestPlayer


class TestGeller(TestPlayer):

    name = "Geller"
    player = axelrod.Geller
    behaviour = {
        'stochastic': True,
        'memory_depth': -1,
        'inspects_opponent_source': False,
        'updates_opponent_source': False
    }

    def test_strategy(self):
        """Should cooperate against cooperaters and defect against defectors."""

        P1 = self.player()
        P2 = axelrod.Cooperator()
        self.assertEqual(P1.strategy(P2), 'C')

        P1 = self.player()
        P2 = axelrod.Defector()
        self.assertEqual(P1.strategy(P2), 'D')

class TestGellerCooperator(TestGeller):

    name = "Geller Cooperator"
    player = axelrod.GellerCooperator
    behaviour = {
        'stochastic': False,
        'memory_depth': -1,
        'inspects_opponent_source': False,
        'updates_opponent_source': False
    }

    def test_against_self(self):
        P1 = self.player()
        P2 = self.player()
        self.assertEqual(P1.strategy(P2), 'C')

class TestGellerDefector(TestGeller):

    name = "Geller Defector"
    player = axelrod.GellerDefector
    behaviour = {
        'stochastic': False,
        'memory_depth': -1,
        'inspects_opponent_source': False,
        'updates_opponent_source': False
    }

    def test_against_self(self):
        P1 = self.player()
        P2 = self.player()
        self.assertEqual(P1.strategy(P2), 'D')
