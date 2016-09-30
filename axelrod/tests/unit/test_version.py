"""
Tests the version number
"""
from axelrod import __version__
import unittest

expected_version = "1.11.0"

class TestVersion(unittest.TestCase):
    def test_version(self):
        self.assertEqual(__version__, expected_version)
