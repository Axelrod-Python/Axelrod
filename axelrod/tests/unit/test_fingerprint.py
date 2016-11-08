import unittest
import axelrod as axl
from axelrod.fingerprint import *


class TestFingerprint(unittest.TestCase):
    """Some stuff"""

    def test_init(self):
        strategy = axl.Cooperator()
        probe = axl.TitForTat()
        fingerprint = AshlockFingerprint(strategy, probe)
        self.assertEqual(fingerprint.strategy, strategy)
        self.assertEqual(fingerprint.probe, probe)
