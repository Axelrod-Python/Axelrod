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
        timed_message = axelrod.utils.timed_message(message, start_time)
        self.assertIsInstance(timed_message, str)
        self.assertEqual(timed_message[:len(message)], message)

class TestSetupLogging(unittest.TestCase):

    def test_setup_logging(self):
        axelrod.utils.setup_logging(logging_destination='console', verbosity='INFO')
