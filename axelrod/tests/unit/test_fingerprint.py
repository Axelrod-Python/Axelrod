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

    def test_create_probe_coords(test):
        pass

    def test_create_probes(self):
        pass

    def test_create_edges(self):
        pass

    def test_fingerprint(self):
        pass

    def test__generate_data(self):
        pass

    def test_plot(self):
        pass
