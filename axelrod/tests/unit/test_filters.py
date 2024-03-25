import unittest

from hypothesis import example, given, settings
from hypothesis.strategies import integers

import axelrod as axl
from axelrod.player import Player
from axelrod.strategies._filters import *


class TestFilters(unittest.TestCase):
    class TestStrategy(Player):
        classifier = {
            "stochastic": True,
            "inspects_source": False,
            "memory_depth": 10,
            "makes_use_of": ["game", "length"],
        }

    def test_equality_filter(self):
        self.assertTrue(
            passes_operator_filter(
                self.TestStrategy, "stochastic", True, operator.eq
            )
        )
        self.assertFalse(
            passes_operator_filter(
                self.TestStrategy, "stochastic", False, operator.eq
            )
        )
        self.assertTrue(
            passes_operator_filter(
                self.TestStrategy, "inspects_source", False, operator.eq
            )
        )
        self.assertFalse(
            passes_operator_filter(
                self.TestStrategy, "inspects_source", True, operator.eq
            )
        )

    @given(
        smaller=integers(min_value=0, max_value=9),
        larger=integers(min_value=11, max_value=100),
    )
    @example(smaller=0, larger=float("inf"))
    @settings(max_examples=5)
    def test_inequality_filter(self, smaller, larger):
        self.assertTrue(
            passes_operator_filter(
                self.TestStrategy, "memory_depth", smaller, operator.ge
            )
        )
        self.assertTrue(
            passes_operator_filter(
                self.TestStrategy, "memory_depth", larger, operator.le
            )
        )
        self.assertFalse(
            passes_operator_filter(
                self.TestStrategy, "memory_depth", smaller, operator.le
            )
        )
        self.assertFalse(
            passes_operator_filter(
                self.TestStrategy, "memory_depth", larger, operator.ge
            )
        )

    def test_list_filter(self):
        self.assertTrue(
            passes_in_list_filter(self.TestStrategy, "makes_use_of", ["game"])
        )
        self.assertTrue(
            passes_in_list_filter(self.TestStrategy, "makes_use_of", ["length"])
        )
        self.assertTrue(
            passes_in_list_filter(
                self.TestStrategy, "makes_use_of", ["game", "length"]
            )
        )
        self.assertFalse(
            passes_in_list_filter(self.TestStrategy, "makes_use_of", "test")
        )

    @given(
        smaller=integers(min_value=0, max_value=9),
        larger=integers(min_value=11, max_value=100),
    )
    @example(smaller=0, larger=float("inf"))
    @settings(max_examples=5)
    def test_passes_filterset(self, smaller, larger):

        full_passing_filterset_1 = {
            "stochastic": True,
            "inspects_source": False,
            "min_memory_depth": smaller,
            "max_memory_depth": larger,
            "makes_use_of": ["game", "length"],
        }

        full_passing_filterset_2 = {
            "stochastic": True,
            "inspects_source": False,
            "memory_depth": 10,
            "makes_use_of": ["game", "length"],
        }

        sparse_passing_filterset = {
            "stochastic": True,
            "inspects_source": False,
            "makes_use_of": ["length"],
        }

        full_failing_filterset = {
            "stochastic": False,
            "inspects_source": False,
            "min_memory_depth": smaller,
            "max_memory_depth": larger,
            "makes_use_of": ["length"],
        }

        sparse_failing_filterset = {
            "stochastic": False,
            "inspects_source": False,
            "min_memory_depth": smaller,
        }

        self.assertTrue(
            passes_filterset(self.TestStrategy, full_passing_filterset_1)
        )
        self.assertTrue(
            passes_filterset(self.TestStrategy, full_passing_filterset_2)
        )
        self.assertTrue(
            passes_filterset(self.TestStrategy, sparse_passing_filterset)
        )
        self.assertFalse(
            passes_filterset(self.TestStrategy, full_failing_filterset)
        )
        self.assertFalse(
            passes_filterset(self.TestStrategy, sparse_failing_filterset)
        )

    def test_filtered_strategies(self):
        class StochasticTestStrategy(Player):
            classifier = {
                "stochastic": True,
                "memory_depth": float("inf"),
                "makes_use_of": [],
            }

        class MemoryDepth2TestStrategy(Player):
            classifier = {
                "stochastic": False,
                "memory_depth": 2,
                "makes_use_of": [],
            }

        class UsesLengthTestStrategy(Player):
            classifier = {
                "stochastic": True,
                "memory_depth": float("inf"),
                "makes_use_of": ["length"],
            }

        strategies = [
            StochasticTestStrategy,
            MemoryDepth2TestStrategy,
            UsesLengthTestStrategy,
        ]

        stochastic_filterset = {"stochastic": True}

        deterministic_filterset = {"stochastic": False}

        uses_length_filterset = {"stochastic": True, "makes_use_of": ["length"]}

        self.assertEqual(
            axl.filtered_strategies(stochastic_filterset, strategies),
            [StochasticTestStrategy, UsesLengthTestStrategy],
        )
        self.assertEqual(
            axl.filtered_strategies(deterministic_filterset, strategies),
            [MemoryDepth2TestStrategy],
        )
        self.assertEqual(
            axl.filtered_strategies(uses_length_filterset, strategies),
            [UsesLengthTestStrategy],
        )
