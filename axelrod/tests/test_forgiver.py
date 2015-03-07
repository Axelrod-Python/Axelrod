"""Test for the forgiver strategies."""

import axelrod

from test_player import TestPlayer


class TestForgiver(TestPlayer):

    def test_initial_strategy(self):
        """Starts by cooperating."""
        P1 = axelrod.Forgiver()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_strategy(self):
        """If opponent has defected more than 10 percent of the time, defect."""
        P1 = axelrod.Forgiver()
        P2 = axelrod.Player()
        P1.history = ['C', 'C', 'C', 'C']
        P2.history = ['C', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'C', 'C', 'C', 'D']
        P2.history = ['C', 'C', 'C', 'D', 'C']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C']
        P2.history = ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'D']


class TestForgivingTitForTat(TestPlayer):

    def test_initial_strategy(self):
        """Starts by cooperating."""
        P1 = axelrod.ForgivingTitForTat()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_strategy(self):
        """If opponent has defected more than 10 percent of the time, defect."""
        P1 = axelrod.ForgivingTitForTat()
        P2 = axelrod.Player()
        P1.history = ['C', 'C', 'C', 'C']
        P2.history = ['C', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'C', 'C', 'C', 'D',]
        P2.history = ['C', 'C', 'C', 'D', 'C',]
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C']
        P2.history = ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'C', 'C', 'C']
        P2.history = ['C', 'C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'D')
