"""Tests for strategies Desperate, Hopeless, Willing, and Grim."""
import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestDesperate(TestPlayer):

    name = "Desperate"
    player = axelrod.Desperate
    expected_classifier = {
        'memory_depth': 1,
        'long_run_time': False,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C, seed=1)
        self.first_play_test(D, seed=2)
        self.responses_test([D], [C] * 4, [D] * 4)
        self.responses_test([D], [D, D, C], [C, C, D])
        self.responses_test([C], [D, D, D], [C, C, D])


class TestHopeless(TestPlayer):

    name = "Hopeless"
    player = axelrod.Hopeless
    expected_classifier = {
        'memory_depth': 1,
        'long_run_time': False,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C, seed=1)
        self.first_play_test(D, seed=2)
        self.responses_test([C], [C] * 4, [D] * 4)
        self.responses_test([C], [D] * 5, [C] * 5)
        self.responses_test([D], [C, D, C], [C, C, C])


class TestWilling(TestPlayer):

    name = "Willing"
    player = axelrod.Willing
    expected_classifier = {
        'memory_depth': 1,
        'long_run_time': False,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C, seed=1)
        self.first_play_test(D, seed=2)
        self.responses_test([C], [C] * 4, [D] * 4)
        self.responses_test([C], [D] * 5, [C] * 5)
        self.responses_test([D], [C, C, D], [C, C, D])
