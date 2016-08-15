"""Tests for strategies Desperate, Hopeless, Willing, and Grim"""
import axelrod

from axelrod.random_ import seed

from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D

class TestDesperate(TestPlayer):

    name = "Desperate"
    player = axelrod.Desperate
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        seed(1)
        self.first_play_test(C)

    def test_responses(self):
        self.responses_test([C] * 4, [D] * 4, [D])
        self.responses_test([D, D, C], [C, C, D], [D])
        self.responses_test([D, D, D], [C, C, D], [C])


class TestHopeless(TestPlayer):

    name = "Hopeless"
    player = axelrod.Hopeless
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        seed(1)
        self.first_play_test(C)

    def test_responses(self):
        self.responses_test([C] * 4, [D] * 4, [C])
        self.responses_test([D] * 5, [C] * 5, [C])
        self.responses_test([C, D, C], [C, C, C], [D])

class TestWilling(TestPlayer):

    name = "Willing"
    player = axelrod.Willing
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        seed(1)
        self.first_play_test(C)

    def test_responses(self):
        self.responses_test([C] * 4, [D] * 4, [C])
        self.responses_test([D] * 5, [C] * 5, [C])
        self.responses_test([C, C, D], [C, C, D], [D])
