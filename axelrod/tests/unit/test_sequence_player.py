"""Test for the Thue-Morse strategies."""
import unittest

import axelrod
from .test_player import TestPlayer
from axelrod.strategies.thuemorse import recursive_thue_morse


C, D = axelrod.Actions.C, axelrod.Actions.D

class TestThueMoreGenerator(unittest.TestCase):
    def test_sequence(self):
        expected = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
        for i, e in enumerate(expected):
            self.assertEqual(recursive_thue_morse(i), e)


class TestThueMorse(TestPlayer):

    name = 'ThueMorse'
    player = axelrod.ThueMorse
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Test that strategy is randomly picked (not affected by history)."""
        self.first_play_test(D)

    def test_effect_of_strategy(self):
        self.markov_test([C, C, C, C])
        self.responses_test([], [], [D, C, C, D, C, D, D, C, C, D, D, C, D, C,
                                     C, D])
        self.responses_test([C], [C], [C, C, D, C, D, D, C, C, D, D, C, D, C, C,
                                       D])
        self.responses_test([D], [D], [C, C, D, C, D, D, C, C, D, D, C, D, C, C,
                                       D])
        self.responses_test([C, C, C, D], [C, C, C, D], [C, D, D, C, C, D, D, C,
                                                         D, C, C, D])


class TestThueMorseInverse(TestPlayer):

    name = 'ThueMorseInverse'
    player = axelrod.ThueMorseInverse
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Test that strategy always picks C first."""
        self.first_play_test(C)
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        self.markov_test([D, D, D, D])
        self.responses_test([], [], [C, D, D, C, D, C, C, D, D, C, C, D, C, D,
                                     D, C])
        self.responses_test([C], [C], [D, D, C, D, C, C, D, D, C, C, D, C, D, D,
                                       C])
        self.responses_test([D], [D], [D, D, C, D, C, C, D, D, C, C, D, C, D, D,
                                       C])
        self.responses_test([C, C, C, D], [C, C, C, D], [D, C, C, D, D, C, C, D,
                                                         C, D, D, C])
