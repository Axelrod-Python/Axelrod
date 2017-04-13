import unittest
import axelrod as axl
from hypothesis import given
from axelrod.fingerprint import AshlockFingerprint, Point
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

    # def assert_match_only_c(self, interactions_value):
    #     """match against Cooperator"""
    #     match = interactions_value[0]
    #     self.assertTrue(all(match_tuple == (C, C) for match_tuple in match))
    #
    # def assert_match_only_d(self, interactions_value):
    #     """match against Cooperator"""
    #     match = interactions_value[0]
    #     self.assertTrue(all(match_tuple == (C, D) for match_tuple in match))
    #
    # def assert_match_c_and_d(self, interactions_value):
    #     """match against Cooperator"""
    #     match = interactions_value[0]
    #     self.assertIn((C, C), match)
    #     self.assertIn((C, D), match)
    #
    # def test_assert_match_only_c(self):
    #     only_c = [[(C, C), (C, C), (C, C)]]
    #     mixed = [[(C, C), (C, D), (C, C)]]
    #     only_d = [[(C, D), (C, D), (C, D)]]
    #
    #     self.assertIsNone(self.assert_match_only_c(only_c))
    #     self.assertRaises(AssertionError, self.assert_match_only_c, mixed)
    #     self.assertRaises(AssertionError, self.assert_match_only_c, only_d)
    #
    # def test_assert_match_only_d(self):
    #     only_c = [[(C, C), (C, C), (C, C)]]
    #     mixed = [[(C, C), (C, D), (C, C)]]
    #     only_d = [[(C, D), (C, D), (C, D)]]
    #
    #     self.assertIsNone(self.assert_match_only_d(only_d))
    #     self.assertRaises(AssertionError, self.assert_match_only_d, mixed)
    #     self.assertRaises(AssertionError, self.assert_match_only_d, only_c)
    #
    # def test_assert_match_c_and_d(self):
    #     only_c = [[(C, C), (C, C), (C, C)]]
    #     mixed = [[(C, C), (C, D), (C, C)]]
    #     only_d = [[(C, D), (C, D), (C, D)]]
    #
    #     self.assertIsNone(self.assert_match_c_and_d(mixed))
    #     self.assertRaises(AssertionError, self.assert_match_c_and_d, only_c)
    #     self.assertRaises(AssertionError, self.assert_match_c_and_d, only_d)

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
        self.assertEqual(len(fp.points), len(fp._probe_list))

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



        #
        # for probe in fp._probe_list:
        #     print(probe)
    #
    # def test_init_with_instance(self):
    #     player = self.strategy()
    #     fingerprint = AshlockFingerprint(player, step=0.5)
    #     self.assertEqual(fingerprint.player, player)
    #     self.assertEqual(fingerprint.probe.__class__, self.probe_class)
    #
    #     probe_player = self.probe_class()
    #     fingerprint = AshlockFingerprint(self.strategy, probe_player, step=0.5)
    #     self.assertEqual(fingerprint.player.__class__, self.strategy)
    #     self.assertEqual(fingerprint.probe.__class__, probe_player.__class__)
    #     self.assertEqual(fingerprint.probe.init_kwargs,
    #                      probe_player.init_kwargs)
    #
    #     fingerprint = AshlockFingerprint(player, probe_player, step=0.5)
    #     self.assertEqual(fingerprint.player, player)
    #     self.assertEqual(fingerprint.probe.__class__, probe_player.__class__)
    #     self.assertEqual(fingerprint.probe.init_kwargs,
    #                      probe_player.init_kwargs)
    #
    # def test_create_jossann(self):
    #     fingerprint = AshlockFingerprint(self.strategy, step=0.5)
    #
    #     # x + y < 1
    #     ja = fingerprint._create_jossann((.5, .4))
    #     self.assertEqual(str(ja), "Joss-Ann Tit For Tat: (0.5, 0.4)")
    #
    #     # x + y = 1
    #     ja = fingerprint._create_jossann((.4, .6))
    #     self.assertEqual(str(ja), "Dual Joss-Ann Tit For Tat: (0.6, 0.4)")
    #
    #     # x + y > 1
    #     ja = fingerprint._create_jossann((.5, .6))
    #     self.assertEqual(str(ja), "Dual Joss-Ann Tit For Tat: (0.5, 0.4)")
    #
    # def test_create_points(self):
    #     test_points = create_points(0.5, progress_bar=False)
    #     self.assertEqual(test_points, self.expected_points)
    #
    # def test_create_probes(self):
    #     af = AshlockFingerprint(self.strategy, self.probe_class, step=0.5)
    #     probes = af._create_probes()
    #     self.assertEqual(len(probes), 9)
    #
    # def test_create_edges(self):
    #     af = AshlockFingerprint(self.strategy, self.probe_class, step=0.5)
    #     edges = af._create_edges()
    #     self.assertEqual(edges, self.expected_edges)
    #
    # # def test_construct_tournament_elemets(self):
    # #     af = AshlockFingerprint(self.strategy, self.probe, step=0.5)
    # #     edges, tournament_players = af._construct_tournament_elements()
    # #     self.assertEqual(edges, self.expected_edges)
    # #     self.assertEqual(len(tournament_players), 10)
    # #     self.assertEqual(tournament_players[0].__class__, af.player.__class__)
    #
    # def test_progress_bar_fingerprint(self):
    #     af = AshlockFingerprint(self.strategy, self.probe_class, step=0.5)
    #     data = af.fingerprint(turns=10, repetitions=2, progress_bar=True)
    #     self.assertEqual(sorted(data.keys()), self.expected_points)

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
    #
    # def test_serial_fingerprint(self):
    #     af = AshlockFingerprint(self.strategy, self.probe_class, step=0.5)
    #     data = af.fingerprint(turns=10, repetitions=2, progress_bar=False)
    #     edge_keys = sorted(list(af.interactions.keys()))
    #     coord_keys = sorted(list(data.keys()))
    #     self.assertEqual(af._step, 0.5)
    #     self.assertEqual(edge_keys, self.expected_edges)
    #     self.assertEqual(coord_keys, self.expected_points)
    #
    # @unittest.skipIf(axl.on_windows,
    #                  "Parallel processing not supported on Windows")
    # def test_parallel_fingerprint(self):
    #     af = AshlockFingerprint(self.strategy, self.probe_class, step=0.5)
    #     af.fingerprint(turns=10, repetitions=2, processes=2,
    #                    progress_bar=False)
    #     edge_keys = sorted(list(af.interactions.keys()))
    #     coord_keys = sorted(list(af.data.keys()))
    #     self.assertEqual(af._step, 0.5)
    #     self.assertEqual(edge_keys, self.expected_edges)
    #     self.assertEqual(coord_keys, self.expected_points)




    # def test_generate_data(self):
    #     af = AshlockFingerprint(self.strategy, self.probe, step=0.5)
    #     edges, players = af.construct_tournament_elements()
    #     spatial_tournament = axl.SpatialTournament(players,
    #                                                turns=10,
    #                                                repetitions=2,
    #                                                edges=edges)
    #     results = spatial_tournament.play(progress_bar=False,
    #                                       keep_interactions=True)
    #     data = af.generate_data(edges=self.expected_edges)
    #     keys = sorted(list(data.keys()))
    #     values = [0 < score < 5 for score in data.values()]
    #     self.assertEqual(sorted(keys), self.expected_points)
    #     self.assertEqual(all(values), True)

    # def test_reshape_data(self):
    #     test_points = [Point(x=0.0, y=0.0),
    #                    Point(x=0.0, y=0.5),
    #                    Point(x=0.0, y=1.0),
    #                    Point(x=0.5, y=0.0),
    #                    Point(x=0.5, y=0.5),
    #                    Point(x=0.5, y=1.0),
    #                    Point(x=1.0, y=0.0),
    #                    Point(x=1.0, y=0.5),
    #                    Point(x=1.0, y=1.0)]
    #     test_data = {Point(x=0.0, y=0.0): 5,
    #                  Point(x=0.0, y=0.5): 9,
    #                  Point(x=0.0, y=1.0): 3,
    #                  Point(x=0.5, y=0.0): 8,
    #                  Point(x=0.5, y=0.5): 2,
    #                  Point(x=0.5, y=1.0): 4,
    #                  Point(x=1.0, y=0.0): 2,
    #                  Point(x=1.0, y=0.5): 1,
    #                  Point(x=1.0, y=1.0): 9}
    #     test_shaped_data = [[3, 4, 9],
    #                         [9, 2, 1],
    #                         [5, 8, 2]]
    #     af = AshlockFingerprint(self.strategy, self.probe, step=0.5)
    #     af.fingerprint(turns=3, repetitions=1)
    #     plotting_data = af.reshape_data(test_data, test_points, 3)
    #     self.assertEqual(af.points, test_points)
    #     self.assertEqual(af.data, test_data)
    #
    #     for i in range(len(plotting_data)):
    #         self.assertEqual(list(plotting_data[i]), test_shaped_data[i])




    # def test_plot(self):
    #     af = AshlockFingerprint(self.strategy, self.probe_class,
    #                             step=0.25, progress_bar=False)
    #     af.fingerprint(turns=10, repetitions=2, progress_bar=False)
    #     p = af.plot()
    #     self.assertIsInstance(p, matplotlib.pyplot.Figure)
    #     q = af.plot(col_map='jet')
    #     self.assertIsInstance(q, matplotlib.pyplot.Figure)
    #     r = af.plot(interpolation='bicubic')
    #     self.assertIsInstance(r, matplotlib.pyplot.Figure)
    #     t = af.plot(title='Title')
    #     self.assertIsInstance(t, matplotlib.pyplot.Figure)
    #     u = af.plot(colorbar=False)
    #     self.assertIsInstance(u, matplotlib.pyplot.Figure)
    #     v = af.plot(labels=False)
    #     self.assertIsInstance(v, matplotlib.pyplot.Figure)
    #
    # def test_wsls_fingerprint(self):
    #     axl.seed(0)  # Fingerprinting is a random process
    #     test_data = {Point(x=0.0, y=0.0): 3.0,
    #                  Point(x=0.0, y=0.25): 1.46,
    #                  Point(x=0.0, y=0.5): 1.54,
    #                  Point(x=0.0, y=0.75): 1.12,
    #                  Point(x=0.0, y=1.0): 0.5,
    #                  Point(x=0.25, y=0.0): 3.0,
    #                  Point(x=0.25, y=0.25): 2.04,
    #                  Point(x=0.25, y=0.5): 2.0,
    #                  Point(x=0.25, y=0.75): 1.34,
    #                  Point(x=0.25, y=1.0): 0.9,
    #                  Point(x=0.5, y=0.0): 3.0,
    #                  Point(x=0.5, y=0.25): 3.0,
    #                  Point(x=0.5, y=0.5): 2.06,
    #                  Point(x=0.5, y=0.75): 1.36,
    #                  Point(x=0.5, y=1.0): 1.0,
    #                  Point(x=0.75, y=0.0): 3.0,
    #                  Point(x=0.75, y=0.25): 3.56,
    #                  Point(x=0.75, y=0.5): 2.06,
    #                  Point(x=0.75, y=0.75): 3.0,
    #                  Point(x=0.75, y=1.0): 1.04,
    #                  Point(x=1.0, y=0.0): 3.0,
    #                  Point(x=1.0, y=0.25): 4.86,
    #                  Point(x=1.0, y=0.5): 4.9,
    #                  Point(x=1.0, y=0.75): 4.9,
    #                  Point(x=1.0, y=1.0): 1.3}
    #
    #     af = axl.AshlockFingerprint(self.strategy, self.probe_class,
    #                                 step=0.25, progress_bar=False)
    #     data = af.fingerprint(turns=50, repetitions=2)
    #
    #     for key, value in data.items():
    #         self.assertAlmostEqual(value, test_data[key])
    #
    # def test_tft_fingerprint(self):
    #     axl.seed(0)  # Fingerprinting is a random process
    #     test_data = {Point(x=0.0, y=0.0): 3.0,
    #                  Point(x=0.0, y=0.25): 1.1,
    #                  Point(x=0.0, y=0.5): 1.08,
    #                  Point(x=0.0, y=0.75): 1.04,
    #                  Point(x=0.0, y=1.0): 0.98,
    #                  Point(x=0.25, y=0.0): 3.0,
    #                  Point(x=0.25, y=0.25): 2.26,
    #                  Point(x=0.25, y=0.5): 2.1,
    #                  Point(x=0.25, y=0.75): 1.66,
    #                  Point(x=0.25, y=1.0): 1.64,
    #                  Point(x=0.5, y=0.0): 3.0,
    #                  Point(x=0.5, y=0.25): 2.5,
    #                  Point(x=0.5, y=0.5): 2.12,
    #                  Point(x=0.5, y=0.75): 1.86,
    #                  Point(x=0.5, y=1.0): 1.88,
    #                  Point(x=0.75, y=0.0): 3.0,
    #                  Point(x=0.75, y=0.25): 2.84,
    #                  Point(x=0.75, y=0.5): 2.36,
    #                  Point(x=0.75, y=0.75): 2.28,
    #                  Point(x=0.75, y=1.0): 1.98,
    #                  Point(x=1.0, y=0.0): 3.0,
    #                  Point(x=1.0, y=0.25): 2.78,
    #                  Point(x=1.0, y=0.5): 2.56,
    #                  Point(x=1.0, y=0.75): 2.44,
    #                  Point(x=1.0, y=1.0): 2.18}
    #     af = axl.AshlockFingerprint(axl.TitForTat, self.probe_class,
    #                                 step=0.25, progress_bar=False)
    #     data = af.fingerprint(turns=50, repetitions=2)
    #
    #     for key, value in data.items():
    #         self.assertAlmostEqual(value, test_data[key])
    #
    # def test_majority_fingerprint(self):
    #     axl.seed(0)  # Fingerprinting is a random process
    #     test_data = {Point(x=0.0, y=0.0): 3.0,
    #                  Point(x=0.0, y=0.25): 1.18,
    #                  Point(x=0.0, y=0.5): 1.98,
    #                  Point(x=0.0, y=0.75): 1.04,
    #                  Point(x=0.0, y=1.0): 0.98,
    #                  Point(x=0.25, y=0.0): 3.0,
    #                  Point(x=0.25, y=0.25): 2.16,
    #                  Point(x=0.25, y=0.5): 1.74,
    #                  Point(x=0.25, y=0.75): 1.96,
    #                  Point(x=0.25, y=1.0): 2.24,
    #                  Point(x=0.5, y=0.0): 3.0,
    #                  Point(x=0.5, y=0.25): 2.46,
    #                  Point(x=0.5, y=0.5): 2.44,
    #                  Point(x=0.5, y=0.75): 2.24,
    #                  Point(x=0.5, y=1.0): 2.74,
    #                  Point(x=0.75, y=0.0): 3.0,
    #                  Point(x=0.75, y=0.25): 2.52,
    #                  Point(x=0.75, y=0.5): 2.16,
    #                  Point(x=0.75, y=0.75): 2.1,
    #                  Point(x=0.75, y=1.0): 2.44,
    #                  Point(x=1.0, y=0.0): 3.0,
    #                  Point(x=1.0, y=0.25): 2.22,
    #                  Point(x=1.0, y=0.5): 1.64,
    #                  Point(x=1.0, y=0.75): 2.08,
    #                  Point(x=1.0, y=1.0): 2.26}
    #     af = axl.AshlockFingerprint(axl.GoByMajority, self.probe_class,
    #                                 step=0.25, progress_bar=False)
    #     data = af.fingerprint(turns=50, repetitions=2)
    #
    #     for key, value in data.items():
    #         self.assertAlmostEqual(value, test_data[key])
    #
    # @given(strategy_pair=strategy_lists(min_size=2, max_size=2))
    # def test_pair_fingerprints(self, strategy_pair):
    #     """
    #     A test to check that we can fingerprint
    #     with any two given strategies or instances
    #     """
    #     strategy, probe = strategy_pair
    #     af = AshlockFingerprint(strategy, probe, step=0.5)
    #     data = af.fingerprint(turns=2, repetitions=2, new_step=0.5,
    #                           progress_bar=False)
    #     self.assertIsInstance(data, dict)
    #
    #     af = AshlockFingerprint(strategy(), probe, step=0.5)
    #     data = af.fingerprint(turns=2, repetitions=2, new_step=0.5,
    #                           progress_bar=False)
    #     self.assertIsInstance(data, dict)
    #
    #     af = AshlockFingerprint(strategy, probe(), step=0.5)
    #     data = af.fingerprint(turns=2, repetitions=2, new_step=0.5,
    #                           progress_bar=False)
    #     self.assertIsInstance(data, dict)
    #
    #     af = AshlockFingerprint(strategy(), probe(), step=0.5)
    #     data = af.fingerprint(turns=2, repetitions=2, new_step=0.5,
    #                           progress_bar=False)
    #     self.assertIsInstance(data, dict)
