"""Test for the tit for tat strategies."""

import axelrod

from test_player import TestPlayer


class TestTitForTat(TestPlayer):

    name = "Tit For Tat"
    player = axelrod.TitForTat

    def test_strategy(self):
        """Starts by cooperating."""
        P1 = axelrod.TitForTat()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """Repeats last action of opponent history."""
        P1 = axelrod.TitForTat()
        P2 = axelrod.Player()
        P2.history = ['C', 'C', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        P2.history = ['C', 'C', 'C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'D')


class TestTitFor2Tats(TestPlayer):

    name = 'Tit For 2 Tats'
    player = axelrod.TitFor2Tats

    def test_strategy(self):
        """Starts by cooperating."""
        P1 = axelrod.TitFor2Tats()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """Will defect only when last two turns of opponent were defections."""
        P1 = axelrod.TitFor2Tats()
        P2 = axelrod.Player()
        P1.history = ['C', 'C', 'C']
        P2.history = ['C', 'D', 'D']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['C', 'C', 'D', 'D']
        P2.history = ['D', 'D', 'D', 'C']
        self.assertEqual(P1.strategy(P2), 'C')


class TestTwoTitsForTat(TestPlayer):

    name = 'Two Tits For Tat'
    player = axelrod.TwoTitsForTat

    def test_strategy(self):
        """
        Starts by cooperating
        """
        P1 = axelrod.TwoTitsForTat()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """
        Will defect only when last two turns of opponent were defections.
        """
        P1 = axelrod.TwoTitsForTat()
        P2 = axelrod.Player()
        P1.history = ['C', 'C']
        P2.history = ['D', 'D']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['C', 'C', 'D']
        P2.history = ['D', 'D', 'C']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['C', 'C', 'D', 'D']
        P2.history = ['D', 'D', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')


class TestSuspiciousTitForTat(TestPlayer):

    name = "Suspicious Tit For Tat"
    player = axelrod.SuspiciousTitForTat

    def test_strategy(self):
        """Starts by defecting"""
        P1 = axelrod.SuspiciousTitForTat()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'D')

    def test_affect_of_strategy(self):
        """Will do opposite of what opponent does."""
        P1 = axelrod.SuspiciousTitForTat()
        P2 = axelrod.Player()
        P1.history = ['D']
        P2.history = ['C']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history.append('D')
        P2.history.append('D')
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history.append('C')
        P2.history.append('D')
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history.append('C')
        P2.history.append('C')
        self.assertEqual(P1.strategy(P2), 'D')


class TestSneakyTitForTat(TestPlayer):

    name = "Sneaky Tit For Tat"
    player = axelrod.SneakyTitForTat

    def test_strategy(self):
        """Starts by cooperating."""
        P1 = axelrod.SneakyTitForTat()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """Will try defecting after two turns of cooperation, but will stop if punished."""
        P1 = axelrod.SneakyTitForTat()
        P2 = axelrod.Player()
        P1.history = ['C', 'C']
        P2.history = ['C', 'C']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['C', 'C', 'D', 'D']
        P2.history = ['C', 'C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'C')