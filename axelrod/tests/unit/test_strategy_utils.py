"""Tests for the strategy utils."""

import unittest

from hypothesis import given
from hypothesis.strategies import sampled_from, lists, integers

from axelrod import Actions
from axelrod._strategy_utils import detect_cycle
from axelrod._strategy_utils import Memoized

C, D = Actions.C, Actions.D


class TestDetectCycle(unittest.TestCase):
    """Test the detect cycle function"""
    @given(cycle=lists(sampled_from([C, D]), min_size=2, max_size=10),
           period=integers(min_value=3, max_value=10))
    def test_finds_cycle(self, cycle, period):
        history = cycle * period
        self.assertIsNotNone(detect_cycle(history))

    def test_no_cycle(self):
        history = [C, D, C, C]
        self.assertIsNone(detect_cycle(history))

        history = [D, D, C, C, C]
        self.assertIsNone(detect_cycle(history))


class TestMemoized(unittest.TestCase):
    """Test the Memoized class"""

    def test_init(self):
        func = lambda x: x + x
        memoized = Memoized(func)
        self.assertEqual(memoized.func, func)
        self.assertEqual(memoized.cache, {})

    def test_call_with_unhashable_type(self):
        func = lambda x: x + x
        memoized = Memoized(func)
        self.assertEqual(memoized([2]), [2, 2])
        self.assertEqual(memoized.cache, {})

    def test_call(self):
        func = lambda x: x + x
        memoized = Memoized(func)
        self.assertEqual(memoized.cache, {})
        self.assertEqual(memoized(2), 4)
        self.assertEqual(memoized.cache, {(2,): 4})
        self.assertEqual(memoized(2), 4)
        self.assertEqual(memoized.cache, {(2,): 4})

    def test_repr(self):
        func = lambda x: x + x
        memoized = Memoized(func)
        self.assertEqual(memoized.__repr__(), None)

        def func_with_docstring(x):
            """A docstring"""
            return x + x

        memoized = Memoized(func_with_docstring)
        self.assertEqual(memoized.__repr__(), "A docstring")
