import unittest
import axelrod as axl
from axelrod.fingerprint import *
from axelrod.strategy_transformers import JossAnnTransformer

matplotlib_installed = True
try:
    import matplotlib.pyplot
except ImportError:
    matplotlib_installed = False


strategy = axl.WinStayLoseShift
probe = axl.TitForTat
coordinates = [(0.0, 0.0), (0.0, 0.5), (0.5, 0.0), (0.5, 0.5)]
probes = [JossAnnTransformer(c)(probe)() for c in coordinates]
edges = [(0, 2), (0, 3), (0, 4), (0, 5)]
long_coordinates = [(0.0, 0.0),
                    (0.0, 0.25),
                    (0.0, 0.5),
                    (0.0, 0.75),
                    (0.25, 0.0),
                    (0.25, 0.25),
                    (0.25, 0.5),
                    (0.25, 0.75),
                    (0.5, 0.0),
                    (0.5, 0.25),
                    (0.5, 0.5),
                    (0.5, 0.75),
                    (0.75, 0.0),
                    (0.75, 0.25),
                    (0.75, 0.5),
                    (0.75, 0.75)]
long_probes = [JossAnnTransformer(c)(probe)() for c in long_coordinates]
long_edges = [(0, 2),
              (0, 3),
              (0, 4),
              (0, 5),
              (0, 6),
              (0, 7),
              (0, 8),
              (0, 9),
              (0, 10),
              (0, 11),
              (0, 12),
              (1, 13),
              (0, 14),
              (0, 15),
              (1, 16),
              (1, 17)]


class TestFingerprint(unittest.TestCase):

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
        probes = create_probes(probe, coords)
        self.assertEqual(len(probes), 4)
        # self.assertEqual(probes, self.expected_probes)

    def test_create_edges(self):
        coords = [(0.0, 0.0), (0.0, 0.5), (0.5, 0.0), (0.5, 0.5)]
        expected_edges = [(0, 2), (0, 3), (0, 4), (0, 5)]
        edges = create_edges(coords)
        self.assertEqual(edges, expected_edges)

    def test_construct_tournament_elemets(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        edges, tournament_players = af.construct_tournament_elements(0.5)
        self.assertEqual(edges, self.expected_edges)
        self.assertEqual(len(tournament_players), 6)
        self.assertEqual(tournament_players[0].__class__, af.strategy)

    def test_serial_fingerprint(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        af.fingerprint(turns=10, repetitions=2, step=0.25)
        edge_keys = sorted(list(af.interactions.keys()))
        coord_keys = sorted(list(af.data.keys()))
        self.assertEqual(af.step, 0.25)
        self.assertEqual(edge_keys, sorted(long_edges))
        self.assertEqual(coord_keys, long_coordinates)

    @unittest.skipIf(axl.on_windows,
                     "Parallel processing not supported on Windows")
    def test_parallel_fingerprint(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        af.fingerprint(turns=10, repetitions=2, step=0.25, processes=2)
        edge_keys = sorted(list(af.interactions.keys()))
        coord_keys = sorted(list(af.data.keys()))
        self.assertEqual(af.step, 0.25)
        self.assertEqual(edge_keys, sorted(long_edges))
        self.assertEqual(coord_keys, long_coordinates)

    def test_generate_data(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        edges, players = af.construct_tournament_elements(0.25)
        spatial_tournament = axl.SpatialTournament(players, turns=10,
                                                   repetitions=2,
                                                   edges=edges)
        results = spatial_tournament.play(progress_bar=False,
                                          keep_interactions=True)
        data = generate_data(results.interactions, long_coordinates, edges)
        keys = sorted(list(data.keys()))
        values = [0 < score < 5 for score in data.values()]
        self.assertEqual(sorted(keys), long_coordinates)
        self.assertEqual(all(values), True)

    def test_plot(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        af.fingerprint(turns=10, repetitions=2, step=0.25)
        p = af.plot()
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
