"""Tests for the hunter strategy."""

import random

import axelrod

from .test_player import TestPlayer

C, D = 'C', 'D'


class TestDefectorHunter(TestPlayer):

    name = "Defector Hunter"
    player = axelrod.DefectorHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        for i in range(3):
            self.responses_test([C] * i, [D] * i, [C])
        self.responses_test([C] * 4, [D] * 4, [D])

class TestCooperatorHunter(TestPlayer):

    name = "Cooperator Hunter"
    player = axelrod.CooperatorHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        for i in range(3):
            self.responses_test([C] * i, [C] * i, [C])
        self.responses_test([C] * 4, [C] * 4, [D])

class TestAlternatorHunter(TestPlayer):

    name = "Alternator Hunter"
    player = axelrod.AlternatorHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        self.responses_test([C] * 2, [C, D], [C])
        self.responses_test([C] * 3, [C, D, C], [C])
        self.responses_test([C] * 4, [C, D] * 2, [C])
        self.responses_test([C] * 5, [C, D] * 2 + [C], [C])
        self.responses_test([C] * 6, [C, D] * 3, [D])
        self.responses_test([C] * 7, [C, D] * 3 + [C], [D])

class TestMathConstantHunter(TestPlayer):

    name = "Math Constant Hunter"
    player = axelrod.MathConstantHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.responses_test([C] * 8, [C] * 7 + [D], [D])

class TestRandomHunter(TestPlayer):

    name = "Random Hunter"
    player = axelrod.RandomHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):

        P1 = axelrod.RandomHunter()
        P2 = axelrod.Player()

        # We should also catch the alternator here.
        self.responses_test([C] * 12, [C, D] * 6, [D])

        # It is still possible for this test to fail, but very unlikely.
        P1.history = [C] * 100
        P2.history = [random.choice([C, D]) for i in range(100)]
        self.assertEqual(P1.strategy(P2), D)

class TestMetaHunter(TestPlayer):

    name = "Meta Hunter"
    player = axelrod.MetaHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)

        # We are not using the Cooperator Hunter here, so this should lead to cooperation.
        self.responses_test([C, C, C, C], [C, C, C, C], [C])

        # After long histories tit-for-tat should come into play.
        self.responses_test([C] * 101, [C] * 100 + [D], [D])

        # All these others, however, should trigger a defection for the hunter.
        self.responses_test([C] * 4, [D] * 4, [D])
        self.responses_test([C] * 6, [C, D] * 3, [D])
        self.responses_test([C] * 8, [C, C, C, D, C, C, C, D], [D])
        self.responses_test([C] * 100, [random.choice([C, D]) for i in range(100)],[D])
