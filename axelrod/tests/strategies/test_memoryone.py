"""Tests for the Memoryone strategies."""

import unittest
import warnings

import axelrod
from axelrod import Game
from axelrod.strategies.memoryone import MemoryOnePlayer

from .test_player import TestPlayer, test_four_vector

C, D = axelrod.Action.C, axelrod.Action.D


class TestGenericPlayerOne(unittest.TestCase):
    """A class to test the naming and classification of generic memory one
    players."""

    p1 = axelrod.MemoryOnePlayer(four_vector=(0, 0, 0, 0))
    p2 = axelrod.MemoryOnePlayer(four_vector=(1, 0, 1, 0))
    p3 = axelrod.MemoryOnePlayer(four_vector=(1, 0.5, 1, 0.5))

    def test_name(self):
        self.assertEqual(self.p1.name, "Generic Memory One Player: (0, 0, 0, 0)")
        self.assertEqual(self.p2.name, "Generic Memory One Player: (1, 0, 1, 0)")
        self.assertEqual(self.p3.name, "Generic Memory One Player: (1, 0.5, 1, 0.5)")

    def test_stochastic_classification(self):
        self.assertFalse(self.p1.classifier["stochastic"])
        self.assertFalse(self.p2.classifier["stochastic"])
        self.assertTrue(self.p3.classifier["stochastic"])


class TestWinStayLoseShift(TestPlayer):

    name = "Win-Stay Lose-Shift: C"
    player = axelrod.WinStayLoseShift
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_class_classification(self):
        self.assertEqual(self.player.classifier, self.expected_classifier)

    def test_strategy(self):
        # Check that switches if does not get best payoff.
        actions = [(C, C), (C, D), (D, C), (D, D), (C, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)


class TestWinShiftLoseStayTestPlayer(TestPlayer):

    name = "Win-Shift Lose-Stay: D"
    player = axelrod.WinShiftLoseStay
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Check that switches if does not get best payoff.
        actions = [(D, C), (C, D), (C, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions)


class TestGTFT(TestPlayer):

    name = "GTFT: 0.33"
    player = axelrod.GTFT
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(["game"]),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=0
        )

        actions = [(C, C), (C, D), (C, C), (C, D), (D, C)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=1
        )

    def test_four_vector(self):
        (R, P, S, T) = Game().RPST()
        p = min(1 - (T - R) / (R - S), (R - P) / (T - P))
        expected_dictionary = {(C, C): 1.0, (C, D): p, (D, C): 1.0, (D, D): p}
        test_four_vector(self, expected_dictionary)

    def test_allow_for_zero_probability(self):
        player = self.player(p=0)
        expected = {(C, C): 1.0, (C, D): 0, (D, C): 1.0, (D, D): 0}
        self.assertAlmostEqual(player._four_vector, expected)


class TestFirmButFair(TestPlayer):

    name = "Firm But Fair"
    player = axelrod.FirmButFair
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1, (C, D): 0, (D, C): 1, (D, D): 2 / 3}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):

        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)

        actions = [(C, D), (D, D), (D, D), (D, D), (C, D)]
        self.versus_test(opponent=axelrod.Defector(), expected_actions=actions, seed=0)

        actions = [(C, D), (D, D), (C, D), (D, D), (D, D)]
        self.versus_test(opponent=axelrod.Defector(), expected_actions=actions, seed=1)


class TestStochasticCooperator(TestPlayer):

    name = "Stochastic Cooperator"
    player = axelrod.StochasticCooperator
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_four_vector(self):
        expected_dictionary = {
            (C, C): 0.935,
            (C, D): 0.229,
            (D, C): 0.266,
            (D, D): 0.42,
        }
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (D, D), (C, C), (C, D), (C, C), (D, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=15
        )

        actions = [(C, C), (C, D), (D, C), (D, D), (C, C), (C, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=1
        )

        actions = [(C, C), (C, D), (D, C), (D, D), (D, C), (D, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=3
        )

        actions = [(C, C), (C, D), (D, C), (D, D), (D, C), (C, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=13
        )


class TestStochasticWSLS(TestPlayer):

    name = "Stochastic WSLS: 0.05"
    player = axelrod.StochasticWSLS
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (D, D), (C, C), (C, D), (D, C), (D, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=2
        )

        actions = [(C, C), (C, D), (D, C), (D, D), (C, C), (C, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=31
        )

        actions = [(C, D), (D, C), (D, D), (C, C), (C, D), (D, C)]
        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=2)

        actions = [(C, D), (C, C), (C, D), (D, C), (D, D), (C, C)]
        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=31)

    def test_four_vector(self):
        player = self.player()
        ep = player.ep
        expected_dictionary = {
            (C, C): 1.0 - ep,
            (C, D): ep,
            (D, C): ep,
            (D, D): 1.0 - ep,
        }
        test_four_vector(self, expected_dictionary)


class TestMemoryOnePlayer(unittest.TestCase):
    def test_default_if_four_vector_not_set(self):
        player = MemoryOnePlayer()
        self.assertEqual(
            player._four_vector, {(C, C): 1.0, (C, D): 0.0, (D, C): 0.0, (D, D): 1.0}
        )

    def test_exception_if_four_vector_not_set(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            player = MemoryOnePlayer()

            self.assertEqual(len(warning), 1)
            self.assertEqual(warning[-1].category, UserWarning)
            self.assertEqual(
                str(warning[-1].message),
                "Memory one player is set to default (1, 0, 0, 1).",
            )

    def test_exception_if_probability_vector_outside_valid_values(self):
        player = MemoryOnePlayer()
        x = 2.0
        with self.assertRaises(ValueError):
            player.set_four_vector([0.1, x, 0.5, 0.1])


class TestSoftJoss(TestPlayer):

    name = "Soft Joss: 0.9"
    player = axelrod.SoftJoss
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1, (C, D): 0.1, (D, C): 1.0, (D, D): 0.1}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=2
        )

        actions = [(C, D), (D, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(opponent=axelrod.CyclerDC(), expected_actions=actions, seed=5)


class TestALLCorALLD(TestPlayer):

    name = "ALLCorALLD"
    player = axelrod.ALLCorALLD
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(D, C)] * 10
        self.versus_test(
            opponent=axelrod.Cooperator(), expected_actions=actions, seed=0
        )
        actions = [(C, C)] * 10
        self.versus_test(
            opponent=axelrod.Cooperator(), expected_actions=actions, seed=1
        )


class TestGenericReactiveStrategy(unittest.TestCase):
    """
    Tests for the Reactive Strategy which.
    """

    p1 = axelrod.ReactivePlayer(probabilities=(0, 0))
    p2 = axelrod.ReactivePlayer(probabilities=(1, 0))
    p3 = axelrod.ReactivePlayer(probabilities=(1, 0.5))

    def test_name(self):
        self.assertEqual(self.p1.name, "Reactive Player: (0, 0)")
        self.assertEqual(self.p2.name, "Reactive Player: (1, 0)")
        self.assertEqual(self.p3.name, "Reactive Player: (1, 0.5)")

    def test_four_vector(self):
        self.assertEqual(
            self.p1._four_vector, {(C, D): 0.0, (D, C): 0.0, (C, C): 0.0, (D, D): 0.0}
        )
        self.assertEqual(
            self.p2._four_vector, {(C, D): 0.0, (D, C): 1.0, (C, C): 1.0, (D, D): 0.0}
        )
        self.assertEqual(
            self.p3._four_vector, {(C, D): 0.5, (D, C): 1.0, (C, C): 1.0, (D, D): 0.5}
        )

    def test_stochastic_classification(self):
        self.assertFalse(self.p1.classifier["stochastic"])
        self.assertFalse(self.p2.classifier["stochastic"])
        self.assertTrue(self.p3.classifier["stochastic"])

    def test_subclass(self):
        self.assertIsInstance(self.p1, MemoryOnePlayer)
        self.assertIsInstance(self.p2, MemoryOnePlayer)
        self.assertIsInstance(self.p3, MemoryOnePlayer)
