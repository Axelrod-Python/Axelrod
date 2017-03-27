"""Tests for the strategy utils."""

import unittest

from hypothesis import given
from hypothesis.strategies import sampled_from, lists, integers

from axelrod import Actions
from axelrod._strategy_utils import detect_cycle

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

    def test_regression_test_can_detect_cycle_that_is_repeated_exactly_once(self):
        self.assertEqual(detect_cycle([C, D, C, D]), (C, D))
        self.assertEqual(detect_cycle([C, D, C, D, C]), (C, D))

    def test_cycle_will_be_at_least_min_size(self):
        self.assertEqual(detect_cycle([C, C, C, C], min_size=1), (C, ))
        self.assertEqual(detect_cycle([C, C, C, C], min_size=2), (C, C))

    def test_cycle_that_never_fully_repeats_returns_none(self):
        cycle = [C, D, D]
        to_test = cycle + cycle[:-1]
        self.assertIsNone(detect_cycle(to_test))

    def test_min_size_greater_than_two_times_history_tail_returns_none(self):
        self.assertIsNone(detect_cycle([C, C, C], min_size=2))

    def test_min_size_greater_than_two_times_max_size_has_no_effect(self):
        self.assertEqual(detect_cycle([C, C, C, C, C, C, C, C], min_size=2, max_size=3), (C, C))

    def test_cycle_greater_than_max_size_returns_none(self):
        self.assertEqual(detect_cycle([C, C, D] * 2, min_size=1, max_size=3), (C, C, D))
        self.assertIsNone(detect_cycle([C, C, D] * 2, min_size=1, max_size=2))
