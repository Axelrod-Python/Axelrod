"""Tests for the Memorytwo strategies."""

import unittest
import warnings

import axelrod as axl
from axelrod.strategies.memorytwo import MemoryTwoPlayer

from .test_alternator import TestAlternator
from .test_cooperator import TestCooperator
from .test_defector import TestDefector
from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestMemoryTwoPlayer(unittest.TestCase):
    def test_default_if_four_vector_not_set(self):
        player = MemoryTwoPlayer()
        self.assertEqual(
            player._sixteen_vector,
            {
                ((C, C), (C, C)): 1.0,
                ((C, C), (C, D)): 1.0,
                ((C, D), (C, C)): 1.0,
                ((C, D), (C, D)): 1.0,
                ((C, C), (D, C)): 1.0,
                ((C, C), (D, D)): 1.0,
                ((C, D), (D, C)): 1.0,
                ((C, D), (D, D)): 1.0,
                ((D, C), (C, C)): 1.0,
                ((D, C), (C, D)): 1.0,
                ((D, D), (C, C)): 1.0,
                ((D, D), (C, D)): 1.0,
                ((D, C), (D, C)): 1.0,
                ((D, C), (D, D)): 1.0,
                ((D, D), (D, C)): 1.0,
                ((D, D), (D, D)): 1.0,
            },
        )

    def test_exception_if_four_vector_not_set(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            player = MemoryTwoPlayer()

            self.assertEqual(len(warning), 1)
            self.assertEqual(warning[-1].category, UserWarning)
            self.assertEqual(
                str(warning[-1].message),
                "Memory two player is set to default, Cooperator.",
            )

    def test_exception_if_probability_vector_outside_valid_values(self):
        player = MemoryTwoPlayer()
        x = 2
        with self.assertRaises(ValueError):
            player.set_sixteen_vector(
                [
                    0.1,
                    x,
                    0.5,
                    0.1,
                    0.1,
                    0.2,
                    0.5,
                    0.1,
                    0.1,
                    0.2,
                    0.5,
                    0.1,
                    0.2,
                    0.5,
                    0.1,
                    0.2,
                    0.5,
                    0.2,
                ]
            )


class TestMemoryStochastic(TestPlayer):
    name = "Generic Memory Two Player"
    player = axl.MemoryTwoPlayer
    expected_classifier = {
        "memory_depth": 0,  # Memory-two Sixteen-Vector
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        rng = axl.RandomGenerator(seed=7888)
        vector = [rng.random() for _ in range(16)]

        actions = [(C, C), (C, C), (D, D), (C, C), (D, C), (D, D), (D, C)]
        self.versus_test(
            opponent=axl.CyclerCCD(),
            expected_actions=actions,
            seed=0,
            init_kwargs={"sixteen_vector": vector},
        )

        actions = [(C, C), (C, C), (C, D), (C, C), (D, C), (D, D), (D, C)]
        self.versus_test(
            opponent=axl.CyclerCCD(),
            expected_actions=actions,
            seed=1,
            init_kwargs={"sixteen_vector": vector},
        )

        actions = [(C, C), (C, C), (D, C), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(
            opponent=axl.TitForTat(),
            expected_actions=actions,
            seed=0,
            init_kwargs={"sixteen_vector": vector},
        )

        actions = [(C, C), (C, C), (C, C), (D, C), (D, D), (D, D), (D, D)]
        self.versus_test(
            opponent=axl.TitForTat(),
            expected_actions=actions,
            seed=1,
            init_kwargs={"sixteen_vector": vector},
        )


class TestAON2(TestPlayer):

    name = "AON2"
    player = axl.AON2
    expected_classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # tests states 2, 7, 14 and 15
        actions = [(C, C), (C, D), (D, C), (D, D), (D, C), (D, D)]
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)

        # tests states 4, 16 and 11
        actions = [(C, D), (C, D), (D, C), (D, D), (D, D), (C, C), (C, D)]
        self.versus_test(opponent=axl.CyclerDDC(), expected_actions=actions)

        # tests states 3, 5 and 12
        actions = [(C, D), (C, C), (D, C), (D, D), (D, D), (C, D)]
        self.versus_test(
            opponent=axl.SuspiciousTitForTat(), expected_actions=actions
        )

        # tests state 1
        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        # tests state 6
        actions = [(C, D), (C, C), (D, D), (C, C)]
        self.versus_test(opponent=axl.CyclerDC(), expected_actions=actions)


class TestDelayedAON1(TestPlayer):

    name = "Delayed AON1"
    player = axl.DelayedAON1
    expected_classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy_mutually_cooperative(self):
        # tests states 2, 7, 14 and 11
        actions = [(C, C), (C, D), (D, C), (D, D), (C, C), (C, D)]
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)

        # tests states 1, 4 and 8
        actions = [(C, D), (C, D), (D, D), (C, C), (C, C), (C, D)]
        self.versus_test(
            opponent=axl.Cycler(["D", "D", "D", "C", "C"]),
            expected_actions=actions,
        )

        # tests states 3, 5
        actions = [(C, D), (C, C), (D, C), (D, D), (C, D)]
        self.versus_test(
            opponent=axl.SuspiciousTitForTat(), expected_actions=actions
        )


class TestMEM2(TestPlayer):

    name = "MEM2"
    player = axl.MEM2
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
        # Start with TFT
        actions = [(C, C), (C, C)]
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            attrs={"play_as": "TFT", "shift_counter": 1, "alld_counter": 0},
        )
        actions = [(C, D), (D, D)]
        self.versus_test(
            opponent=axl.Defector(),
            expected_actions=actions,
            attrs={"play_as": "TFT", "shift_counter": 1, "alld_counter": 0},
        )
        # TFTT if C, D and D, C
        opponent = axl.MockPlayer([D, C, D, D])
        actions = [(C, D), (D, C), (C, D), (C, D)]
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            attrs={"play_as": "TFTT", "shift_counter": 1, "alld_counter": 0},
        )

        opponent = axl.MockPlayer([D, C, D, D])
        actions = [
            (C, D),
            (D, C),
            (C, D),
            (C, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
        ]
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            attrs={"play_as": "ALLD", "shift_counter": -1, "alld_counter": 2},
        )


class TestMemoryTwoCooperator(TestCooperator):
    """Cooperator is equivalent to MemoryTwoPlayer((1, 1, ..., 1), C)"""

    name = "Generic Memory Two Player: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], (C, C)"
    player = lambda x: axl.MemoryTwoPlayer(
        sixteen_vector=[1] * 16, initial=(C, C)
    )
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMemoryTwoDefector(TestDefector):
    """Defector is equivalent to MemoryTwoPlayer((0, 0, ..., 0), D)"""

    name = "Generic Memory Two Player: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (D, D)"
    player = lambda x: axl.MemoryTwoPlayer(
        sixteen_vector=[0] * 16, initial=(D, D)
    )
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


def four_vector_to_sixteen_vector(four_vector):
    a, b, c, d = four_vector
    sixteen_vector = [a, b, a, b, d, c, d, c] * 2
    return sixteen_vector


class TestMemoryTwoAlternator(TestAlternator):
    """Alternator is equivalent to MemoryTwoPlayer(0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1), C)."""

    name = "Generic Memory Two Player: [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1], (C, D)"
    player = lambda x: axl.MemoryTwoPlayer(
        sixteen_vector=four_vector_to_sixteen_vector((0, 0, 1, 1)),
        initial=(C, D),
    )
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }
