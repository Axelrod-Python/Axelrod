"""Tests for the Thue-Morse strategies."""
import unittest

import axelrod
from .test_player import TestPlayer, TestOpponent
from axelrod.strategies.sequence_player import SequencePlayer
from axelrod._strategy_utils import recursive_thue_morse


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
        player = SequencePlayer(generator_function=cooperate_gen)
        opponent = TestOpponent()
        self.assertEqual(C, player.strategy(opponent))


class TestThueMorse(TestPlayer):

    name = 'ThueMorse'
    player = axelrod.ThueMorse
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):

        thue_morse_seq = [D, C, C, D, C, D, D, C, C, D, D, C, D, C, C, D, C]
        n = len(thue_morse_seq)

        actions = list(zip(thue_morse_seq, [C] * n))
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = list(zip(thue_morse_seq, [D] * n))
        self.versus_test(axelrod.Defector(), expected_actions=actions)


class TestThueMorseInverse(TestPlayer):

    name = 'ThueMorseInverse'
    player = axelrod.ThueMorseInverse
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):

        inv_thue_morse_seq = [C, D, D, C, D, C, C, D, D, C, C, D, C, D, D, C, D]
        n = len(inv_thue_morse_seq)

        actions = list(zip(inv_thue_morse_seq, [C] * n))
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = list(zip(inv_thue_morse_seq, [D] * n))
        self.versus_test(axelrod.Defector(), expected_actions=actions)
