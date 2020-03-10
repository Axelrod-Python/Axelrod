"""Tests for the Zero Determinant strategies."""

import unittest

import axelrod
from axelrod.game import DefaultGame
from axelrod.strategies.zero_determinant import LRPlayer

from .test_player import TestPlayer, test_four_vector

C, D = axelrod.Action.C, axelrod.Action.D


class TestLRPlayer(unittest.TestCase):
    def test_exception(self):
        with self.assertRaises(ValueError):
            LRPlayer(0, 0, -float("inf"))


class TestZDExtortion(TestPlayer):

    name = "ZD-Extortion: 0.2, 0.1, 1"
    player = axelrod.ZDExtortion
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(["game"]),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 0.64, (C, D): 0.18, (D, C): 0.28, (D, D): 0}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (D, D), (D, C), (D, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=3
        )

        actions = [(C, D), (D, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=6)


class TestZDExtort2(TestPlayer):

    name = "ZD-Extort-2: 0.1111111111111111, 0.5"
    player = axelrod.ZDExtort2
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(["game"]),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 8 / 9, (C, D): 0.5, (D, C): 1 / 3, (D, D): 0.0}
        test_four_vector(self, expected_dictionary)

    def test_receive_match_attributes(self):
        player = self.player()
        R, P, S, T = DefaultGame.RPST()
        self.assertEqual(player.l, P)

    def test_strategy(self):
        actions = [(C, C), (D, D), (D, C), (D, D), (D, C), (C, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=2
        )

        actions = [(C, C), (C, D), (C, C), (C, D), (D, C), (C, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=31
        )

        actions = [(C, D), (D, C), (D, D), (D, C), (C, D), (C, C)]
        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=2)

        actions = [(C, D), (C, C), (C, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=31)


class TestZDExtort2v2(TestPlayer):

    name = "ZD-Extort-2 v2: 0.125, 0.5, 1"
    player = axelrod.ZDExtort2v2
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(["game"]),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_four_vector(self):
        expected_dictionary = {
            (C, C): 7 / 8,
            (C, D): 7 / 16,
            (D, C): 3 / 8,
            (D, D): 0.0,
        }
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (D, D), (D, C), (D, D), (D, C), (C, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=2
        )

        actions = [(C, D), (D, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=5)


class TestZDExtort3(TestPlayer):
    name = "ZD-Extort3: 0.11538461538461539, 0.3333333333333333, 1"
    player = axelrod.ZDExtort3
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(["game"]),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_four_vector(self):
        expected_dictionary = {
            (C, C): 11 / 13,
            (C, D): 1 / 2,
            (D, C): 7 / 26,
            (D, D): 0,
        }
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (D, D), (D, C), (D, D)]

        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=3
        )

        actions = [(C, D), (D, C), (D, D), (D, C), (D, D), (D, C)]

        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=6)


class TestZDExtort4(TestPlayer):

    name = "ZD-Extort-4: 0.23529411764705882, 0.25, 1"
    player = axelrod.ZDExtort4
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(["game"]),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 11 / 17, (C, D): 0, (D, C): 8 / 17, (D, D): 0.0}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (D, D), (D, C), (D, D), (D, C), (C, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=2
        )

        actions = [(C, D), (D, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=5)


class TestZDGen2(TestPlayer):

    name = "ZD-GEN-2: 0.125, 0.5, 3"
    player = axelrod.ZDGen2
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(["game"]),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1, (C, D): 9 / 16, (D, C): 1 / 2, (D, D): 1 / 8}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):

        actions = [(C, C), (C, D), (D, C), (D, D), (C, C), (C, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=2
        )

        actions = [(C, C), (C, D), (C, C), (C, D), (C, C), (C, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=31
        )

        actions = [(C, D), (D, C), (D, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=2)

        actions = [(C, D), (C, C), (C, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=31)


class TestZDGTFT2(TestPlayer):

    name = "ZD-GTFT-2: 0.25, 0.5"
    player = axelrod.ZDGTFT2
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(["game"]),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1.0, (C, D): 1 / 8, (D, C): 1.0, (D, D): 0.25}
        test_four_vector(self, expected_dictionary)

    def test_receive_match_attributes(self):
        player = self.player()
        R, P, S, T = DefaultGame.RPST()
        self.assertEqual(player.l, R)

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=2
        )

        actions = [(C, C), (C, D), (C, C), (C, D), (C, C), (C, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=31
        )

        actions = [(C, D), (D, C), (C, D), (D, C), (C, D), (C, C)]
        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=2)

        actions = [(C, D), (C, C), (C, D), (C, C), (C, D), (D, C)]
        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=31)


class TestZDMischief(TestPlayer):

    name = "ZD-Mischief: 0.1, 0.0, 1"
    player = axelrod.ZDMischief
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(["game"]),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 0.8, (C, D): 0.6, (D, C): 0.1, (D, D): 0}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (D, D), (D, C), (D, D), (D, C), (C, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=2
        )

        actions = [(C, D), (D, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=5)


class TestZDSet2(TestPlayer):

    name = "ZD-SET-2: 0.25, 0.0, 2"
    player = axelrod.ZDSet2
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(["game"]),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_four_vector(self):
        expected_dictionary = {
            (C, C): 3 / 4,
            (C, D): 1 / 4,
            (D, C): 1 / 2,
            (D, D): 1 / 4,
        }
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (D, D), (D, C), (C, D), (C, C), (D, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=2
        )

        actions = [(C, D), (D, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=5)


class TestAdaptiveZeroDet(TestPlayer):
    """
    Test the AdaptiveZeroDet strategy.
    """

    name = "AdaptiveZeroDet: 0.125, 0.5, 3, C"
    player = axelrod.AdaptiveZeroDet
    expected_classifier = {
        "memory_depth": float('inf'),
        "stochastic": True,
        "makes_use_of": set(['game']),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (C, C), (C, D), (C, C)]
        self.versus_test(
            axelrod.Alternator(), expected_actions=actions
        )
