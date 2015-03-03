"""Test for the defector strategy."""

import axelrod

from test_player import TestPlayer


class TestDefector(TestPlayer):

    name = "Defector"
    player = axelrod.Defector
    stoachastic = False

    def test_strategy(self):
        """Test that always defects."""

        P1 = axelrod.Defector()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['C', 'D', 'C']
        P2.history = ['C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'D')


class TestTrickyDefector(TestPlayer):

    name = "Tricky Defector"
    player = axelrod.TrickyDefector
    stochastic = False

    def test_strategy(self):
        """Test if it is trying to trick opponent."""
        P1 = axelrod.TrickyDefector()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['D', 'D', 'D', 'D']
        P2.history = ['C', 'D', 'D', 'D']
