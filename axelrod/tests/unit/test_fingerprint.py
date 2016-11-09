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

    def test_create_coordinates(self):
        test_coordinates = create_coordinates(0.5)
        coordinates = [(0.0, 0.0), (0.0, 0.5), (0.5, 0.0), (0.5, 0.5)]
        self.assertEqual(test_coordinates, coordinates)

    def test_create_probes(self):
        coords = [(0.0, 0.0), (0.0, 0.5), (0.5, 0.0), (0.5, 0.5)]
        probe_dict = create_probes(probe, coords)
        self.assertEqual(list(probe_dict.keys()), coords)
        # self.assertEqual(list(probe_dict.values()), self.expected_probes)

    def test_create_edges(self):
        coords = [(0.0, 0.0), (0.0, 0.5), (0.5, 0.0), (0.5, 0.5)]
        expected_edges = [(0, 2), (0, 3), (0, 4), (0, 5)]
        edges = create_edges(coords)
        self.assertEqual(edges, expected_edges)

    def test_fingerprint(self):
        pass

    def test__generate_data(self):
        pass

    def test_plot(self):
        pass
