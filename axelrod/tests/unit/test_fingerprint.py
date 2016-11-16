import unittest
import axelrod as axl
from axelrod.fingerprint import *
from axelrod.strategy_transformers import JossAnnTransformer

from hypothesis import given, settings
from axelrod.tests.property import strategy_lists



matplotlib_installed = True
try:
    import matplotlib.pyplot
except ImportError:
    matplotlib_installed = False


strategy = axl.WinStayLoseShift
probe = axl.TitForTat
coordinates = [(0.0, 0.0), (0.0, 0.5), (0.5, 0.0), (0.5, 0.5)]
probes = [JossAnnTransformer(c)(probe)() for c in coordinates]
edges = [(0, 2), (0, 3), (0, 4), (1, 5)]



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

    def test_create_points(self):
        test_coordinates = create_points(0.5)
        self.assertEqual(test_coordinates, self.expected_coordinates)

    def test_create_probes(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        probes = af.create_probes(probe, self.expected_coordinates)
        self.assertEqual(len(probes), 4)
        # self.assertEqual(probes, self.expected_probes)

    def test_create_edges(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        edges = af.create_edges(self.expected_coordinates)
        self.assertEqual(edges, self.expected_edges)

    def test_construct_tournament_elemets(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        edges, tournament_players = af.construct_tournament_elements(0.5)
        self.assertEqual(edges, self.expected_edges)
        self.assertEqual(len(tournament_players), 6)
        self.assertEqual(tournament_players[0].__class__, af.strategy)

    def test_progress_bar_fingerprint(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        data = af.fingerprint(turns=10, repetitions=2, step=0.5,
                              progress_bar=True)
        self.assertEqual(sorted(data.keys()), self.expected_coordinates)

    def test_in_memory_fingerprint(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        af.fingerprint(turns=10, repetitions=2, step=0.5, progress_bar=False,
                       in_memory=True)
        edge_keys = sorted(list(af.interactions.keys()))
        coord_keys = sorted(list(af.data.keys()))
        self.assertEqual(af.step, 0.5)
        self.assertEqual(af.spatial_tournament.interactions_dict,
                         af.interactions)
        self.assertEqual(edge_keys, self.expected_edges)
        self.assertEqual(coord_keys, self.expected_coordinates)

    def test_serial_fingerprint(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        data = af.fingerprint(turns=10, repetitions=2, step=0.5, progress_bar=False)
        edge_keys = sorted(list(af.interactions.keys()))
        coord_keys = sorted(list(data.keys()))
        self.assertEqual(af.step, 0.5)
        self.assertEqual(edge_keys, self.expected_edges)
        self.assertEqual(coord_keys, self.expected_coordinates)

    @unittest.skipIf(axl.on_windows,
                     "Parallel processing not supported on Windows")
    def test_parallel_fingerprint(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        af.fingerprint(turns=10, repetitions=2, step=0.5, processes=2,
                       progress_bar=False)
        edge_keys = sorted(list(af.interactions.keys()))
        coord_keys = sorted(list(af.data.keys()))
        self.assertEqual(af.step, 0.5)
        self.assertEqual(edge_keys, self.expected_edges)
        self.assertEqual(coord_keys, self.expected_coordinates)

    def test_generate_data(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        edges, players = af.construct_tournament_elements(0.5)
        spatial_tournament = axl.SpatialTournament(players,
                                                   turns=10,
                                                   repetitions=2,
                                                   edges=edges)
        results = spatial_tournament.play(progress_bar=False,
                                          keep_interactions=True)
        data = af.generate_data(results.interactions, self.expected_coordinates,
                             self.expected_edges)
        keys = sorted(list(data.keys()))
        values = [0 < score < 5 for score in data.values()]
        self.assertEqual(sorted(keys), self.expected_coordinates)
        self.assertEqual(all(values), True)

    def test_plot(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        af.fingerprint(turns=10, repetitions=2, step=0.25, progress_bar=False)
        p = af.plot()
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
        q = af.plot(col_map='jet')
        self.assertIsInstance(q, matplotlib.pyplot.Figure)

    @given(strategy_pair=strategy_lists(min_size=2, max_size=2))
    def test_pair_fingerprints(self, strategy_pair):
        """
        A test to check that we can fingerprint
        with any two given strategies
        """
        strategy, probe = strategy_pair
        af = AshlockFingerprint(strategy, probe)
        data = af.fingerprint(turns=2, repetitions=2, step=0.5,
                              progress_bar=False)
        self.assertIsInstance(data, dict)
