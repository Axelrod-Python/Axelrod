"""Tests for the hunter strategy."""

import random

import axelrod

from test_player import TestPlayer

C, D = 'C', 'D'


class TestDefectorHunter(TestPlayer):

    name = "Defector Hunter"
    player = axelrod.DefectorHunter
    stochastic = False

    def test_strategy(self):
        self.first_play_test(C)
        for i in range(3):
            self.responses_test([C]*i, [D]*i, [C])
        self.responses_test([C]*4, [D]*4, [D])

class TestCooperatorHunter(TestPlayer):

    name = "Cooperator Hunter"
    player = axelrod.CooperatorHunter
    stochastic = False

    def test_strategy(self):
        self.first_play_test(C)
        for i in range(3):
            self.responses_test([C]*i, [C]*i, [C])
        self.responses_test([C]*4, [C]*4, [D])

class TestAlternatorHunter(TestPlayer):

    name = "Alternator Hunter"
    player = axelrod.AlternatorHunter
    stochastic = False

    def test_strategy(self):
        self.first_play_test(C)
        self.responses_test([C, C], [C, D], [C])
        self.responses_test([C, C, C], [C, D, C], [C])
        self.responses_test([C, C, C, C], [C, D, C, D], [D])
        self.responses_test([C, C, C, C, C], [C, D, C, D, C], [D])

class TestMathConstantHunter(TestPlayer):

    name = "Math Constant Hunter"
    player = axelrod.MathConstantHunter
    stochastic = False

    def test_strategy(self):
        self.responses_test([C]*8, [C, C, C, D, C, C, C, D], [D])

class TestRandomHunter(TestPlayer):

    name = "Random Hunter"
    player = axelrod.RandomHunter
    stochastic = False

    def test_strategy(self):
        P1 = axelrod.RandomHunter()
        P2 = axelrod.Player()
        P1.history = [C] * 8
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
        self.first_play_test(C)
        # We are not using the Cooperator Hunter here, so this should lead to cooperation.
        self.responses_test([C, C, C, C], [C, C, C, C], [C])
        # All these others, however, should trigger a defection for the hunter.
        self.responses_test([C, C, C, C], [D, D, D, D], [D])
        self.responses_test([C, C, C, C], [C, D, C, D], [D])
        self.responses_test([C]*8, [C, C, C, D, C, C, C, D], [D])
        self.responses_test([C]*8, [random.choice([C, D]) for i in range(8)],[D])

