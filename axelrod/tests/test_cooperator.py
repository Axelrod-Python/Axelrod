"""Test for the cooperator strategy."""

import axelrod

from test_player import TestPlayer


class TestCooperator(TestPlayer):

    name = "Cooperator"
    player = axelrod.Cooperator
    stochastic = False

    def test_strategy(self):
        """Test that always cooperates."""
        P1 = axelrod.Cooperator()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'D', 'C']
        P2.history = ['C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'C')


class TestTrickyCooperator(TestPlayer):

    name = "Tricky Cooperator"
    player = axelrod.TrickyCooperator
    stochastic = False

    def test_strategy(self):
        """Test if it tries to trick opponent"""
        P1 = axelrod.TrickyCooperator()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'C', 'C']
        P2.history = ['C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history.extend(['D', 'D'])
        P2.history.extend(['C', 'D'])
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history.extend(['C']*11)
        P2.history.extend(['D'] + ['C']*10)
        self.assertEqual(P1.strategy(P2), 'D')
