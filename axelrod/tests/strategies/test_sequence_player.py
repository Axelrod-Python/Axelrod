"""Tests for the Thue-Morse strategies."""

import unittest

import axelrod as axl
from axelrod._strategy_utils import recursive_thue_morse
from axelrod.strategies.sequence_player import SequencePlayer

from .test_player import TestOpponent, TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestThueMoreGenerator(unittest.TestCase):
    def test_sequence(self):
        expected = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
        for i, e in enumerate(expected):
            self.assertEqual(recursive_thue_morse(i), e)


class TestSequencePlayer(unittest.TestCase):
    def test_sequence_player(self):
        """Basic test for SequencePlayer."""

        def cooperate_gen():
            yield 1

        player = SequencePlayer(generator_function=cooperate_gen)
        opponent = TestOpponent()
        self.assertEqual(C, player.strategy(opponent))


class TestThueMorse(TestPlayer):

    name = "ThueMorse"
    player = axl.ThueMorse
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):

        thue_morse_seq = [D, C, C, D, C, D, D, C, C, D, D, C, D, C, C, D, C]
        n = len(thue_morse_seq)

        actions = list(zip(thue_morse_seq, [C] * n))
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        actions = list(zip(thue_morse_seq, [D] * n))
        self.versus_test(axl.Defector(), expected_actions=actions)


class TestThueMorseInverse(TestPlayer):

    name = "ThueMorseInverse"
    player = axl.ThueMorseInverse
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        inv_thue_morse_seq = [C, D, D, C, D, C, C, D, D, C, C, D, C, D, D, C, D]
        n = len(inv_thue_morse_seq)

        actions = list(zip(inv_thue_morse_seq, [C] * n))
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        actions = list(zip(inv_thue_morse_seq, [D] * n))
        self.versus_test(axl.Defector(), expected_actions=actions)
