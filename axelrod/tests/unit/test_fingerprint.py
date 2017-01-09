import unittest
from hypothesis import given
from axelrod.fingerprint import *
from axelrod.tests.property import strategy_lists


matplotlib_installed = True
try:
    import matplotlib.pyplot
except ImportError:
    matplotlib_installed = False


class TestFingerprint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.strategy = axl.WinStayLoseShift
        cls.probe = axl.TitForTat
        cls.expected_points = [(0.0, 0.0), (0.0, 0.5), (0.0, 1.0),
                               (0.5, 0.0), (0.5, 0.5), (0.5, 1.0),
                               (1.0, 0.0), (1.0, 0.5), (1.0, 1.0)]
        cls.expected_edges = [(0, 1), (0, 2), (0, 3),
                              (0, 4), (0, 5), (0, 6),
                              (0, 7), (0, 8), (0, 9)]

    def test_default_init(self):
        fingerprint = AshlockFingerprint(self.strategy)
        self.assertEqual(fingerprint.strategy, self.strategy)
        self.assertEqual(fingerprint.probe, self.probe)

    def test_init(self):
        fingerprint = AshlockFingerprint(self.strategy, self.probe)
        self.assertEqual(fingerprint.strategy, self.strategy)
        self.assertEqual(fingerprint.probe, self.probe)

    def test_init_with_instance(self):
        player = self.strategy()
        fingerprint = AshlockFingerprint(player)
        self.assertEqual(fingerprint.strategy, player)
        self.assertEqual(fingerprint.probe, self.probe)

        probe_player = self.probe()
        fingerprint = AshlockFingerprint(self.strategy, probe_player)
        self.assertEqual(fingerprint.strategy, self.strategy)
        self.assertEqual(fingerprint.probe, probe_player)

        fingerprint = AshlockFingerprint(player, probe_player)
        self.assertEqual(fingerprint.strategy, player)
        self.assertEqual(fingerprint.probe, probe_player)

    def test_create_jossann(self):
        fingerprint = AshlockFingerprint(self.strategy)

        # x + y < 1
        ja = fingerprint.create_jossann((.5, .4), self.probe)
        self.assertEqual(str(ja), "Joss-Ann Tit For Tat")

        # x + y = 1
        ja = fingerprint.create_jossann((.4, .6), self.probe)
        self.assertEqual(str(ja), "Dual Joss-Ann Tit For Tat")

        # x + y > 1
        ja = fingerprint.create_jossann((.5, .6), self.probe)
        self.assertEqual(str(ja), "Dual Joss-Ann Tit For Tat")

    def test_create_jossann_parametrised_player(self):
        fingerprint = AshlockFingerprint(self.strategy)

        probe = axl.Random(0.1)

        # x + y < 1
        ja = fingerprint.create_jossann((.5, .4), probe)
        self.assertEqual(str(ja), "Joss-Ann Random: 0.1")

        # x + y = 1
        ja = fingerprint.create_jossann((.4, .6), probe)
        self.assertEqual(str(ja), "Dual Joss-Ann Random: 0.1")

        # x + y > 1
        ja = fingerprint.create_jossann((.5, .6), probe)
        self.assertEqual(str(ja), "Dual Joss-Ann Random: 0.1")

    def test_create_points(self):
        test_points = create_points(0.5, progress_bar=False)
        self.assertEqual(test_points, self.expected_points)

    def test_create_probes(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        probes = af.create_probes(self.probe, self.expected_points,
                                  progress_bar=False)
        self.assertEqual(len(probes), 9)

    def test_create_edges(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        edges = af.create_edges(self.expected_points, progress_bar=False)
        self.assertEqual(edges, self.expected_edges)

    def test_construct_tournament_elemets(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        edges, tournament_players = af.construct_tournament_elements(0.5,
                                                            progress_bar=False)
        self.assertEqual(edges, self.expected_edges)
        self.assertEqual(len(tournament_players), 10)
        self.assertEqual(tournament_players[0].__class__, af.strategy)

    def test_progress_bar_fingerprint(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        data = af.fingerprint(turns=10, repetitions=2, step=0.5,
                              progress_bar=True)
        self.assertEqual(sorted(data.keys()), self.expected_points)

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
        self.assertEqual(coord_keys, self.expected_points)

    def test_serial_fingerprint(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        data = af.fingerprint(turns=10, repetitions=2, step=0.5,
                              progress_bar=False)
        edge_keys = sorted(list(af.interactions.keys()))
        coord_keys = sorted(list(data.keys()))
        self.assertEqual(af.step, 0.5)
        self.assertEqual(edge_keys, self.expected_edges)
        self.assertEqual(coord_keys, self.expected_points)

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
        self.assertEqual(coord_keys, self.expected_points)

    def test_generate_data(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        edges, players = af.construct_tournament_elements(0.5)
        spatial_tournament = axl.SpatialTournament(players,
                                                   turns=10,
                                                   repetitions=2,
                                                   edges=edges)
        results = spatial_tournament.play(progress_bar=False,
                                          keep_interactions=True)
        data = af.generate_data(results.interactions, self.expected_points,
                                self.expected_edges)
        keys = sorted(list(data.keys()))
        values = [0 < score < 5 for score in data.values()]
        self.assertEqual(sorted(keys), self.expected_points)
        self.assertEqual(all(values), True)

    def test_reshape_data(self):
        test_points = [Point(x=0.0, y=0.0),
                       Point(x=0.0, y=0.5),
                       Point(x=0.0, y=1.0),
                       Point(x=0.5, y=0.0),
                       Point(x=0.5, y=0.5),
                       Point(x=0.5, y=1.0),
                       Point(x=1.0, y=0.0),
                       Point(x=1.0, y=0.5),
                       Point(x=1.0, y=1.0)]
        test_data = {Point(x=0.0, y=0.0): 5,
                     Point(x=0.0, y=0.5): 9,
                     Point(x=0.0, y=1.0): 3,
                     Point(x=0.5, y=0.0): 8,
                     Point(x=0.5, y=0.5): 2,
                     Point(x=0.5, y=1.0): 4,
                     Point(x=1.0, y=0.0): 2,
                     Point(x=1.0, y=0.5): 1,
                     Point(x=1.0, y=1.0): 9}
        test_shaped_data = [[3, 4, 9],
                            [9, 2, 1],
                            [5, 8, 2]]
        af = AshlockFingerprint(self.strategy, self.probe)
        plotting_data = af.reshape_data(test_data, test_points, 3)
        for i in range(len(plotting_data)):
            self.assertEqual(list(plotting_data[i]), test_shaped_data[i])

    def test_plot(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        af.fingerprint(turns=10, repetitions=2, step=0.25, progress_bar=False)
        p = af.plot()
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
        q = af.plot(col_map='jet')
        self.assertIsInstance(q, matplotlib.pyplot.Figure)
        r = af.plot(interpolation='bicubic')
        self.assertIsInstance(r, matplotlib.pyplot.Figure)
        t = af.plot(title='Title')
        self.assertIsInstance(t, matplotlib.pyplot.Figure)
        u = af.plot(colorbar=False)
        self.assertIsInstance(u, matplotlib.pyplot.Figure)
        v = af.plot(labels=False)
        self.assertIsInstance(v, matplotlib.pyplot.Figure)

    def test_wsls_fingerprint(self):
        axl.seed(0)  # Fingerprinting is a random process
        test_data = {Point(x=0.0, y=0.0): 3.0,
                     Point(x=0.0, y=0.25): 1.46,
                     Point(x=0.0, y=0.5): 1.54,
                     Point(x=0.0, y=0.75): 1.12,
                     Point(x=0.0, y=1.0): 0.5,
                     Point(x=0.25, y=0.0): 3.0,
                     Point(x=0.25, y=0.25): 2.04,
                     Point(x=0.25, y=0.5): 2.0,
                     Point(x=0.25, y=0.75): 1.34,
                     Point(x=0.25, y=1.0): 0.9,
                     Point(x=0.5, y=0.0): 3.0,
                     Point(x=0.5, y=0.25): 3.0,
                     Point(x=0.5, y=0.5): 2.06,
                     Point(x=0.5, y=0.75): 1.36,
                     Point(x=0.5, y=1.0): 1.0,
                     Point(x=0.75, y=0.0): 3.0,
                     Point(x=0.75, y=0.25): 3.56,
                     Point(x=0.75, y=0.5): 2.06,
                     Point(x=0.75, y=0.75): 3.0,
                     Point(x=0.75, y=1.0): 1.04,
                     Point(x=1.0, y=0.0): 3.0,
                     Point(x=1.0, y=0.25): 4.86,
                     Point(x=1.0, y=0.5): 4.9,
                     Point(x=1.0, y=0.75): 4.9,
                     Point(x=1.0, y=1.0): 1.3}

        af = axl.AshlockFingerprint(self.strategy, self.probe)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25)

        for key, value in data.items():
            self.assertAlmostEqual(value, test_data[key])

    def test_tft_fingerprint(self):
        axl.seed(0)  # Fingerprinting is a random process
        test_data = {Point(x=0.0, y=0.0): 3.0,
                     Point(x=0.0, y=0.25): 1.1,
                     Point(x=0.0, y=0.5): 1.08,
                     Point(x=0.0, y=0.75): 1.04,
                     Point(x=0.0, y=1.0): 0.98,
                     Point(x=0.25, y=0.0): 3.0,
                     Point(x=0.25, y=0.25): 2.26,
                     Point(x=0.25, y=0.5): 2.1,
                     Point(x=0.25, y=0.75): 1.66,
                     Point(x=0.25, y=1.0): 1.64,
                     Point(x=0.5, y=0.0): 3.0,
                     Point(x=0.5, y=0.25): 2.5,
                     Point(x=0.5, y=0.5): 2.12,
                     Point(x=0.5, y=0.75): 1.86,
                     Point(x=0.5, y=1.0): 1.88,
                     Point(x=0.75, y=0.0): 3.0,
                     Point(x=0.75, y=0.25): 2.84,
                     Point(x=0.75, y=0.5): 2.36,
                     Point(x=0.75, y=0.75): 2.28,
                     Point(x=0.75, y=1.0): 1.98,
                     Point(x=1.0, y=0.0): 3.0,
                     Point(x=1.0, y=0.25): 2.78,
                     Point(x=1.0, y=0.5): 2.56,
                     Point(x=1.0, y=0.75): 2.44,
                     Point(x=1.0, y=1.0): 2.18}
        af = axl.AshlockFingerprint(axl.TitForTat, self.probe)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25)

        for key, value in data.items():
            self.assertAlmostEqual(value, test_data[key])

    def test_majority_fingerprint(self):
        axl.seed(0)  # Fingerprinting is a random process
        test_data = {Point(x=0.0, y=0.0): 3.0,
                     Point(x=0.0, y=0.25): 1.18,
                     Point(x=0.0, y=0.5): 1.98,
                     Point(x=0.0, y=0.75): 1.04,
                     Point(x=0.0, y=1.0): 0.98,
                     Point(x=0.25, y=0.0): 3.0,
                     Point(x=0.25, y=0.25): 2.16,
                     Point(x=0.25, y=0.5): 1.74,
                     Point(x=0.25, y=0.75): 1.96,
                     Point(x=0.25, y=1.0): 2.24,
                     Point(x=0.5, y=0.0): 3.0,
                     Point(x=0.5, y=0.25): 2.46,
                     Point(x=0.5, y=0.5): 2.44,
                     Point(x=0.5, y=0.75): 2.24,
                     Point(x=0.5, y=1.0): 2.74,
                     Point(x=0.75, y=0.0): 3.0,
                     Point(x=0.75, y=0.25): 2.52,
                     Point(x=0.75, y=0.5): 2.16,
                     Point(x=0.75, y=0.75): 2.1,
                     Point(x=0.75, y=1.0): 2.44,
                     Point(x=1.0, y=0.0): 3.0,
                     Point(x=1.0, y=0.25): 2.22,
                     Point(x=1.0, y=0.5): 1.64,
                     Point(x=1.0, y=0.75): 2.08,
                     Point(x=1.0, y=1.0): 2.26}
        af = axl.AshlockFingerprint(axl.GoByMajority, self.probe)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25)

        for key, value in data.items():
            self.assertAlmostEqual(value, test_data[key])

    @given(strategy_pair=strategy_lists(min_size=2, max_size=2))
    def test_pair_fingerprints(self, strategy_pair):
        """
        A test to check that we can fingerprint
        with any two given strategies or instances
        """
        strategy, probe = strategy_pair
        af = AshlockFingerprint(strategy, probe)
        data = af.fingerprint(turns=2, repetitions=2, step=0.5,
                              progress_bar=False)
        self.assertIsInstance(data, dict)

        af = AshlockFingerprint(strategy(), probe)
        data = af.fingerprint(turns=2, repetitions=2, step=0.5,
                              progress_bar=False)
        self.assertIsInstance(data, dict)

        af = AshlockFingerprint(strategy, probe())
        data = af.fingerprint(turns=2, repetitions=2, step=0.5,
                              progress_bar=False)
        self.assertIsInstance(data, dict)

        af = AshlockFingerprint(strategy(), probe())
        data = af.fingerprint(turns=2, repetitions=2, step=0.5,
                              progress_bar=False)
        self.assertIsInstance(data, dict)
