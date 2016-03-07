"""Tests for the hunter strategy."""

import random
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
