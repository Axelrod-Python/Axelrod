"""Tests for the hunter strategy."""

import random

import axelrod

from test_player import TestPlayer


class TestDefectorHunter(TestPlayer):

    name = "Defector Hunter"
    player = axelrod.DefectorHunter
    stochastic = False

    def test_strategy(self):

        P1 = axelrod.DefectorHunter()
        P2 = axelrod.Player()
        for i in range(4):
            self.assertEqual(P1.strategy(P2), 'C')
            P1.history.append('C')
            P2.history.append('D')
        self.assertEqual(P1.strategy(P2), 'D')

class TestCooperatorHunter(TestPlayer):

    name = "Cooperator Hunter"
    player = axelrod.CooperatorHunter
    stochastic = False

    def test_strategy(self):

        P1 = axelrod.CooperatorHunter()
        P2 = axelrod.Player()
        for i in range(4):
            self.assertEqual(P1.strategy(P2), 'C')
            P1.history.append('C')
            P2.history.append('C')
        self.assertEqual(P1.strategy(P2), 'D')

class TestAlternatorHunter(TestPlayer):

    name = "Alternator Hunter"
    player = axelrod.AlternatorHunter
    stochastic = False

    def test_strategy(self):

        P1 = axelrod.AlternatorHunter()
        P2 = axelrod.Player()
        for i in range(4):
            self.assertEqual(P1.strategy(P2), 'C')
            P1.history.append('C')
            P2.history.append('C'*(i%2==0) or 'D')
        self.assertEqual(P1.strategy(P2), 'D')

class TestMathConstantHunter(TestPlayer):

    name = "Math Constant Hunter"
    player = axelrod.MathConstantHunter
    stochastic = False

    def test_strategy(self):

        P1 = axelrod.MathConstantHunter()
        P2 = axelrod.Player()
        P1.history = ['C'] * 8
        P2.history = ['C', 'C', 'C', 'D', 'C', 'C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'D')

class TestRandomHunter(TestPlayer):

    name = "Random Hunter"
    player = axelrod.RandomHunter
    stochastic = False

    def test_strategy(self):

        P1 = axelrod.RandomHunter()
        P2 = axelrod.Player()
        P1.history = ['C'] * 8
        P2.history = [random.choice(['C', 'D']) for i in range(8)]
        for i in range(10):
            self.assertEqual(P1.strategy(P2), 'D')
            P1.history.append('D')
            P2.history.append(random.choice(['C', 'D']))

class TestMetaHunter(TestPlayer):

    name = "Meta Hunter"
    player = axelrod.MetaHunter
    stochastic = False

    def test_strategy(self):

        P1 = axelrod.MetaHunter()
        P2 = axelrod.Player()

        self.assertEqual(P1.strategy(P2), 'C')

        # We are not using the Cooperator Hunter here, so this should lead to cooperation.
        P1.history = ['C'] * 4
        P2.history = ['C'] * 4
        self.assertEqual(P1.strategy(P2), 'C')

        # All these others, however, should trigger a defection for the hunter.
        histories = [
            ['D'] * 4,
            ['C', 'D'] * 2,
            ['C', 'C', 'C', 'D', 'C', 'C', 'C', 'D'],
            [random.choice(['C', 'D']) for i in range(8)],
        ]
        for h in histories:
            P1.history = ['C'] * len(h)
            P2.history = h
            self.assertEqual(P1.strategy(P2), 'D')
