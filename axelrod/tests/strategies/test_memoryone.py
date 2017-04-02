"""Tests for the Memoryone strategies."""

import unittest

import axelrod
from axelrod import Game
from axelrod.strategies.memoryone import MemoryOnePlayer, LRPlayer
from .test_player import TestPlayer, test_four_vector

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGenericPlayerOne(unittest.TestCase):
    """A class to test the naming and classification of generic memory one
    players."""
    p1 = axelrod.MemoryOnePlayer(four_vector=(0, 0, 0, 0))
    p2 = axelrod.MemoryOnePlayer(four_vector=(1, 0, 1, 0))
    p3 = axelrod.MemoryOnePlayer(four_vector=(1, 0.5, 1, 0.5))

    def test_name(self):
        self.assertEqual(self.p1.name,
                         "Generic Memory One Player: (0, 0, 0, 0)")
        self.assertEqual(self.p2.name,
                         "Generic Memory One Player: (1, 0, 1, 0)")
        self.assertEqual(self.p3.name,
                         "Generic Memory One Player: (1, 0.5, 1, 0.5)")

    def test_stochastic_classification(self):
        self.assertFalse(self.p1.classifier['stochastic'])
        self.assertFalse(self.p2.classifier['stochastic'])
        self.assertTrue(self.p3.classifier['stochastic'])


class TestWinStayLoseShift(TestPlayer):

    name = "Win-Stay Lose-Shift: C"
    player = axelrod.WinStayLoseShift
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_class_classification(self):
        self.assertEqual(self.player.classifier,
                         self.expected_classifier)

    def test_strategy(self):
        # Starts by cooperating
        self.first_play_test(C)
        # Check that switches if does not get best payoff.
        self.second_play_test(C, D, D, C)


class TestWinShiftLoseStayTestPlayer(TestPlayer):

    name = "Win-Shift Lose-Stay: D"
    player = axelrod.WinShiftLoseStay
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by defecting.
        self.first_play_test(D)
        # Check that switches if does not get best payoff.
        self.second_play_test(D, C, C, D)


class TestGTFT(TestPlayer):

    name = "GTFT: 0.33"
    player = axelrod.GTFT
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)

    def test_four_vector(self):
        (R, P, S, T) = Game().RPST()
        p = min(1 - (T - R) / (R - S), (R - P) / (T - P))
        expected_dictionary = {(C, C): 1., (C, D): p, (D, C): 1., (D, D): p}
        test_four_vector(self, expected_dictionary)

    def test_allow_for_zero_probability(self):
        player = self.player(p=0)
        expected = {(C, C): 1., (C, D): 0, (D, C): 1., (D, D): 0}
        self.assertAlmostEqual(player._four_vector, expected)


class TestFirmButFair(TestPlayer):

    name = "Firm But Fair"
    player = axelrod.FirmButFair
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1, (C, D): 0, (D, C): 1, (D, D): 2/3}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)
        self.responses_test([C], [C], [C])
        self.responses_test([D], [C], [D])
        self.responses_test([C], [D], [C])
        self.responses_test([C], [D], [D], seed=1)
        self.responses_test([D], [D], [D], seed=2)


class TestStochasticCooperator(TestPlayer):

    name = "Stochastic Cooperator"
    player = axelrod.StochasticCooperator
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 0.935, (C, D): 0.229, (D, C): 0.266,
                               (D, D): 0.42}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)
        # With probability 0.065 will defect
        self.responses_test([D, C, C, C], [C], [C], seed=15)
        # With probability 0.266 will cooperate
        self.responses_test([C], [C], [D], seed=1)
        # With probability 0.42 will cooperate
        self.responses_test([C], [D], [C], seed=3)
        # With probability 0.229 will cooperate
        self.responses_test([C], [D], [D], seed=13)


class TestStochasticWSLS(TestPlayer):

    name = "Stochastic WSLS: 0.05"
    player = axelrod.StochasticWSLS
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        # With probability 0.05 will defect
        self.responses_test([D], [C], [C], seed=2)
        # With probability 0.05 will cooperate
        self.responses_test([C], [C], [D], seed=31)
        # With probability 0.05 will cooperate
        self.responses_test([C], [D], [C], seed=31)
        # With probability 0.05 will defect
        self.responses_test([D], [D], [D], seed=2)

    def test_four_vector(self):
        player = self.player()
        ep = player.ep
        expected_dictionary = {(C, C): 1. - ep, (C, D): ep, (D, C): ep,
                               (D, D): 1. - ep}
        test_four_vector(self, expected_dictionary)


class TestMemoryOnePlayer(unittest.TestCase):

    def test_exception_if_four_vector_not_set(self):
        player = MemoryOnePlayer()
        opponent = axelrod.Player()
        with self.assertRaises(ValueError):
            player.strategy(opponent)

    def test_exception_if_probability_vector_outside_valid_values(self):
        player = MemoryOnePlayer()
        x = 2.
        with self.assertRaises(ValueError):
            player.set_four_vector([0.1, x, 0.5, 0.1])


class TestLRPlayer(unittest.TestCase):

    def test_exception(self):
        player = LRPlayer()
        with self.assertRaises(ValueError):
            player.receive_match_attributes(0, 0, -float("inf"))


class TestZDExtort2(TestPlayer):

    name = "ZD-Extort-2: 0.1111111111111111, 0.5"
    player = axelrod.ZDExtort2
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 8/9, (C, D): 0.5, (D, C): 1/3,
                               (D, D): 0.}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)
        self.responses_test([D, D, C, C], [C], [C], seed=2)
        self.responses_test([D, D, C, C], [C], [D], seed=2)
        self.responses_test([D, D, C, C], [D], [C], seed=2)
        self.responses_test([D, D, C, C], [C], [D], seed=2)


class TestZDExtort2v2(TestPlayer):

    name = "ZD-Extort-2 v2: 0.125, 0.5, 1"
    player = axelrod.ZDExtort2v2
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 7/8, (C, D): 7/16, (D, C): 3/8,
                               (D, D): 0.}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)


class TestZDExtort4(TestPlayer):

    name = "ZD-Extort-4: 0.23529411764705882, 0.25, 1"
    player = axelrod.ZDExtort4
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 11/17, (C, D): 0, (D, C): 8/17,
                               (D, D): 0.}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)


class TestZDGen2(TestPlayer):

    name = "ZD-GEN-2: 0.125, 0.5, 3"
    player = axelrod.ZDGen2
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1, (C, D): 9/16, (D, C): 1/2,
                               (D, D): 1/8}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)


class TestZDGTFT2(TestPlayer):

    name = "ZD-GTFT-2: 0.25, 0.5"
    player = axelrod.ZDGTFT2
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1., (C, D): 1/8, (D, C): 1.,
                               (D, D): 0.25}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)
        self.responses_test([C, C, C, C], [C], [C], seed=2)
        self.responses_test([D], [C], [D], seed=2)
        self.responses_test([C, C, C, C], [D], [C], seed=2)
        self.responses_test([D], [D], [D], seed=2)


class TestZDSet2(TestPlayer):

    name = "ZD-SET-2: 0.25, 0.0, 2"
    player = axelrod.ZDSet2
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 3/4, (C, D): 1/4, (D, C): 1/2,
                               (D, D): 1/4}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)


class TestSoftJoss(TestPlayer):

    name = "Soft Joss: 0.9"
    player = axelrod.SoftJoss
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1, (C, D): 0.1, (D, C): 1., (D, D): 0.1}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.responses_test([C], [C], [C], seed=2)
        self.responses_test([D], [C], [D], seed=5)


class TestALLCorALLD(TestPlayer):

    name = "ALLCorALLD"
    player = axelrod.ALLCorALLD
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.responses_test([D] * 10, seed=2)
        self.responses_test([C] * 10, seed=3)
        self.responses_test([C] * 10, seed=4)
        self.responses_test([D] * 10, seed=5)
        self.responses_test([D] * 10, seed=6)
