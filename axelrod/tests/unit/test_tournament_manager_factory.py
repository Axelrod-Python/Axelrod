import unittest
import axelrod


class TestTournamentManagerFactory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmf = axelrod.TournamentManagerFactory

        cls.test_output_directory = './assets/'
        cls.test_with_ecological = True
        cls.test_rebuild_cache = False
        cls.test_cache_file = './cache.txt'
        cls.test_exclusions = ['basic_strategies', 'cheating_strategies']
        cls.test_kwargs = {
            'processes': 2,
            'turns': 10,
            'repetitions': 200,
            'noise': 0
        }

        cls.expected_basic_strategies = axelrod.basic_strategies
        cls.expected_strategies = (
            axelrod.ordinary_strategies)
        cls.expected_cheating_strategies = axelrod.cheating_strategies
        cls.expected_all_strategies = (
            axelrod.ordinary_strategies +
            axelrod.cheating_strategies)

    def test_tournaments_dict(self):

        # Tests to ensure that the tournaments dictionary contains the correct
        # keys and values
        actual_basic_strategies = (
            self.tmf._tournaments_dict()['basic_strategies'])
        actual_strategies = self.tmf._tournaments_dict()['strategies']
        actual_cheating_strategies = (
            self.tmf._tournaments_dict()['cheating_strategies'])
        actual_all_strategies = self.tmf._tournaments_dict()['all_strategies']

        self.assertEqual(
            actual_basic_strategies, self.expected_basic_strategies)
        self.assertEqual(actual_strategies, self.expected_strategies)
        self.assertEqual(
            actual_cheating_strategies, self.expected_cheating_strategies)
        self.assertEqual(actual_all_strategies, self.expected_all_strategies)

        # Tests to ensure that the exclusions list works as intended
        with_exclusions = self.tmf._tournaments_dict(self.test_exclusions)
        self.assertFalse('basic_strategies' in with_exclusions)
        self.assertFalse('cheating_strategies' in with_exclusions)
        self.assertEqual(
            with_exclusions['strategies'], self.expected_strategies)

    def test_add_tournaments(self):
        mgr = axelrod.TournamentManager(
            self.test_output_directory,
            self.test_with_ecological)

        self.tmf._add_tournaments(mgr, self.test_exclusions, self.test_kwargs)
        self.assertEqual(len(mgr._tournaments), 2)
        self.assertIsInstance(mgr._tournaments[0], axelrod.Tournament)
        self.assertEqual(mgr._tournaments[0].name, 'strategies')

    def test_create_tournament_manager(self):
        mgr = self.tmf.create_tournament_manager(
            output_directory=self.test_output_directory,
            no_ecological=False,
            rebuild_cache=self.test_rebuild_cache,
            cache_file=self.test_cache_file,
            exclusions=self.test_exclusions,
            **self.test_kwargs)

        self.assertIsInstance(mgr, axelrod.TournamentManager)
        self.assertEqual(mgr._output_directory, self.test_output_directory)
        self.assertEqual(len(mgr._tournaments), 2)
        self.assertTrue(mgr._with_ecological)
        self.assertTrue(mgr._pass_cache)
