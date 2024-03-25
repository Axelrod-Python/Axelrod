"""Tests for the Memoryone strategies."""

import unittest
import warnings

import axelrod as axl
from axelrod.strategies.memoryone import MemoryOnePlayer

from .test_alternator import TestAlternator
from .test_cooperator import TestCooperator
from .test_defector import TestDefector
from .test_player import TestPlayer, test_four_vector
from .test_titfortat import TestTitForTat

C, D = axl.Action.C, axl.Action.D


class TestWinStayLoseShift(TestPlayer):

    name = "Win-Stay Lose-Shift"
    player = axl.WinStayLoseShift
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
        # Check that player switches if does not get best payoff.
        actions = [(C, C), (C, D), (D, C), (D, D), (C, C)]
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)


class TestWinShiftLoseStayTestPlayer(TestPlayer):

    name = "Win-Shift Lose-Stay: D"
    player = axl.WinShiftLoseStay
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
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)


class TestGTFT(TestPlayer):

    name = "GTFT: 0.33"
    player = axl.GTFT
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": {"game"},
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(
            opponent=axl.Alternator(), expected_actions=actions, seed=2
        )

    def test_strategy2(self):
        actions = [(C, C), (C, D), (C, C), (C, D), (D, C)]
        self.versus_test(
            opponent=axl.Alternator(), expected_actions=actions, seed=1
        )

    def test_four_vector(self):
        (R, P, S, T) = axl.Game().RPST()
        p = min(1 - (T - R) / (R - S), (R - P) / (T - P))
        expected_dictionary = {(C, C): 1.0, (C, D): p, (D, C): 1.0, (D, D): p}
        test_four_vector(self, expected_dictionary)

    def test_allow_for_zero_probability(self):
        player = self.player(p=0)
        expected = {(C, C): 1.0, (C, D): 0, (D, C): 1.0, (D, D): 0}
        self.assertAlmostEqual(player._four_vector, expected)


class TestFirmButFair(TestPlayer):

    name = "Firm But Fair"
    player = axl.FirmButFair
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
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)

    def test_strategy2(self):
        actions = [(C, D), (D, D), (D, D), (D, D), (C, D)]
        self.versus_test(
            opponent=axl.Defector(), expected_actions=actions, seed=10
        )

    def test_strategy3(self):
        actions = [(C, D), (D, D), (C, D), (D, D), (D, D)]
        self.versus_test(
            opponent=axl.Defector(), expected_actions=actions, seed=1
        )


class TestStochasticCooperator(TestPlayer):

    name = "Stochastic Cooperator"
    player = axl.StochasticCooperator
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
            opponent=axl.Alternator(), expected_actions=actions, seed=113
        )

    def test_strategy2(self):
        actions = [(C, C), (C, D), (D, C), (D, D), (C, C), (C, D)]
        self.versus_test(
            opponent=axl.Alternator(), expected_actions=actions, seed=1
        )

    def test_strategy3(self):
        actions = [(C, C), (C, D), (D, C), (D, D), (D, C), (D, D)]
        self.versus_test(
            opponent=axl.Alternator(), expected_actions=actions, seed=5
        )

    def test_strategy4(self):
        actions = [(C, C), (C, D), (D, C), (D, D), (D, C), (C, D)]
        self.versus_test(
            opponent=axl.Alternator(), expected_actions=actions, seed=12
        )


class TestStochasticWSLS(TestPlayer):

    name = "Stochastic WSLS: 0.05"
    player = axl.StochasticWSLS
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
            opponent=axl.Alternator(), expected_actions=actions, seed=50
        )

    def test_strategy2(self):
        actions = [(C, C), (C, D), (D, C), (D, D), (C, C), (C, D)]
        self.versus_test(
            opponent=axl.Alternator(), expected_actions=actions, seed=1
        )

    def test_strategy3(self):
        actions = [(C, D), (D, C), (D, D), (C, C), (C, D), (D, C)]
        self.versus_test(
            opponent=axl.CyclerDC(), expected_actions=actions, seed=2
        )

    def test_strategy4(self):
        actions = [(C, D), (C, C), (C, D), (D, C), (D, D), (C, C)]
        self.versus_test(
            opponent=axl.CyclerDC(), expected_actions=actions, seed=23
        )

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
            player._four_vector,
            {(C, C): 1.0, (C, D): 0.0, (D, C): 0.0, (D, D): 1.0},
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
    player = axl.SoftJoss
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
            opponent=axl.Alternator(), expected_actions=actions, seed=2
        )

    def test_strategy2(self):
        actions = [(C, D), (D, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(
            opponent=axl.CyclerDC(), expected_actions=actions, seed=5
        )


class TestALLCorALLD(TestPlayer):

    name = "ALLCorALLD"
    player = axl.ALLCorALLD
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
            opponent=axl.Cooperator(), expected_actions=actions, seed=0
        )

    def test_strategy2(self):
        actions = [(C, C)] * 10
        self.versus_test(
            opponent=axl.Cooperator(), expected_actions=actions, seed=1
        )


class TestGenericReactiveStrategy(unittest.TestCase):
    """
    Tests for the Reactive Strategy which.
    """

    p1 = axl.ReactivePlayer(probabilities=(0, 0))
    p2 = axl.ReactivePlayer(probabilities=(1, 0))
    p3 = axl.ReactivePlayer(probabilities=(1, 0.5))

    def test_four_vector(self):
        self.assertEqual(
            self.p1._four_vector,
            {(C, D): 0.0, (D, C): 0.0, (C, C): 0.0, (D, D): 0.0},
        )
        self.assertEqual(
            self.p2._four_vector,
            {(C, D): 0.0, (D, C): 1.0, (C, C): 1.0, (D, D): 0.0},
        )
        self.assertEqual(
            self.p3._four_vector,
            {(C, D): 0.5, (D, C): 1.0, (C, C): 1.0, (D, D): 0.5},
        )

    def test_subclass(self):
        self.assertIsInstance(self.p1, MemoryOnePlayer)
        self.assertIsInstance(self.p2, MemoryOnePlayer)
        self.assertIsInstance(self.p3, MemoryOnePlayer)


class TestMemoryOneAlternator(TestAlternator):
    """Alternator is equivalent to MemoryOnePlayer((0, 0, 1, 1), C)"""

    name = "Generic Memory One Player: (0, 0, 1, 1), C"
    player = lambda x: axl.MemoryOnePlayer(four_vector=(0, 0, 1, 1))
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMemoryOneCooperator(TestCooperator):
    """Cooperator is equivalent to MemoryOnePlayer((1, 1, 1, 1), C)"""

    name = "Generic Memory One Player: (1, 1, 1, 1), C"
    player = lambda x: axl.MemoryOnePlayer(four_vector=(1, 1, 1, 1))
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMemoryOneDefector(TestDefector):
    """Defector is equivalent to MemoryOnePlayer((0, 0, 0, 0), D)"""

    name = "Generic Memory One Player: (0, 0, 0, 0), D"
    player = lambda x: axl.MemoryOnePlayer(four_vector=(0, 0, 0, 0), initial=D)
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMemoryOneTitForTat(TestTitForTat):
    """TitForTat is equivalent to MemoryOnePlayer((1, 0, 1, 0), C)"""

    name = "Generic Memory One Player: (1, 0, 1, 0), C"
    player = lambda x: axl.MemoryOnePlayer(four_vector=(1, 0, 1, 0))
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMemoryOneWSLS(TestWinStayLoseShift):
    """WinStayLoseShift is equivalent to MemoryOnePlayer((1, 0, 0, 1), C)"""

    name = "Generic Memory One Player: (1, 0, 0, 1), C"
    player = lambda x: axl.MemoryOnePlayer(four_vector=(1, 0, 0, 1))
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }
