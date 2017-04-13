import unittest
import axelrod as axl
from hypothesis import given
from axelrod.fingerprint import (AshlockFingerprint, Point, create_player,
                                 get_class_and_kwargs)
from axelrod.tests.property import strategy_lists


matplotlib_installed = True
try:
    import matplotlib.pyplot
except ImportError:  # pragma: no cover
    matplotlib_installed = False


C, D = axl.Actions.C, axl.Actions.D


class TestFingerprint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.strategy = axl.WinStayLoseShift
        cls.probe_class = axl.TitForTat
        cls.expected_points = [(0.0, 0.0), (0.0, 0.5), (0.0, 1.0),
                               (0.5, 0.0), (0.5, 0.5), (0.5, 1.0),
                               (1.0, 0.0), (1.0, 0.5), (1.0, 1.0)]
        cls.expected_edges = [(0, 1), (0, 2), (0, 3),
                              (0, 4), (0, 5), (0, 6),
                              (0, 7), (0, 8), (0, 9)]

        cls.score_matrix = {(C, C): 3, (C, D): 0, (D, C): 5, (D, D): 1}

    def test_create_player_from_instance(self):
        new_player = create_player(axl.Cycler('DDD'))
        self.assertIsInstance(new_player, axl.Cycler)
        self.assertEqual(new_player.init_kwargs, {'cycle': 'DDD'})

    def test_create_player_from_class(self):
        new_player = create_player(axl.Cycler)
        self.assertIsInstance(new_player, axl.Cycler)
        self.assertEqual(new_player.init_kwargs, axl.Cycler().init_kwargs)

    def test_get_class_and_kwargs_from_instance(self):
        strategy, kwargs = get_class_and_kwargs(axl.Cycler('DDD'))
        self.assertEqual(strategy, axl.Cycler)
        self.assertEqual(kwargs, {'cycle': 'DDD'})

    def test_get_class_and_kwargs_from_class(self):
        strategy, kwargs = get_class_and_kwargs(axl.Cycler)
        self.assertEqual(strategy, axl.Cycler)
        self.assertEqual(kwargs, axl.Cycler().init_kwargs)

    def test_default_init(self):
        fp = AshlockFingerprint(self.strategy)
        self.assertIsInstance(fp.player, self.strategy)
        self.assertIsInstance(fp.probe, self.probe_class)
        self.assertEqual(fp.step, 0.01)
        self.assertEqual(fp.progress_bar, True)
        expected_default_points = [Point(x * 0.01, y * 0.01)
                                   for x in range(101)
                                   for y in range(101)]
        self.assertEqual(fp.points, expected_default_points)
        self.assertEqual(str(fp._probe_list[0]),
                         'Joss-Ann Tit For Tat: (0.0, 0.0)')
        self.assertEqual(str(fp._probe_list[-1]),
                         'Dual Joss-Ann Tit For Tat: (0.0, 0.0)')

    def test_init_set_step(self):
        fp = AshlockFingerprint(self.strategy, step=0.5)
        self.assertEqual(fp.points, self.expected_points)
        self.assertEqual(len(fp.points), 9)
        self.assertEqual(len(fp._probe_list), 9)

    def test_init_set_step_rounds_step_up_to_nearest(self):
        fp = AshlockFingerprint(self.strategy, step=0.4)
        step_zero_pt_five = self.expected_points[:]
        self.assertEqual(fp.points, step_zero_pt_five)
        self.assertEqual(fp.step, 0.5)

        fp = AshlockFingerprint(self.strategy, step=0.51)
        self.assertEqual(fp.points,
                         [Point(0.0, 0.0), Point(0.0, 1.0),
                          Point(1.0, 0.0), Point(1.0, 1.0)])
        self.assertEqual(fp.step, 1.0)

    def test_init_set_progress_bar(self):
        fp = AshlockFingerprint(self.strategy, step=0.5, progress_bar=False)
        self.assertFalse(fp.progress_bar)

    def test_init_set_probe_as_class(self):
        fp = AshlockFingerprint(self.strategy, step=0.5, probe=axl.Cooperator)
        self.assertIsInstance(fp.probe, axl.Cooperator)

    def test_init_set_probe_as_instance(self):
        probe = axl.Cycler('CCC')
        fp = AshlockFingerprint(self.strategy, step=0.5, probe=probe)
        self.assertEqual(str(fp.probe), 'Cycler: CCC')
        self.assertEqual(str(fp._probe_list[0]),
                         'Joss-Ann Cycler: CCC: (0.0, 0.0)')

    def test_init_set_strategy_as_instance(self):
        player = axl.Cycler('DDD')
        fp = AshlockFingerprint(player, step=0.5)
        self.assertEqual(str(fp.player), 'Cycler: DDD')

    def test_step_setter(self):
        fp = AshlockFingerprint(self.strategy, step=0.25)
        self.assertNotEqual(fp.points, self.expected_points)
        self.assertEqual(len(fp.points), 25)
        self.assertEqual(len(fp._probe_list), 25)
        self.assertEqual(str(fp._probe_list[1]),
                         'Joss-Ann Tit For Tat: (0.0, 0.25)')

        fp.step = 0.5
        self.assertEqual(fp.points, self.expected_points)
        self.assertEqual(len(fp.points), 9)
        self.assertEqual(len(fp._probe_list), 9)
        self.assertEqual(str(fp._probe_list[1]),
                         'Joss-Ann Tit For Tat: (0.0, 0.5)')

    def test_probe_setter(self):
        fp = AshlockFingerprint(self.strategy, step=0.5)
        fp.probe = axl.Cooperator
        self.assertIsInstance(fp.probe, axl.Cooperator)
        self.assertEqual(str(fp._probe_list[1]),
                         'Joss-Ann Cooperator: (0.0, 0.5)')
        for probe in fp._probe_list:
            self.assertIn('Cooperator', str(probe))

    def test_probe_list_maps_to_points(self):
        """probe is Joss-AnnTitForTat(x, y) if x + y < 1. Else is
        DualJoss-AnnTitForTat(1-x, 1-y)"""
        expected_point_probe_str = {
            Point(0.0, 0.0): 'Joss-Ann Tit For Tat: (0.0, 0.0)',
            Point(0.0, 0.5): 'Joss-Ann Tit For Tat: (0.0, 0.5)',
            Point(0.0, 1.0): 'Dual Joss-Ann Tit For Tat: (1.0, 0.0)',
            Point(0.5, 0.0): 'Joss-Ann Tit For Tat: (0.5, 0.0)',
            Point(0.5, 0.5): 'Dual Joss-Ann Tit For Tat: (0.5, 0.5)',
            Point(0.5, 1.0): 'Dual Joss-Ann Tit For Tat: (0.5, 0.0)',
            Point(1.0, 0.0): 'Dual Joss-Ann Tit For Tat: (0.0, 1.0)',
            Point(1.0, 0.5): 'Dual Joss-Ann Tit For Tat: (0.0, 0.5)',
            Point(1.0, 1.0): 'Dual Joss-Ann Tit For Tat: (0.0, 0.0)',
        }
        fp = AshlockFingerprint(self.strategy, step=0.5)
        probe_strings = [str(probe) for probe in fp._probe_list]
        from_fp = dict(zip(fp.points, probe_strings))
        self.assertEqual(expected_point_probe_str, from_fp)

    def test_interactions_maps_to_probe_list(self):
        turns = 50
        repetitions = 2
        seed = 0
        fp = AshlockFingerprint(self.strategy, step=0.5)

        axl.seed(seed)
        fp.fingerprint(turns=turns, repetitions=repetitions, in_memory=True)

        players = [fp.player] + fp._probe_list
        edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5),  # player plays each
                 (0, 6), (0, 7), (0, 8), (0, 9)]  # probe in order one time
        tournament = axl.SpatialTournament(players, edges=edges, turns=turns,
                                           repetitions=repetitions)

        axl.seed(seed)
        tournament.play(in_memory=True)

        self.assertEqual(fp.interactions, tournament.interactions_dict)

    def test_data_maps_back_to_points(self):
        turns = 50
        one_rep_only = 1
        seed = 0
        fp = AshlockFingerprint(self.strategy, step=0.5)

        axl.seed(seed)
        fp.fingerprint(turns=turns, repetitions=one_rep_only, in_memory=True)

        players = [fp.player] + fp._probe_list
        edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5),  # player plays each
                 (0, 6), (0, 7), (0, 8), (0, 9)]  # probe in order one time
        tournament = axl.SpatialTournament(players, edges=edges, turns=turns,
                                           repetitions=one_rep_only)

        axl.seed(seed)
        tournament.play(in_memory=True)

        avg_scores = {}
        for edge, matches in tournament.interactions_dict.items():
            only_match = matches[0]
            scores = [self.score_matrix[match_val] for match_val in only_match]
            avg = sum(scores)/len(scores)
            avg_scores[edge] = avg

        edges_to_points = dict(zip(edges, fp.points))

        for edge, avg in avg_scores.items():
            data_avg = fp.data[edges_to_points[edge]]
            self.assertAlmostEqual(data_avg, avg, places=5)

    def test_data_gets_average(self):
        axl.seed(0)
        fp = AshlockFingerprint(self.strategy, step=0.5)
        fp.fingerprint(turns=5, repetitions=5)

        expected_midpoint = [
            [(C, D), (D, C), (D, D), (C, D), (D, D)],
            [(C, D), (D, C), (D, D), (C, D), (D, D)],
            [(C, D), (D, C), (D, D), (C, D), (D, D)],
            [(C, D), (D, C), (D, D), (C, D), (D, D)],
            [(C, D), (D, C), (D, D), (C, D), (D, D)]
        ]

        self.assertEqual(fp.interactions[(0, 5)], expected_midpoint)

        flattened_midpoint_matches = []
        for match in expected_midpoint:
            flattened_midpoint_matches += match
        midpoint_scores = [self.score_matrix[play]
                           for play in flattened_midpoint_matches]
        avg_score = sum(midpoint_scores) / len(midpoint_scores)

        self.assertEqual(fp.data[Point(0.5, 0.5)], avg_score)

    def test_fingerprint_with_filename(self):
        filename = "test_outputs/test_fingerprint.csv"
        af = AshlockFingerprint(self.strategy, probe=self.probe_class, step=0.5,
                                progress_bar=False)
        af.fingerprint(turns=1, repetitions=1, filename=filename)
        with open(filename, 'r') as out:
            data = out.read()
            self.assertEqual(len(data.split("\n")), 10)

    def test_in_memory_fingerprint(self):
        af = AshlockFingerprint(self.strategy, probe=self.probe_class, step=0.5,
                                progress_bar=False)
        af.fingerprint(turns=10, repetitions=2, in_memory=True)
        edge_keys = sorted(list(af.interactions.keys()))
        coord_keys = sorted(list(af.data.keys()))
        self.assertEqual(af._step, 0.5)
        self.assertEqual(af.spatial_tournament.interactions_dict,
                         af.interactions)
        self.assertEqual(edge_keys, self.expected_edges)
        self.assertEqual(coord_keys, self.expected_points)

    @unittest.skipIf(axl.on_windows,
                     "Parallel processing not supported on Windows")
    def test_parallel_fingerprint(self):
        af = AshlockFingerprint(self.strategy, self.probe_class, step=0.5)
        af.fingerprint(turns=10, repetitions=2, processes=2)
        edge_keys = sorted(list(af.interactions.keys()))
        coord_keys = sorted(list(af.data.keys()))
        self.assertEqual(af.step, 0.5)
        self.assertEqual(edge_keys, self.expected_edges)
        self.assertEqual(coord_keys, self.expected_points)

    def test_reshape_data(self):
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
        af = AshlockFingerprint(self.strategy, step=0.5, progress_bar=False)
        af.data = test_data.copy()

        plotting_data = af._reshape_data()

        for i in range(len(plotting_data)):
            self.assertEqual(list(plotting_data[i]), test_shaped_data[i])

    def test_plot(self):
        af = AshlockFingerprint(self.strategy, self.probe_class,
                                step=0.25, progress_bar=False)
        af.fingerprint(turns=10, repetitions=2)
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

    def test_wsls_fingerprint_and_progress_bar(self):
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

        af = axl.AshlockFingerprint(self.strategy, self.probe_class,
                                    step=0.25, progress_bar=True)
        data = af.fingerprint(turns=50, repetitions=2)

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
        af = axl.AshlockFingerprint(axl.TitForTat, self.probe_class,
                                    step=0.25, progress_bar=False)
        data = af.fingerprint(turns=50, repetitions=2)

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
        af = axl.AshlockFingerprint(axl.GoByMajority, self.probe_class,
                                    step=0.25, progress_bar=False)
        data = af.fingerprint(turns=50, repetitions=2)

        for key, value in data.items():
            self.assertAlmostEqual(value, test_data[key])

    @given(strategy_pair=strategy_lists(min_size=2, max_size=2))
    def test_pair_fingerprints(self, strategy_pair):
        """
        A test to check that we can fingerprint
        with any two given strategies or instances
        """
        strategy, probe = strategy_pair
        af = AshlockFingerprint(strategy, probe, step=1.0, progress_bar=False)
        data = af.fingerprint(turns=2, repetitions=2)
        self.assertIsInstance(data, dict)

        af = AshlockFingerprint(strategy(), probe, step=1.0, progress_bar=False)
        data = af.fingerprint(turns=2, repetitions=2)
        self.assertIsInstance(data, dict)

        af = AshlockFingerprint(strategy, probe(), step=1.0, progress_bar=False)
        data = af.fingerprint(turns=2, repetitions=2)
        self.assertIsInstance(data, dict)

        af = AshlockFingerprint(strategy(), probe(), step=1.0,
                                progress_bar=False)
        data = af.fingerprint(turns=2, repetitions=2)
        self.assertIsInstance(data, dict)
