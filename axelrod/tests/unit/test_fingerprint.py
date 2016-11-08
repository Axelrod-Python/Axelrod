import unittest
import axelrod as axl
from axelrod.fingerprint import *
from axelrod.strategy_transformers import JossAnnTransformer


strategy = axl.WinStayLoseShift
probe = axl.TitForTat
coordinates = [(0.0, 0.0), (0.0, 0.5), (0.5, 0.0), (0.5, 0.5)]
probes = [JossAnnTransformer(c)(probe)() for c in coordinates]
edges = [(0, 2), (0, 3), (0, 4), (0, 5)]


class TestFingerprint(unittest.TestCase):
    """Some stuff"""

    @classmethod
    def setUpClass(cls):
        cls.strategy = strategy
        cls.probe = probe
        cls.expected_probes = probes
        cls.expected_coordinates = coordinates
        cls.expected_edges = edges

    def test_init(self):
        strategy = axl.Cooperator()
        probe = axl.TitForTat()
        fingerprint = AshlockFingerprint(strategy, probe)
        self.assertEqual(fingerprint.strategy, strategy)
        self.assertEqual(fingerprint.probe, probe)

    def test_create_probe_coords(self):
        AF = AshlockFingerprint(self.strategy, self.probe)
        probe_coords = AF.create_probe_coords(0.5)
        self.assertEqual(probe_coords, self.expected_coordinates)

    def test_create_probes(self):
        AF = AshlockFingerprint(self.strategy, self.probe)
        coords = [(0.0, 0.0), (0.0, 0.5), (0.5, 0.0), (0.5, 0.5)]
        probe_dict = AF.create_probes(self.probe, coords)
        self.assertEqual(list(probe_dict.keys()), self.expected_coordinates)
        # self.assertEqual(list(probe_dict.values()), self.expected_probes)

    def test_create_edges(self):
        AF = AshlockFingerprint(self.strategy, self.probe)
        coords = [(0.0, 0.0), (0.0, 0.5), (0.5, 0.0), (0.5, 0.5)]
        edges = AF.create_edges(coords)
        self.assertEqual(edges, self.expected_edges)
        pass

    def test_fingerprint(self):
        pass

    def test__generate_data(self):
        pass

    def test_plot(self):
        pass
