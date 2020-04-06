import unittest
from unittest.mock import patch

import os
from tempfile import mkstemp
import matplotlib.pyplot
import numpy as np
import pathlib

import axelrod as axl
from axelrod.fingerprint import AshlockFingerprint, Point, TransitiveFingerprint
from axelrod.load_data_ import axl_filename
from axelrod.strategy_transformers import DualTransformer, JossAnnTransformer
from axelrod.tests.property import strategy_lists

from hypothesis import given, settings


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

    points_when_using_half_step = [
        (0.0, 0.0),
        (0.0, 0.5),
        (0.0, 1.0),
        (0.5, 0.0),
        (0.5, 0.5),
        (0.5, 1.0),
        (1.0, 0.0),
        (1.0, 0.5),
        (1.0, 1.0),
    ]
    edges_when_using_half_step = [
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
        (0, 7),
        (0, 8),
        (0, 9),
    ]

    def test_default_init(self):
        fingerprint = AshlockFingerprint(axl.WinStayLoseShift)
        self.assertEqual(fingerprint.strategy, axl.WinStayLoseShift)
        self.assertEqual(fingerprint.probe, axl.TitForTat)

    def test_init_with_explicit_probe(self):
        fingerprint = AshlockFingerprint(axl.WinStayLoseShift, axl.Random)
        self.assertEqual(fingerprint.strategy, axl.WinStayLoseShift)
        self.assertEqual(fingerprint.probe, axl.Random)

    def test_init_with_instances(self):
        player = axl.WinStayLoseShift()
        fingerprint = AshlockFingerprint(player)
        self.assertEqual(fingerprint.strategy, player)
        self.assertEqual(fingerprint.probe, axl.TitForTat)

        probe = axl.Random()
        fingerprint = AshlockFingerprint(axl.WinStayLoseShift, probe)
        self.assertEqual(fingerprint.strategy, axl.WinStayLoseShift)
        self.assertEqual(fingerprint.probe, probe)

        fingerprint = AshlockFingerprint(player, probe)
        self.assertEqual(fingerprint.strategy, player)
        self.assertEqual(fingerprint.probe, probe)

    def test_fingerprint_player(self):
        af = AshlockFingerprint(axl.Cooperator())
        af.fingerprint(turns=5, repetitions=3, step=0.5, progress_bar=False)

        self.assertEqual(af.step, 0.5)
        self.assertEqual(af.points, self.points_when_using_half_step)
        self.assertEqual(af.spatial_tournament.turns, 5)
        self.assertEqual(af.spatial_tournament.repetitions, 3)
        self.assertEqual(af.spatial_tournament.edges, self.edges_when_using_half_step)

        # The first player is the fingerprinted one, the rest are probes.
        self.assertIsInstance(af.spatial_tournament.players[0], axl.Cooperator)
        self.assertEqual(len(af.spatial_tournament.players), 10)
        probes = af.spatial_tournament.players[1:]
        self.assertEqual(len(probes), len(af.points))
        self.assertEqual(
            str(probes[0]), "Joss-Ann Tit For Tat: (0.0, 0.0)"
        )  # x + y < 1
        self.assertEqual(
            str(probes[2]), "Dual Joss-Ann Tit For Tat: (1.0, 0.0)"
        )  # x + y = 1
        self.assertEqual(
            str(probes[8]), "Dual Joss-Ann Tit For Tat: (0.0, 0.0)"
        )  # x + y > 1

    def test_fingeprint_explicit_probe(self):
        af = AshlockFingerprint(axl.TitForTat(), probe=axl.Random(p=0.1))
        af.fingerprint(turns=10, repetitions=2, step=0.5, progress_bar=False)

        probes = af.spatial_tournament.players[1:]
        self.assertEqual(
            str(probes[0]), "Joss-Ann Random: 0.1: (0.0, 0.0)"
        )  # x + y < 1
        self.assertEqual(
            str(probes[2]), "Dual Joss-Ann Random: 0.1: (1.0, 0.0)"
        )  # x + y = 1
        self.assertEqual(
            str(probes[8]), "Dual Joss-Ann Random: 0.1: (0.0, 0.0)"
        )  # x + y > 1

    def test_fingerprint_interactions_cooperator(self):
        af = AshlockFingerprint(axl.Cooperator())
        af.fingerprint(turns=5, repetitions=3, step=0.5, progress_bar=False)

        # The keys are edges between players, values are repetitions.
        self.assertCountEqual(
            af.interactions.keys(),
            [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9)],
        )
        self.assertEqual(len(af.interactions.values()), 9)

        # Each edge has 3 repetitions with 5 turns each.
        repetitions = af.interactions.values()
        self.assertTrue(all(len(rep) == 3 for rep in repetitions))
        for iturn in range(3):
            self.assertTrue(all(len(rep[iturn]) == 5 for rep in repetitions))

        # Interactions are invariant for any points where y is zero, and
        # the score should be maximum possible.
        # Player 1 is Point(0.0, 0.0).
        # Player 4 is Point(0.5, 0.0).
        # Player 7 is Point(1.0, 0.0).
        for iplayer in (1, 4, 7):
            for turns in af.interactions[(0, iplayer)]:
                self.assertEqual(len(turns), 5)
                self.assertTrue(all(t == (C, C) for t in turns))
        self.assertEqual(af.data[Point(0.0, 0.0)], 3.0)
        self.assertEqual(af.data[Point(0.5, 0.0)], 3.0)
        self.assertEqual(af.data[Point(1.0, 0.0)], 3.0)

        # Player 3 is Point(0.0, 1.0), which means constant defection
        # from the probe. But the Cooperator doesn't change and score is zero.
        for turns in af.interactions[(0, 3)]:
            self.assertEqual(len(turns), 5)
            self.assertTrue(all(t == (C, D) for t in turns))
        self.assertEqual(af.data[Point(0.0, 1.0)], 0.0)

    def test_fingerprint_interactions_titfortat(self):
        af = AshlockFingerprint(axl.TitForTat())
        af.fingerprint(turns=5, repetitions=3, step=0.5, progress_bar=False)

        # Tit-for-Tats will always cooperate if left to their own devices,
        # so interactions are invariant for any points where y is zero,
        # and the score should be maximum possible.
        # Player 1 is Point(0.0, 0.0).
        # Player 4 is Point(0.5, 0.0).
        # Player 7 is Point(1.0, 0.0).
        for iplayer in (1, 4, 7):
            for turns in af.interactions[(0, iplayer)]:
                self.assertEqual(len(turns), 5)
                self.assertTrue(all(t == (C, C) for t in turns))
        self.assertEqual(af.data[Point(0.0, 0.0)], 3.0)
        self.assertEqual(af.data[Point(0.5, 0.0)], 3.0)
        self.assertEqual(af.data[Point(1.0, 0.0)], 3.0)

        # Player 3 is Point(0.0, 1.0) which implies defection after the
        # first turn since Tit-for-Tat is playing, and a score of 0.8
        # since we get zero on first turn and one point per turn later.
        for turns in af.interactions[(0, 3)]:
            self.assertEqual(len(turns), 5)
            self.assertTrue(all(t == (D, D) for t in turns[1:]))
        self.assertAlmostEqual(af.data[Point(0.0, 1.0)], 0.8)

    def test_progress_bar_fingerprint(self):
        af = AshlockFingerprint(axl.TitForTat)
        data = af.fingerprint(turns=10, repetitions=2, step=0.5, progress_bar=True)
        self.assertEqual(sorted(data.keys()), self.points_when_using_half_step)

    @patch("axelrod.fingerprint.mkstemp", RecordedMksTemp.mkstemp)
    def test_temp_file_creation(self):

        RecordedMksTemp.reset_record()
        af = AshlockFingerprint(axl.TitForTat)
        path = pathlib.Path("test_outputs/test_fingerprint.csv")
        filename = axl_filename(path)

        self.assertEqual(RecordedMksTemp.record, [])

        # Temp file is created and destroyed.
        af.fingerprint(
            turns=1, repetitions=1, step=0.5, progress_bar=False, filename=None
        )

        self.assertEqual(len(RecordedMksTemp.record), 1)
        filename = RecordedMksTemp.record[0][1]
        self.assertIsInstance(filename, str)
        self.assertNotEqual(filename, "")
        self.assertFalse(os.path.isfile(filename))

    def test_fingerprint_with_filename(self):
        path = pathlib.Path("test_outputs/test_fingerprint.csv")
        filename = axl_filename(path)
        af = AshlockFingerprint(axl.TitForTat)
        af.fingerprint(
            turns=1, repetitions=1, step=0.5, progress_bar=False, filename=filename
        )
        with open(filename, "r") as out:
            data = out.read()
            self.assertEqual(len(data.split("\n")), 20)

    def test_serial_fingerprint(self):
        af = AshlockFingerprint(axl.TitForTat)
        data = af.fingerprint(turns=10, repetitions=2, step=0.5, progress_bar=False)
        edge_keys = sorted(list(af.interactions.keys()))
        coord_keys = sorted(list(data.keys()))
        self.assertEqual(af.step, 0.5)
        self.assertEqual(edge_keys, self.edges_when_using_half_step)
        self.assertEqual(coord_keys, self.points_when_using_half_step)

    def test_parallel_fingerprint(self):
        af = AshlockFingerprint(axl.TitForTat)
        af.fingerprint(
            turns=10, repetitions=2, step=0.5, processes=2, progress_bar=False
        )
        edge_keys = sorted(list(af.interactions.keys()))
        coord_keys = sorted(list(af.data.keys()))
        self.assertEqual(af.step, 0.5)
        self.assertEqual(edge_keys, self.edges_when_using_half_step)
        self.assertEqual(coord_keys, self.points_when_using_half_step)

    def test_plot_data(self):
        axl.seed(0)  # Fingerprinting is a random process.
        af = AshlockFingerprint(axl.Cooperator())
        af.fingerprint(turns=5, repetitions=3, step=0.5, progress_bar=False)

        reshaped_data = np.array([[0.0, 0.0, 0.0], [2.0, 1.0, 2.0], [3.0, 3.0, 3.0]])
        plotted_data = af.plot().gca().images[0].get_array()
        np.testing.assert_allclose(plotted_data, reshaped_data)

    def test_plot_figure(self):
        af = AshlockFingerprint(axl.WinStayLoseShift, axl.TitForTat)
        af.fingerprint(turns=10, repetitions=2, step=0.25, progress_bar=False)
        p = af.plot()
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
        q = af.plot(cmap="jet")
        self.assertIsInstance(q, matplotlib.pyplot.Figure)
        r = af.plot(interpolation="bicubic")
        self.assertIsInstance(r, matplotlib.pyplot.Figure)
        t = af.plot(title="Title")
        self.assertIsInstance(t, matplotlib.pyplot.Figure)
        u = af.plot(colorbar=False)
        self.assertIsInstance(u, matplotlib.pyplot.Figure)
        v = af.plot(labels=False)
        self.assertIsInstance(v, matplotlib.pyplot.Figure)

    def test_wsls_fingerprint(self):
        axl.seed(0)  # Fingerprinting is a random process.
        test_data = {
            Point(x=0.0, y=0.0): 3.000,
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
            Point(x=1.0, y=1.0): 1.300,
        }
        af = axl.AshlockFingerprint(axl.WinStayLoseShift(), axl.TitForTat)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25, progress_bar=False)

        for key, value in data.items():
            self.assertAlmostEqual(value, test_data[key], places=2)

    def test_tft_fingerprint(self):
        axl.seed(0)  # Fingerprinting is a random process.
        test_data = {
            Point(x=0.0, y=0.0): 3.000,
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
            Point(x=1.0, y=1.0): 2.180,
        }

        af = axl.AshlockFingerprint(axl.TitForTat(), axl.TitForTat)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25, progress_bar=False)

        for key, value in data.items():
            self.assertAlmostEqual(value, test_data[key], places=2)

    def test_majority_fingerprint(self):
        axl.seed(0)  # Fingerprinting is a random process.
        test_data = {
            Point(x=0.0, y=0.0): 3.000,
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
            Point(x=1.0, y=1.0): 2.260,
        }

        af = axl.AshlockFingerprint(axl.GoByMajority, axl.TitForTat)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25, progress_bar=False)

        for key, value in data.items():
            self.assertAlmostEqual(value, test_data[key], places=2)

    @given(strategy_pair=strategy_lists(min_size=2, max_size=2))
    @settings(max_examples=5)
    def test_pair_fingerprints(self, strategy_pair):
        """
        A test to check that we can fingerprint
        with any two given strategies or instances
        """
        strategy, probe = strategy_pair
        af = AshlockFingerprint(strategy, probe)
        data = af.fingerprint(turns=2, repetitions=2, step=0.5, progress_bar=False)
        self.assertIsInstance(data, dict)

        af = AshlockFingerprint(strategy(), probe)
        data = af.fingerprint(turns=2, repetitions=2, step=0.5, progress_bar=False)
        self.assertIsInstance(data, dict)

        af = AshlockFingerprint(strategy, probe())
        data = af.fingerprint(turns=2, repetitions=2, step=0.5, progress_bar=False)
        self.assertIsInstance(data, dict)

        af = AshlockFingerprint(strategy(), probe())
        data = af.fingerprint(turns=2, repetitions=2, step=0.5, progress_bar=False)
        self.assertIsInstance(data, dict)


class TestTransitiveFingerprint(unittest.TestCase):
    def test_init(self):
        player = axl.TitForTat()
        fingerprint = axl.TransitiveFingerprint(strategy=player)
        self.assertEqual(fingerprint.strategy, player)
        self.assertEqual(
            fingerprint.opponents, [axl.Random(p) for p in np.linspace(0, 1, 50)]
        )

    def test_init_with_opponents(self):
        player = axl.TitForTat()
        opponents = [s() for s in axl.demo_strategies]
        fingerprint = axl.TransitiveFingerprint(strategy=player, opponents=opponents)
        self.assertEqual(fingerprint.strategy, player)
        self.assertEqual(fingerprint.opponents, opponents)

    def test_init_with_not_default_number(self):
        player = axl.TitForTat()
        number_of_opponents = 10
        fingerprint = axl.TransitiveFingerprint(
            strategy=player, number_of_opponents=number_of_opponents
        )
        self.assertEqual(fingerprint.strategy, player)
        self.assertEqual(
            fingerprint.opponents, [axl.Random(p) for p in np.linspace(0, 1, 10)]
        )

    def test_fingerprint_with_filename(self):
        path = pathlib.Path("test_outputs/test_fingerprint.csv")
        filename = axl_filename(path)
        strategy = axl.TitForTat()
        tf = TransitiveFingerprint(strategy)
        tf.fingerprint(turns=1, repetitions=1, progress_bar=False, filename=filename)
        with open(filename, "r") as out:
            data = out.read()
            self.assertEqual(len(data.split("\n")), 102)

    def test_serial_fingerprint(self):
        strategy = axl.TitForTat()
        tf = TransitiveFingerprint(strategy)
        path = pathlib.Path("test_outputs/test_fingerprint.csv")
        tf.fingerprint(
            repetitions=1,
            progress_bar=False,
            filename=axl_filename(path),
        )
        self.assertEqual(tf.data.shape, (50, 50))

    def test_parallel_fingerprint(self):
        strategy = axl.TitForTat()
        tf = TransitiveFingerprint(strategy)
        tf.fingerprint(repetitions=1, progress_bar=False, processes=2)

        self.assertEqual(tf.data.shape, (50, 50))

    def test_analyse_cooperation_ratio(self):
        tf = TransitiveFingerprint(axl.TitForTat)
        path = pathlib.Path("test_outputs/test_fingerprint.csv")
        filename = axl_filename(path)
        with open(filename, "w") as f:
            f.write(
                """Interaction index,Player index,Opponent index,Repetition,Player name,Opponent name,Actions
0,0,1,0,Player0,Player1,CCC
0,1,0,0,Player1,Player0,DDD
1,0,1,1,Player0,Player1,CCC
1,1,0,1,Player1,Player0,DDD
2,0,2,0,Player0,Player2,CCD
2,2,0,0,Player2,Player0,DDD
3,0,2,1,Player0,Player2,CCC
3,2,0,1,Player2,Player0,DDD
4,0,3,0,Player0,Player3,CCD
4,3,0,0,Player3,Player0,DDD
5,0,3,1,Player0,Player3,DCC
5,3,0,1,Player3,Player0,DDD
6,0,4,2,Player0,Player4,DDD
6,4,0,2,Player4,Player0,DDD
7,0,4,3,Player0,Player4,DDD
7,4,0,3,Player4,Player0,DDD"""
            )
        data = tf.analyse_cooperation_ratio(filename)
        expected_data = np.array(
            [[1, 1, 1], [1, 1, 1 / 2], [1 / 2, 1, 1 / 2], [0, 0, 0]]
        )
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
        p = tf.plot(interpolation="bicubic")
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
        p = tf.plot(title="Title")
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
        p = tf.plot(colorbar=False)
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
        p = tf.plot(labels=False)
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
        p = tf.plot(display_names=True)
        self.assertIsInstance(p, matplotlib.pyplot.Figure)

    def test_plot_with_axis(self):
        fig, axarr = matplotlib.pyplot.subplots(2, 2)
        tf = TransitiveFingerprint(axl.TitForTat)
        tf.fingerprint(turns=10, repetitions=2, progress_bar=False)
        p = tf.plot(ax=axarr[0, 0])
        self.assertIsInstance(p, matplotlib.pyplot.Figure)
