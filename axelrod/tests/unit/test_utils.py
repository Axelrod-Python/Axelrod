"""Tests for the utils functions and classes."""

import axelrod
import unittest

from hypothesis import given
from hypothesis.strategies import floats, text

import logging
from testfixtures import Comparison as C, compare
import sys

class TestTimedMessage(unittest.TestCase):

    @given(start_time=floats(min_value=0, allow_nan=False,
                             allow_infinity=False),
           message=text())
    def test_time_message(self, start_time, message):
        timed_message = axelrod.utils.timed_message(message, start_time)
        self.assertEqual(timed_message[:len(message)], message)

    def test_time_message_example(self):
        message = "Full tournament"
        start_time = 0
        timed_message = axelrod.utils.timed_message(message, start_time)
        self.assertEqual(timed_message[:len(message)], message)
        self.assertGreaterEqual(float(timed_message[len(message)+4:-1]), 0)



class TestSetupLogging(unittest.TestCase):

    def test_basic_configuration_console(self):
        logger = logging.getLogger("axelrod")
        axelrod.utils.setup_logging(logging_destination='console',
                                    verbosity='INFO')

        compare(logger.level, 20)
        compare([
            C('logging.StreamHandler',
              stream=sys.stderr,
              formatter=C('logging.Formatter',
                          _fmt='%(message)s',
                          strict=False),
              level=logging.NOTSET,
              strict=False)
            ], logger.handlers)
