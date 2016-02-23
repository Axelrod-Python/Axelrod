"""Test for the Thue-Morse strategies."""
import unittest

import axelrod
from .test_player import TestPlayer, TestOpponent
from axelrod.strategies.sequence_player import recursive_thue_morse, SequencePlayer


C, D = axelrod.Actions.C, axelrod.Actions.D

class TestThueMoreGenerator(unittest.TestCase):
    def test_sequence(self):
        expected = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
        for i, e in enumerate(expected):
            self.assertEqual(recursive_thue_morse(i), e)


class TestSequencePlayer(unittest.TestCase):
    def test_sequence_player(self):
        """Basic test for SequencePlayer."""
        def cooperate_gen():
            yield C
        player = SequencePlayer(cooperate_gen)
        opponent = TestOpponent()
        self.assertEqual(C, player.strategy(opponent))


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
        self.first_play_test(D)
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
        self.first_play_test(C)
        self.markov_test([D, D, D, D])
        self.responses_test([], [], [C, D, D, C, D, C, C, D, D, C, C, D, C, D,
                                     D, C])
        self.responses_test([C], [C], [D, D, C, D, C, C, D, D, C, C, D, C, D, D,
                                       C])
        self.responses_test([D], [D], [D, D, C, D, C, C, D, D, C, C, D, C, D, D,
                                       C])
        self.responses_test([C, C, C, D], [C, C, C, D], [D, C, C, D, D, C, C, D,
                                                         C, D, D, C])
