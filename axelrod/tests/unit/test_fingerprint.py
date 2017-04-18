import unittest
from hypothesis import given
from axelrod.fingerprint import *
from axelrod.tests.property import strategy_lists
import axelrod as axl

C, D = axl.Actions.C, axl.Actions.D


matplotlib_installed = True
try:
    import matplotlib.pyplot
except ImportError:  # pragma: no cover
    matplotlib_installed = False


class TestFingerPrintHelpers(unittest.TestCase):

    def test_create_points_progress_bar_true(self):
        expected = [Point(0.0, 0.0), Point(0.0, 1.0),
                    Point(1.0, 0.0), Point(1.0, 1.0)]
        self.assertEqual(expected, create_points(1.0, progress_bar=True))

    def test_create_points_rounds_up_to_fraction_with_numerator_eq_one(self):
        step_one = [Point(0.0, 0.0), Point(0.0, 1.0),
                    Point(1.0, 0.0), Point(1.0, 1.0)]
        step_half = [Point(0.0, 0.0), Point(0.0, 0.5), Point(0.0, 1.0),
                     Point(0.5, 0.0), Point(0.5, 0.5), Point(0.5, 1.0),
                     Point(1.0, 0.0), Point(1.0, 0.5), Point(1.0, 1.0)]
        self.assertEqual(step_one, create_points(0.51, progress_bar=False))
        self.assertEqual(step_half, create_points(0.5, progress_bar=False))

    def test_create_point_with_fraction_that_is_not_finite_decimal(self):
        points = create_points(0.3, progress_bar=False)
        self.assertEqual(points[7][1], 1.0)
        self.assertAlmostEqual(points[7][0], 0.33333333, places=7)

    def test_create_edges(self):
        points = [(0.0, 0.0), (0.0, 0.5), (0.0, 1.0),
                  (0.5, 0.0), (0.5, 0.5), (0.5, 1.0),
                  (1.0, 0.0), (1.0, 0.5), (1.0, 1.0)]
        expected_edges = [(0, 1), (0, 2), (0, 3),
                          (0, 4), (0, 5), (0, 6),
                          (0, 7), (0, 8), (0, 9)]
        edges = create_edges(points, progress_bar=False)
        self.assertEqual(edges, expected_edges)

    def test_create_jossann(self):
        probe = axl.TitForTat
        # x + y < 1
        ja = create_jossann((.5, .4), probe)
        self.assertEqual(str(ja), "Joss-Ann Tit For Tat: (0.5, 0.4)")

        # x + y = 1
        ja = create_jossann((.4, .6), probe)
        self.assertEqual(str(ja), "Dual Joss-Ann Tit For Tat: (0.6, 0.4)")

        # x + y > 1
        ja = create_jossann((.5, .6), probe)
        self.assertEqual(str(ja), "Dual Joss-Ann Tit For Tat: (0.5, 0.4)")

    def test_create_jossann_parametrised_player(self):
        probe = axl.Random(p=0.1)

        # x + y < 1
        ja = create_jossann((.5, .4), probe)
        self.assertEqual(str(ja), "Joss-Ann Random: 0.1: (0.5, 0.4)")

        # x + y = 1
        ja = create_jossann((.4, .6), probe)
        self.assertEqual(str(ja), "Dual Joss-Ann Random: 0.1: (0.6, 0.4)")

        # x + y > 1
        ja = create_jossann((.5, .6), probe)
        self.assertEqual(str(ja), "Dual Joss-Ann Random: 0.1: (0.5, 0.4)")

    def test_create_probes_progress_bar_true(self):
        nine_points = create_points(0.5, progress_bar=False)
        probes = create_probes(axl.TitForTat, nine_points, progress_bar=True)
        self.assertEqual(len(probes), 9)

    def test_create_probes(self):
        expected_probe_str = ['Joss-Ann Tit For Tat: (0.0, 0.0)',
                              'Dual Joss-Ann Tit For Tat: (1.0, 0.0)',
                              'Dual Joss-Ann Tit For Tat: (0.0, 1.0)',
                              'Dual Joss-Ann Tit For Tat: (0.0, 0.0)']
        points = create_points(1.0, progress_bar=False)
        probes = create_probes(axl.TitForTat, points, progress_bar=False)
        self.assertEqual([str(probe) for probe in probes], expected_probe_str)

    def test_generate_data(self):
        interactions = {
            (0, 1): [[(C, C)], [(C, C)]],
            (0, 2): [[(C, C), (C, C)], [(C, D)]],
            (0, 3): [[(C, C), (D, C)]],
            (0, 4): [[(C, C), (D, D)]],
            (0, 5): [[(C, D), (D, C)]],
            (0, 6): [[(C, D), (C, D)]],
            (0, 7): [[(C, D), (D, D)]],
            (0, 8): [[(D, D), (D, D)]],
            (0, 9): [[(D, C), (D, C)]],
        }

        expected = {
            Point(0.0, 0.0): 3.0,
            Point(0.0, 0.5): 1.5,
            Point(0.0, 1.0): 4.0,
            Point(0.5, 0.0): 2.0,
            Point(0.5, 0.5): 2.5,
            Point(0.5, 1.0): 0.0,
            Point(1.0, 0.0): 0.5,
            Point(1.0, 0.5): 1.0,
            Point(1.0, 1.0): 5.0,
        }
        points = create_points(0.5, progress_bar=False)
        edges = create_edges(points, progress_bar=False)
        data = generate_data(interactions, points, edges)
        self.assertEqual(data, expected)

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
        plotting_data = reshape_data(test_data, test_points, 3)
        for i in range(len(plotting_data)):
            self.assertEqual(list(plotting_data[i]), test_shaped_data[i])


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

    def test_construct_tournament_elements(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        edges, tournament_players = af.construct_tournament_elements(
            0.5, progress_bar=False)
        self.assertEqual(edges, self.expected_edges)
        self.assertEqual(len(tournament_players), 10)
        self.assertEqual(tournament_players[0].__class__, af.strategy)

    def test_progress_bar_fingerprint(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        data = af.fingerprint(turns=10, repetitions=2, step=0.5,
                              progress_bar=True)
        self.assertEqual(sorted(data.keys()), self.expected_points)

    def test_fingerprint_with_filename(self):
        filename = "test_outputs/test_fingerprint.csv"
        af = AshlockFingerprint(self.strategy, self.probe)
        af.fingerprint(turns=1, repetitions=1, step=0.5, progress_bar=False,
                       filename=filename)
        with open(filename, 'r') as out:
            data = out.read()
            self.assertEqual(len(data.split("\n")), 10)

    def test_fingerprint_with_filename_none_and_in_memory_false(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        af.fingerprint(turns=1, repetitions=1, step=0.5, progress_bar=False,
                       filename=None, in_memory=False)

        edge_keys = sorted(list(af.interactions.keys()))
        coord_keys = sorted(list(af.data.keys()))
        self.assertEqual(af.step, 0.5)
        self.assertEqual(af.spatial_tournament.interactions_dict,
                         af.interactions)
        self.assertEqual(edge_keys, self.expected_edges)
        self.assertEqual(coord_keys, self.expected_points)

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
        u = af.plot(color_bar=False)
        self.assertIsInstance(u, matplotlib.pyplot.Figure)
        v = af.plot(labels=False)
        self.assertIsInstance(v, matplotlib.pyplot.Figure)

    def test_wsls_fingerprint(self):
        axl.seed(0)  # Fingerprinting is a random process
        test_data = {Point(x=0.25, y=1.0): 0.84,
                     Point(x=0.25, y=0.5): 1.85,
                     Point(x=0.75, y=0.5): 3.01,
                     Point(x=0.25, y=0.25): 2.23,
                     Point(x=0.0, y=0.75): 1.08,
                     Point(x=0.75, y=1.0): 1.14,
                     Point(x=0.5, y=0.25): 2.66,
                     Point(x=0.0, y=0.0): 3.0,
                     Point(x=0.75, y=0.25): 3.12,
                     Point(x=1.0, y=0.75): 3.57,
                     Point(x=1.0, y=0.5): 3.94,
                     Point(x=1.0, y=0.0): 3.0,
                     Point(x=1.0, y=0.25): 4.78,
                     Point(x=0.0, y=1.0): 0.5,
                     Point(x=0.5, y=0.0): 3.0,
                     Point(x=0.25, y=0.0): 3.0,
                     Point(x=0.0, y=0.25): 1.71,
                     Point(x=0.0, y=0.5): 1.44,
                     Point(x=0.5, y=0.75): 1.62,
                     Point(x=0.5, y=0.5): 2.77,
                     Point(x=0.75, y=0.75): 2.27,
                     Point(x=0.5, y=1.0): 1.02,
                     Point(x=0.75, y=0.0): 3.0,
                     Point(x=0.25, y=0.75): 1.27,
                     Point(x=1.0, y=1.0): 1.3}

        af = axl.AshlockFingerprint(self.strategy, self.probe)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25,
                              progress_bar=False)

        for key, value in data.items():
            self.assertAlmostEqual(value, test_data[key], places=2)

    def test_tft_fingerprint(self):
        axl.seed(0)  # Fingerprinting is a random process
        test_data = {Point(x=0.25, y=1.0): 1.63,
                     Point(x=0.25, y=0.5): 1.92,
                     Point(x=0.75, y=0.5): 2.33,
                     Point(x=0.25, y=0.25): 2.31,
                     Point(x=0.0, y=0.75): 1.05,
                     Point(x=0.75, y=1.0): 2.07,
                     Point(x=0.5, y=0.25): 2.6,
                     Point(x=0.0, y=0.0): 3.0,
                     Point(x=0.75, y=0.25): 2.76,
                     Point(x=1.0, y=0.75): 2.38,
                     Point(x=1.0, y=0.5): 2.58,
                     Point(x=1.0, y=0.0): 3.0,
                     Point(x=1.0, y=0.25): 2.72,
                     Point(x=0.0, y=1.0): 0.98,
                     Point(x=0.5, y=0.0): 3.0,
                     Point(x=0.25, y=0.0): 3.0,
                     Point(x=0.0, y=0.25): 1.82,
                     Point(x=0.0, y=0.5): 1.13,
                     Point(x=0.5, y=0.75): 1.93,
                     Point(x=0.5, y=0.5): 2.46,
                     Point(x=0.75, y=0.75): 2.3,
                     Point(x=0.5, y=1.0): 1.91,
                     Point(x=0.75, y=0.0): 3.0,
                     Point(x=0.25, y=0.75): 1.62,
                     Point(x=1.0, y=1.0): 2.18}

        af = axl.AshlockFingerprint(axl.TitForTat, self.probe)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25,
                              progress_bar=False)

        for key, value in data.items():
            self.assertAlmostEqual(value, test_data[key], places=2)

    def test_majority_fingerprint(self):
        axl.seed(0)  # Fingerprinting is a random process
        test_data = {Point(x=0.25, y=1.0): 2.179,
                     Point(x=0.25, y=0.5): 1.9,
                     Point(x=0.75, y=0.5): 1.81,
                     Point(x=0.25, y=0.25): 2.31,
                     Point(x=0.0, y=0.75): 1.03,
                     Point(x=0.75, y=1.0): 2.58,
                     Point(x=0.5, y=0.25): 2.34,
                     Point(x=0.0, y=0.0): 3.0,
                     Point(x=0.75, y=0.25): 2.4,
                     Point(x=1.0, y=0.75): 2.0,
                     Point(x=1.0, y=0.5): 1.74,
                     Point(x=1.0, y=0.0): 3.0,
                     Point(x=1.0, y=0.25): 2.219,
                     Point(x=0.0, y=1.0): 0.98,
                     Point(x=0.5, y=0.0): 3.0,
                     Point(x=0.25, y=0.0): 3.0,
                     Point(x=0.0, y=0.25): 1.94,
                     Point(x=0.0, y=0.5): 1.13,
                     Point(x=0.5, y=0.75): 2.6,
                     Point(x=0.5, y=0.5): 1.89,
                     Point(x=0.75, y=0.75): 2.13,
                     Point(x=0.5, y=1.0): 2.7,
                     Point(x=0.75, y=0.0): 3.0,
                     Point(x=0.25, y=0.75): 1.859,
                     Point(x=1.0, y=1.0): 2.26}

        af = axl.AshlockFingerprint(axl.GoByMajority, self.probe)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25,
                              progress_bar=False)

        for key, value in data.items():
            self.assertAlmostEqual(value, test_data[key], places=2)

    @given(strategy_pair=strategy_lists(min_size=2, max_size=2))
    def test_pair_fingerprints(self, strategy_pair):
        """
        A test to check that we can fingerprint
        with any two given strategies or instances
        """
        strategy, probe = strategy_pair
        af = AshlockFingerprint(strategy, probe)
        data = af.fingerprint(turns=2, repetitions=2, step=1.0,
                              progress_bar=False)
        self.assertIsInstance(data, dict)

        af = AshlockFingerprint(strategy(), probe)
        data = af.fingerprint(turns=2, repetitions=2, step=1.0,
                              progress_bar=False)
        self.assertIsInstance(data, dict)

        af = AshlockFingerprint(strategy, probe())
        data = af.fingerprint(turns=2, repetitions=2, step=1.0,
                              progress_bar=False)
        self.assertIsInstance(data, dict)

        af = AshlockFingerprint(strategy(), probe())
        data = af.fingerprint(turns=2, repetitions=2, step=1.0,
                              progress_bar=False)
        self.assertIsInstance(data, dict)
