"""Test for the memoryone strategies."""

import unittest

import axelrod
from axelrod import Game
from axelrod.strategies.memoryone import MemoryOnePlayer, LRPlayer
from .test_player import TestPlayer, test_four_vector

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestWinStayLoseShift(TestPlayer):

    name = "Win-Stay Lose-Shift"
    player = axelrod.WinStayLoseShift
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by cooperating"""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Check that switches if does not get best payoff."""
        self.markov_test([C, D, D, C])


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
        player = self.player()
        (R, P, S, T) = Game().RPST()
        p = min(1 - float(T - R) / (R - S), float(R - P) / (T - P))
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
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1, (C, D): 0, (D, C): 1, (D, D): 2./3}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)
        self.responses_test([C], [C], [C])
        self.responses_test([C], [D], [D])
        self.responses_test([D], [C], [C])
        self.responses_test([D], [D], [C], random_seed=1)
        self.responses_test([D], [D], [D], random_seed=2)

class TestStochasticCooperator(TestPlayer):

    name = "Stochastic Cooperator"
    player = axelrod.StochasticCooperator
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 0.935, (C, D): 0.229, (D, C): 0.266, (D, D): 0.42}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        # With probability 0.065 will defect
        self.responses_test([C], [C], [D, C, C, C], random_seed=15)
        # With probability 0.266 will cooperate
        self.responses_test([C], [D], [C], random_seed=1)
        # With probability 0.42 will cooperate
        self.responses_test([D], [C], [C], random_seed=3)
        # With probability 0.229 will cooperate
        self.responses_test([D], [D], [C], random_seed=13)


class TestStochasticWSLS(TestPlayer):

    name = "Stochastic WSLS"
    player = axelrod.StochasticWSLS
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)

    def test_four_vector(self):
        player = self.player()
        ep = player.ep
        expected_dictionary = {(C, C): 1.-ep, (C, D): ep, (D, C): ep, (D, D): 1.-ep}
        test_four_vector(self, expected_dictionary)

    def test_effect_of_strategy(self):
        # With probability 0.05 will defect
        self.responses_test([C], [C], [D], random_seed=2)
        # With probability 0.05 will cooperate
        self.responses_test([C], [D], [C], random_seed=31)
        # With probability 0.05 will cooperate
        self.responses_test([D], [C], [C], random_seed=31)
        # With probability 0.05 will defect
        self.responses_test([D], [D], [D], random_seed=2)


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
            player.receive_tournament_attributes(0, 0, -float("inf"))


class TestZDExtort2(TestPlayer):

    name = "ZD-Extort-2"
    player = axelrod.ZDExtort2
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 8./9, (C, D): 0.5, (D, C): 1./3,
                               (D, D): 0.}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        self.responses_test([C], [C], [D, D, C, C], random_seed=2)
        self.responses_test([C], [D], [D, D, D, C])
        self.responses_test([D], [C], [D, D, D, C])
        self.responses_test([D], [D], [D, D, D, D])


class TestZDExtort2v2(TestPlayer):

    name = "ZD-Extort-2 v2"
    player = axelrod.ZDExtort2v2
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 7./8, (C, D): 7./16, (D, C): 3./8,
                               (D, D): 0.}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)


class TestZDExtort4(TestPlayer):

    name = "ZD-Extort-4"
    player = axelrod.ZDExtort4
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 11./17, (C, D): 0, (D, C): 8./17,
                               (D, D): 0.}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)


class TestZDGen2(TestPlayer):

    name = "ZD-GEN-2"
    player = axelrod.ZDGen2
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1, (C, D): 9./16, (D, C): 1./2,
                               (D, D): 1./8}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)


class TestZDGTFT2(TestPlayer):

    name = "ZD-GTFT-2"
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
        expected_dictionary = {(C, C): 1., (C, D): 1./8, (D, C): 1.,
                               (D, D): 0.25}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        self.responses_test([C], [C], [C, C, C, C], random_seed=2)
        self.responses_test([C], [D], [D])
        self.responses_test([D], [C], [C, C, C, C])
        self.responses_test([D], [D], [D])


class TestZDSet2(TestPlayer):

    name = "ZD-SET-2"
    player = axelrod.ZDSet2
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 3./4, (C, D): 1./4, (D, C): 1./2,
                               (D, D): 1./4}
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
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1, (C, D): 0.1, (D, C): 1., (D, D): 0.1}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.responses_test([C], [C], [C], random_seed=2)
        self.responses_test([C], [D], [D], random_seed=5)


class TestALLCorALLD(TestPlayer):

    name = "ALLCorALLD"
    player = axelrod.ALLCorALLD
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.responses_test([], [], [D] * 10, random_seed=2)
        self.responses_test([], [], [C] * 10, random_seed=3)
        self.responses_test([], [], [C] * 10, random_seed=4)
        self.responses_test([], [], [D] * 10, random_seed=5)
        self.responses_test([], [], [D] * 10, random_seed=6)
