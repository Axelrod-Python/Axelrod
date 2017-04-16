import unittest
import axelrod as axl
from hypothesis import given
from axelrod.fingerprint import (
    AshlockFingerprint, Point, create_player, get_class_and_kwargs,
    SpatialTournamentCreator, JossAnnProbeCreator,
    DataOrganizer, create_points, get_mean_score, update_according_to_os
)
from axelrod.tests.property import strategy_lists


matplotlib_installed = True
try:
    import matplotlib.pyplot
except ImportError:  # pragma: no cover
    matplotlib_installed = False


C, D = axl.Actions.C, axl.Actions.D


class TestModuleFunctions(unittest.TestCase):
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

    def test_update_according_to_os_filename_none_windows_vs_other(self):
        filename, in_memory = update_according_to_os(None, False)
        if axl.on_windows:
            self.assertTrue(in_memory)
            self.assertIsNone(filename)
        else:
            self.assertFalse(in_memory)
            self.assertIsNotNone(filename)

    def test_update_according_to_os_no_special_case(self):
        filename, in_memory = update_according_to_os('bobo_knows', False)
        self.assertFalse(in_memory)
        self.assertEqual(filename, 'bobo_knows')

    def test_create_points(self):
        expected = [Point(0.0, 0.0), Point(0.0, 1.0),
                    Point(1.0, 0.0), Point(1.0, 1.0)]
        self.assertEqual(expected, create_points(1.0))

    def test_create_points_rounds_up_to_nearest_whole(self):
        step_one = [Point(0.0, 0.0), Point(0.0, 1.0),
                    Point(1.0, 0.0), Point(1.0, 1.0)]
        step_two = [Point(0.0, 0.0), Point(0.0, 0.5), Point(0.0, 1.0),
                    Point(0.5, 0.0), Point(0.5, 0.5), Point(0.5, 1.0),
                    Point(1.0, 0.0), Point(1.0, 0.5), Point(1.0, 1.0)]
        self.assertEqual(step_one, create_points(0.51))
        self.assertEqual(step_two, create_points(0.5))

    def test_create_point_with_fraction_that_is_not_finite_decimal(self):
        points = create_points(0.3)
        self.assertEqual(points[7][1], 1.0)
        self.assertAlmostEqual(points[7][0], 0.33333333, places=7)

    def test_get_mean_score(self):
        matches = [[(C, C), (C, D), (D, C)],
                   [(D, C), (D, D)]]
        match_scores = [(3 + 0 + 5) / 3, (5 + 1) / 2]
        mean = (match_scores[0] + match_scores[1]) / 2.0

        self.assertEqual(get_mean_score(matches), mean)


class TestJossAnnProbeCreator(unittest.TestCase):
    def test_get_probe_joss_ann(self):
        probe_creator = JossAnnProbeCreator(axl.Cooperator)
        probe = probe_creator.get_probe(Point(0.5, 0.3))
        self.assertEqual(str(probe), 'Joss-Ann Cooperator: (0.5, 0.3)')

    def test_get_probe_dual_joss_ann(self):
        probe_creator = JossAnnProbeCreator(axl.Cooperator)
        probe = probe_creator.get_probe(Point(0.5, 0.5))
        self.assertEqual(str(probe), 'Dual Joss-Ann Cooperator: (0.5, 0.5)')

    def test_get_probe_probe_creator_passed_instance(self):
        probe_creator = JossAnnProbeCreator(axl.Cycler('DDD'))
        probe = probe_creator.get_probe(Point(0.2, 0.2))
        self.assertEqual(str(probe), 'Joss-Ann Cycler: DDD: (0.2, 0.2)')

    def test_get_probe_probe_creator_passed_strategy_uses_default(self):
        probe_creator = JossAnnProbeCreator(axl.Cycler)
        probe = probe_creator.get_probe(Point(0.2, 0.2))
        self.assertEqual(str(probe), 'Joss-Ann Cycler: CCD: (0.2, 0.2)')

    def test_get_probe_dict_from_point_list(self):
        points = [Point(0.0, 0.0), Point(0.0, 0.5), Point(0.5, 1.0)]
        expected_point_probe_str = {
            Point(0.0, 0.0): 'Joss-Ann Tit For Tat: (0.0, 0.0)',
            Point(0.0, 0.5): 'Joss-Ann Tit For Tat: (0.0, 0.5)',
            Point(0.5, 1.0): 'Dual Joss-Ann Tit For Tat: (0.5, 0.0)',
        }
        probe_creator = JossAnnProbeCreator(
            axl.TitForTat, progress_bar=False)
        alt_probe_creator = JossAnnProbeCreator(
            axl.TitForTat, progress_bar=True)
        probe_dict = probe_creator.get_probe_dict(points)
        alt_probe_dict = alt_probe_creator.get_probe_dict(points)

        for point in probe_dict.keys():
            self.assertEqual(str(probe_dict[point]),
                             expected_point_probe_str[point])
            self.assertEqual(str(alt_probe_dict[point]),
                             expected_point_probe_str[point])

    def test_get_probe_dict_from_step(self):
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
        probe_creator = JossAnnProbeCreator(
            axl.TitForTat, progress_bar=False)
        alt_probe_creator = JossAnnProbeCreator(
            axl.TitForTat, progress_bar=True)
        probe_dict = probe_creator.get_probe_dict_from_step(0.5)
        alt_probe_dict = alt_probe_creator.get_probe_dict_from_step(0.5)

        for point in probe_dict.keys():
            self.assertEqual(str(probe_dict[point]),
                             expected_point_probe_str[point])
            self.assertEqual(str(alt_probe_dict[point]),
                             expected_point_probe_str[point])


class TestSpatialTournamentCreator(unittest.TestCase):
    def test_get_points_to_edges(self):
        tournament_creator = SpatialTournamentCreator(
            player=axl.Cooperator, probe=axl.TitForTat, step=1.0)
        expected = {Point(0.0, 0.0): (0, 1), Point(0.0, 1.0): (0, 2),
                    Point(1.0, 0.0): (0, 3), Point(1.0, 1.0): (0, 4)}
        self.assertEqual(tournament_creator.get_points_to_edges(), expected)

    def test_get_tournament_default_args(self):
        tournament_creator = SpatialTournamentCreator(
            player=axl.Cooperator, probe=axl.TitForTat, step=1.0)
        tournament = tournament_creator.get_tournament()
        expected_player_strings = [
            'Cooperator',
            'Joss-Ann Tit For Tat: (0.0, 0.0)',
            'Dual Joss-Ann Tit For Tat: (1.0, 0.0)',
            'Dual Joss-Ann Tit For Tat: (0.0, 1.0)',
            'Dual Joss-Ann Tit For Tat: (0.0, 0.0)']

        self.assertEqual(tournament.edges, [(0, 1), (0, 2), (0, 3), (0, 4)])
        self.assertEqual([str(player) for player in tournament.players],
                         expected_player_strings)
        self.assertEqual(tournament.noise, 0)
        self.assertEqual(tournament.turns, 200)
        self.assertEqual(tournament.repetitions, 10)
        self.assertEqual(tournament.name, 'axelrod')

    def test_get_tournament_new_args(self):
        tournament_creator = SpatialTournamentCreator(
            player=axl.Cooperator, probe=axl.TitForTat, step=1.0)
        new_kwargs = {'turns': 2, 'repetitions': 1, 'noise': 0.5,
                      'name': 'super_badass_tournament_of_awesomeness'}
        tournament = tournament_creator.get_tournament(**new_kwargs)
        expected_player_strings = [
            'Cooperator',
            'Joss-Ann Tit For Tat: (0.0, 0.0)',
            'Dual Joss-Ann Tit For Tat: (1.0, 0.0)',
            'Dual Joss-Ann Tit For Tat: (0.0, 1.0)',
            'Dual Joss-Ann Tit For Tat: (0.0, 0.0)']

        self.assertEqual(tournament.edges, [(0, 1), (0, 2), (0, 3), (0, 4)])
        self.assertEqual([str(player) for player in tournament.players],
                         expected_player_strings)
        self.assertEqual(tournament.noise, 0.5)
        self.assertEqual(tournament.turns, 2)
        self.assertEqual(tournament.repetitions, 1)
        self.assertEqual(tournament.name,
                         'super_badass_tournament_of_awesomeness')

    def test_player_as_instance(self):
        tournament_creator = SpatialTournamentCreator(
            player=axl.Cycler('DDD'), probe=axl.TitForTat, step=1.0)
        tournament = tournament_creator.get_tournament()
        self.assertEqual(str(tournament.players[0]), 'Cycler: DDD')

    def test_probe_as_instance(self):
        tournament_creator = SpatialTournamentCreator(
            player=axl.Cooperator, probe=axl.Cycler('DDD'), step=1.0)
        tournament = tournament_creator.get_tournament()
        self.assertEqual(str(tournament.players[1]),
                         'Joss-Ann Cycler: DDD: (0.0, 0.0)')

    def test_progress_bar_false(self):
        tournament_creator = SpatialTournamentCreator(
            player=axl.Cycler('DDD'), probe=axl.TitForTat, step=1.0,
            progress_bar=False
        )
        tournament = tournament_creator.get_tournament()
        self.assertEqual(str(tournament.players[0]), 'Cycler: DDD')


class TestDataOrganizer(unittest.TestCase):
    def setUp(self):
        self.points_edges = {
            Point(0.0, 0.0): (0, 1),
            Point(0.0, 0.5): (0, 2),
            Point(0.0, 1.0): (0, 3),
            Point(0.5, 0.0): (0, 4),
            Point(0.5, 0.5): (0, 5),
            Point(0.5, 1.0): (0, 6),
            Point(1.0, 0.0): (0, 7),
            Point(1.0, 0.5): (0, 8),
            Point(1.0, 1.0): (0, 9),

        }
        self.interactions = {
            (0, 1): [[(C, C), (C, C)]],
            (0, 2): [[(C, C), (C, D)]],
            (0, 3): [[(C, C), (D, C)]],
            (0, 4): [[(C, C), (D, D)]],
            (0, 5): [[(C, D), (D, C)]],
            (0, 6): [[(C, D), (C, D)]],
            (0, 7): [[(C, D), (D, D)]],
            (0, 8): [[(D, D), (D, D)]],
            (0, 9): [[(D, C), (D, C)]],
        }
        self.organizer = DataOrganizer(self.points_edges, self.interactions)

    def test_get_points_interactions_dict(self):
        expected = {
            Point(0.0, 0.0): [[(C, C), (C, C)]],
            Point(0.0, 0.5): [[(C, C), (C, D)]],
            Point(0.0, 1.0): [[(C, C), (D, C)]],
            Point(0.5, 0.0): [[(C, C), (D, D)]],
            Point(0.5, 0.5): [[(C, D), (D, C)]],
            Point(0.5, 1.0): [[(C, D), (C, D)]],
            Point(1.0, 0.0): [[(C, D), (D, D)]],
            Point(1.0, 0.5): [[(D, D), (D, D)]],
            Point(1.0, 1.0): [[(D, C), (D, C)]],
        }
        self.assertEqual(expected,
                         self.organizer.get_points_interactions_dict())

    def test_get_points_averages_dict(self):
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
        self.assertEqual(expected, self.organizer.get_points_averages_dict())

    def test_get_plotting_data(self):
        expected = [[4.0, 0.0, 5.0],
                    [1.5, 2.5, 1.0],
                    [3.0, 2.0, 0.5]]

        plot_data = self.organizer.get_plotting_data()
        for i in range(len(plot_data)):
            self.assertEqual(list(plot_data[i]), expected[i])


class TestFingerprint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.strategy = axl.WinStayLoseShift
        cls.probe_class = axl.TitForTat

    def setUp(self):
        self.simple_af = AshlockFingerprint(axl.Cooperator, axl.Cooperator)
        self.simple_interactions = {
            Point(0.0, 0.0): [[(C, C), (C, C)]],
            Point(0.0, 1.0): [[(C, D), (C, D)]],
            Point(1.0, 0.0): [[(C, C), (C, C)]],
            Point(1.0, 1.0): [[(C, D), (C, D)]]
        }
        self.simple_data = {
            Point(0.0, 0.0): 3.0,
            Point(0.0, 1.0): 0.0,
            Point(1.0, 0.0): 3.0,
            Point(1.0, 1.0): 0.0
        }

    def test_data_and_interactions_when_none(self):
        self.assertIsNone(self.simple_af.data)
        self.assertIsNone(self.simple_af.interactions)

    def test_data_and_interactions(self):
        self.simple_af.fingerprint(turns=2, repetitions=1, step=1.0)

        self.assertEqual(self.simple_af.interactions, self.simple_interactions)
        self.assertEqual(self.simple_af.data, self.simple_data)

    def test_fingerprint_with_filename(self):
        filename = "test_outputs/test_fingerprint.csv"
        af = AshlockFingerprint(self.strategy, probe=self.probe_class)
        af.fingerprint(turns=1, repetitions=1, filename=filename, step=0.5,
                       progress_bar=False)
        with open(filename, 'r') as out:
            data = out.read()
            self.assertEqual(len(data.split("\n")), 10)

    def test_in_memory_fingerprint(self):
        self.simple_af.fingerprint(turns=2, repetitions=1, step=1.0,
                                   in_memory=True)
        self.assertEqual(self.simple_af.interactions, self.simple_interactions)
        self.assertEqual(self.simple_af.data, self.simple_data)

    @unittest.skipIf(axl.on_windows,
                     "Parallel processing not supported on Windows")
    def test_parallel_fingerprint(self):
        self.simple_af.fingerprint(turns=2, repetitions=1, step=1.0,
                                   processes=2)
        self.assertEqual(self.simple_af.interactions, self.simple_interactions)
        self.assertEqual(self.simple_af.data, self.simple_data)

    def test_plot(self):
        af = AshlockFingerprint(self.strategy, self.probe_class)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25,
                              progress_bar=False)
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

        af = axl.AshlockFingerprint(self.strategy, self.probe_class)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25,
                              progress_bar=True)

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
        af = axl.AshlockFingerprint(axl.TitForTat, self.probe_class)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25,
                              progress_bar=False)

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
        af = axl.AshlockFingerprint(axl.GoByMajority, self.probe_class)
        data = af.fingerprint(turns=50, repetitions=2, step=0.25,
                              progress_bar=False)

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
