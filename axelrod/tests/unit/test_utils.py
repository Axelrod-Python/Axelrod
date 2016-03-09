"""Tests for the utils functions and classes."""

import axelrod
import unittest

from hypothesis import given
from hypothesis.strategies import floats, text


class TestTimedMessage(unittest.TestCase):

    @given(start_time=floats(min_value=0, allow_nan=False,
                             allow_infinity=False),
           message=text())
    def test_time_message(self, start_time, message):
        self.assertIsInstance(axelrod.utils.timed_message(message, start_time), str)
