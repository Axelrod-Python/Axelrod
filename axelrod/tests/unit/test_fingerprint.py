import os
import unittest
from tempfile import mkstemp
from unittest.mock import patch

import numpy as np
import matplotlib.pyplot
from hypothesis import given, settings

import axelrod as axl
from axelrod.fingerprint import (create_points, create_jossann, create_probes,
                                 create_edges, generate_data, reshape_data,
                                 AshlockFingerprint, Point, TransitiveFingerprint)
from axelrod.tests.property import strategy_lists

C, D = axl.Action.C, axl.Action.D


class RecordedMksTemp(object):
    """This object records all results from RecordedMksTemp.mkstemp. It's for
    testing that temp files are created and then destroyed."""
    record = []

    @staticmethod
    def mkstemp(*args, **kwargs):
        temp_file_info = mkstemp(*args, **kwargs)
        RecordedMksTemp.record.append(temp_file_info)
        return temp_file_info

    @staticmethod
    def reset_record():
        RecordedMksTemp.record = []


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

    def test_create_points(self):
        test_points = create_points(0.5, progress_bar=False)
        self.assertEqual(test_points, self.expected_points)

    def test_create_jossann(self):
        # x + y < 1
        ja = create_jossann((.5, .4), self.probe)
        self.assertEqual(str(ja), "Joss-Ann Tit For Tat: (0.5, 0.4)")

        # x + y = 1
        ja = create_jossann((.4, .6), self.probe)
        self.assertEqual(str(ja), "Dual Joss-Ann Tit For Tat: (0.6, 0.4)")

        # x + y > 1
        ja = create_jossann((.5, .6), self.probe)
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

    def test_create_probes(self):
        probes = create_probes(self.probe, self.expected_points,
                               progress_bar=False)
        self.assertEqual(len(probes), 9)

    def test_create_edges(self):
        edges = create_edges(self.expected_points, progress_bar=False)
        self.assertEqual(edges, self.expected_edges)

    def test_generate_data(self):
        interactions = {
            (0, 1): [[(C, C)], [(C, C)]],
            (0, 2): [[(C, C), (C, C)], [(C, D)]],
            (0, 3): [[(C, C), (D, C)]],
            (0, 4): [[(C, C), (D, C)], [(D, D)]],
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
            Point(0.5, 0.0): 2.5,
            Point(0.5, 0.5): 2.5,
            Point(0.5, 1.0): 0.0,
            Point(1.0, 0.0): 0.5,
            Point(1.0, 0.5): 1.0,
            Point(1.0, 1.0): 5.0,
        }
        data = generate_data(interactions, self.expected_points,
                             self.expected_edges)
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

    def test_construct_tournament_elemets(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        edges, tournament_players = af.construct_tournament_elements(
            0.5, progress_bar=False
        )
        self.assertEqual(edges, self.expected_edges)
        self.assertEqual(len(tournament_players), 10)
        self.assertEqual(tournament_players[0].__class__, af.strategy)

    def test_progress_bar_fingerprint(self):
        af = AshlockFingerprint(self.strategy, self.probe)
        data = af.fingerprint(turns=10, repetitions=2, step=0.5,
                              progress_bar=True)
        self.assertEqual(sorted(data.keys()), self.expected_points)

    @patch('axelrod.fingerprint.mkstemp', RecordedMksTemp.mkstemp)
    def test_temp_file_creation(self):

        RecordedMksTemp.reset_record()
        af = AshlockFingerprint(self.strategy, self.probe)
        filename = "test_outputs/test_fingerprint.csv"

        # No temp file is created.
        af.fingerprint(turns=1, repetitions=1, step=0.5, progress_bar=False,
                       in_memory=True)
        af.fingerprint(turns=1, repetitions=1, step=0.5, progress_bar=False,
                       in_memory=True, filename=filename)
        af.fingerprint(turns=1, repetitions=1, step=0.5, progress_bar=False,
                       in_memory=False, filename=filename)

        self.assertEqual(RecordedMksTemp.record, [])

        # Temp file is created and destroyed.
        af.fingerprint(turns=1, repetitions=1, step=0.5, progress_bar=False,
                       in_memory=False, filename=None)

        self.assertEqual(len(RecordedMksTemp.record), 1)
        filename = RecordedMksTemp.record[0][1]
        self.assertIsInstance(filename, str)
        self.assertNotEqual(filename, '')
        self.assertFalse(os.path.isfile(filename))

    def test_fingerprint_with_filename(self):
        filename = "test_outputs/test_fingerprint.csv"
        af = AshlockFingerprint(self.strategy, self.probe)
        af.fingerprint(turns=1, repetitions=1, step=0.5, progress_bar=False,
                       filename=filename)
        with open(filename, 'r') as out:
            data = out.read()
            self.assertEqual(len(data.split("\n")), 10)

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
        q = af.plot(cmap='jet')
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
        test_data = {Point(x=0.0, y=0.0): 3.000,
                     Point(x=0.0, y=0.25): 1.710,
                     Point(x=0.0, y=0.5): 1.440,
                     Point(x=0.0, y=0.75): 1.080,
                     Point(x=0.0, y=1.0): 0.500,
                     Point(x=0.25, y=0.0): 3.000,
                     Point(x=0.25, y=0.25): 2.280,
                     Point(x=0.25, y=0.5): 1.670,
                     Point(x=0.25, y=0.75): 1.490,
                     Point(x=0.25, y=1.0): 0.770,
                     Point(x=0.5, y=0.0): 3.000,
                     Point(x=0.5, y=0.25): 2.740,
                     Point(x=0.5, y=0.5): 2.240,
                     Point(x=0.5, y=0.75): 1.730,
                     Point(x=0.5, y=1.0): 1.000,
                     Point(x=0.75, y=0.0): 3.000,
                     Point(x=0.75, y=0.25): 3.520,
                     Point(x=0.75, y=0.5): 2.830,
                     Point(x=0.75, y=0.75): 1.750,
                     Point(x=0.75, y=1.0): 1.250,
                     Point(x=1.0, y=0.0): 3.000,
                     Point(x=1.0, y=0.25): 4.440,
                     Point(x=1.0, y=0.5): 4.410,
                     Point(x=1.0, y=0.75): 4.440,
                     Point(x=1.0, y=1.0): 1.300}
        af = axl.AshlockFingerprint(self.strategy, self.probe)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25,
                              progress_bar=False)

        for key, value in data.items():
            self.assertAlmostEqual(value, test_data[key], places=2)

    def test_tft_fingerprint(self):
        axl.seed(0)  # Fingerprinting is a random process
        test_data = {Point(x=0.0, y=0.0): 3.000,
                     Point(x=0.0, y=0.25): 1.820,
                     Point(x=0.0, y=0.5): 1.130,
                     Point(x=0.0, y=0.75): 1.050,
                     Point(x=0.0, y=1.0): 0.980,
                     Point(x=0.25, y=0.0): 3.000,
                     Point(x=0.25, y=0.25): 2.440,
                     Point(x=0.25, y=0.5): 1.770,
                     Point(x=0.25, y=0.75): 1.700,
                     Point(x=0.25, y=1.0): 1.490,
                     Point(x=0.5, y=0.0): 3.000,
                     Point(x=0.5, y=0.25): 2.580,
                     Point(x=0.5, y=0.5): 2.220,
                     Point(x=0.5, y=0.75): 2.000,
                     Point(x=0.5, y=1.0): 1.940,
                     Point(x=0.75, y=0.0): 3.000,
                     Point(x=0.75, y=0.25): 2.730,
                     Point(x=0.75, y=0.5): 2.290,
                     Point(x=0.75, y=0.75): 2.310,
                     Point(x=0.75, y=1.0): 2.130,
                     Point(x=1.0, y=0.0): 3.000,
                     Point(x=1.0, y=0.25): 2.790,
                     Point(x=1.0, y=0.5): 2.480,
                     Point(x=1.0, y=0.75): 2.310,
                     Point(x=1.0, y=1.0): 2.180}

        af = axl.AshlockFingerprint(axl.TitForTat, self.probe)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25,
                              progress_bar=False)

        for key, value in data.items():
            self.assertAlmostEqual(value, test_data[key], places=2)

    def test_majority_fingerprint(self):
        axl.seed(0)  # Fingerprinting is a random process
        test_data = {Point(x=0.0, y=0.0): 3.000,
                     Point(x=0.0, y=0.25): 1.940,
                     Point(x=0.0, y=0.5): 1.130,
                     Point(x=0.0, y=0.75): 1.030,
                     Point(x=0.0, y=1.0): 0.980,
                     Point(x=0.25, y=0.0): 3.000,
                     Point(x=0.25, y=0.25): 2.130,
                     Point(x=0.25, y=0.5): 1.940,
                     Point(x=0.25, y=0.75): 2.060,
                     Point(x=0.25, y=1.0): 1.940,
                     Point(x=0.5, y=0.0): 3.000,
                     Point(x=0.5, y=0.25): 2.300,
                     Point(x=0.5, y=0.5): 2.250,
                     Point(x=0.5, y=0.75): 2.420,
                     Point(x=0.5, y=1.0): 2.690,
                     Point(x=0.75, y=0.0): 3.000,
                     Point(x=0.75, y=0.25): 2.400,
                     Point(x=0.75, y=0.5): 2.010,
                     Point(x=0.75, y=0.75): 2.390,
                     Point(x=0.75, y=1.0): 2.520,
                     Point(x=1.0, y=0.0): 3.000,
                     Point(x=1.0, y=0.25): 2.360,
                     Point(x=1.0, y=0.5): 1.740,
                     Point(x=1.0, y=0.75): 2.260,
                     Point(x=1.0, y=1.0): 2.260}

        af = axl.AshlockFingerprint(axl.GoByMajority, self.probe)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25,
                              progress_bar=False)

        for key, value in data.items():
            self.assertAlmostEqual(value, test_data[key], places=2)

    @given(strategy_pair=strategy_lists(min_size=2, max_size=2))
    @settings(max_examples=5, max_iterations=20)
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


class TestTransitiveFingerprint(unittest.TestCase):

    def test_init(self):
        player = axl.TitForTat()
        fingerprint = axl.TransitiveFingerprint(strategy=player)
        self.assertEqual(fingerprint.strategy, player)
        self.assertEqual(fingerprint.opponents, [axl.Random(p) for p in
                                                 np.linspace(0, 1, 50)])

    def test_init_with_opponents(self):
        player = axl.TitForTat()
        opponents = [s() for s in axl.demo_strategies]
        fingerprint = axl.TransitiveFingerprint(strategy=player,
                                                opponents=opponents)
        self.assertEqual(fingerprint.strategy, player)
        self.assertEqual(fingerprint.opponents, opponents)

    def test_init_with_not_default_number(self):
        player = axl.TitForTat()
        number_opponents = 10
        fingerprint = axl.TransitiveFingerprint(strategy=player,
                                                number_opponents=number_opponents)
        self.assertEqual(fingerprint.strategy, player)
        self.assertEqual(fingerprint.opponents, [axl.Random(p) for p in
                                                 np.linspace(0, 1, 10)])

    def test_fingerprint_with_filename(self):
        filename = "test_outputs/test_fingerprint.csv"
        strategy = axl.TitForTat()
        tf = TransitiveFingerprint(strategy)
        tf.fingerprint(turns=1, repetitions=1, progress_bar=False,
                       filename=filename)
        with open(filename, 'r') as out:
            data = out.read()
            self.assertEqual(len(data.split("\n")), 50 + 1)

    def test_serial_fingerprint(self):
        strategy = axl.TitForTat()
        tf = TransitiveFingerprint(strategy)
        tf.fingerprint(repetitions=1, progress_bar=False,
                       filename='test_outputs/tran_fin.csv')
        self.assertEqual(tf.data.shape, (50, 50))

    def test_parallel_fingerprint(self):
        strategy = axl.TitForTat()
        tf = TransitiveFingerprint(strategy)
        tf.fingerprint(repetitions=1, progress_bar=False, processes=2)

        self.assertEqual(tf.data.shape, (50, 50))

    def test_analyse_cooperation_ratio(self):
        tf = TransitiveFingerprint(axl.TitForTat)
        filename = "test_outputs/test_fingerprint.csv"
        with open(filename, "w") as f:
            f.write(
"""0,1,Player0,Player1,CCC,DDD
0,1,Player0,Player1,CCC,DDD
0,2,Player0,Player2,CCD,DDD
0,2,Player0,Player2,CCC,DDD
0,3,Player0,Player3,CCD,DDD
0,3,Player0,Player3,DCC,DDD
0,4,Player0,Player3,DDD,DDD
0,4,Player0,Player3,DDD,DDD""")
        data = tf.analyse_cooperation_ratio(filename)
        expected_data = np.array([[1, 1, 1],
                                  [1, 1, 1 / 2],
                                  [1 / 2, 1, 1 / 2],
                                  [0, 0, 0]])
        self.assertTrue(np.array_equal(data, expected_data))

    def test_plot(self):
        """
        Test that plot is created with various arguments.
        """
        tf = TransitiveFingerprint(axl.TitForTat)
        tf.fingerprint(turns=10, repetitions=2, progress_bar=False)
        p = tf.plot()
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
        p = tf.plot(cmap="jet")
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
        p = tf.plot(interpolation='bicubic')
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
        p = tf.plot(title="Title")
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
        p = tf.plot(colorbar=False)
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
        p = tf.plot(labels=False)
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
        p = tf.plot(display_names=True)
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
