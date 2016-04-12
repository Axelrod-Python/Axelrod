import unittest
import sys
import os
import axelrod


def test_pickle():
    if sys.version_info[0] == 2:
        # Python 2.x
        test_pickle = b'\x80\x02}q\x00caxelrod.strategies.titfortat\nTitForTat\nq\x01caxelrod.strategies.defector\nDefector\nq\x02\x86q\x03]q\x04(U\x01Cq\x05U\x01Dq\x06\x86q\x07h\x06h\x06\x86q\x08h\x06h\x06\x86q\tes.'
    else:
        # Python 3.x
        test_pickle = b'\x80\x03}q\x00caxelrod.strategies.titfortat\nTitForTat\nq\x01caxelrod.strategies.defector\nDefector\nq\x02\x86q\x03]q\x04(X\x01\x00\x00\x00Cq\x05X\x01\x00\x00\x00Dq\x06\x86q\x07h\x06h\x06\x86q\x08h\x06h\x06\x86q\tes.'
    return test_pickle

class TestTournamentManagerFactory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmf = axelrod.TournamentManagerFactory

        cls.test_output_directory = './assets/'
        cls.test_with_ecological = True
        cls.test_rebuild_cache = False
        cls.test_cache_file = './test_cache.txt'

        with open(cls.test_cache_file, 'wb') as f:
            f.write(test_pickle())

        cls.test_exclusions = ['basic_strategies', 'cheating_strategies']
        cls.test_kwargs = {
            'processes': 2,
            'turns': 10,
            'repetitions': 200,
            'noise': 0
        }

        cls.expected_basic_strategies = axelrod.basic_strategies
        cls.expected_ordinary_strategies = (
            axelrod.ordinary_strategies)
        cls.expected_cheating_strategies = axelrod.cheating_strategies
        cls.expected_strategies = (
            axelrod.ordinary_strategies +
            axelrod.cheating_strategies)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_cache_file)

    def test_tournaments_dict(self):

        # Tests to ensure that the tournaments dictionary contains the correct
        # keys and values
        actual_basic_strategies = (
            self.tmf._tournaments_dict()['basic_strategies'])
        actual_strategies = self.tmf._tournaments_dict()['strategies']
        actual_cheating_strategies = (
            self.tmf._tournaments_dict()['cheating_strategies'])
        actual_all_strategies = self.tmf._tournaments_dict()['strategies']

        self.assertEqual(
            actual_basic_strategies, self.expected_basic_strategies)
        self.assertEqual(actual_strategies, self.expected_strategies)
        self.assertEqual(
            actual_cheating_strategies, self.expected_cheating_strategies)
        self.assertEqual(actual_all_strategies, self.expected_strategies)

        # Tests to ensure that the exclusions list works as intended
        with_exclusions = self.tmf._tournaments_dict(self.test_exclusions)
        self.assertFalse('basic_strategies' in with_exclusions)
        self.assertFalse('cheating_strategies' in with_exclusions)
        self.assertEqual(
            with_exclusions['strategies'], self.expected_strategies)

    def test_add_tournaments(self):
        mgr = axelrod.TournamentManager(
            self.test_output_directory,
            self.test_with_ecological,
            cache_file=self.test_cache_file)

        self.tmf._add_tournaments(mgr, self.test_exclusions, self.test_kwargs)
        self.assertEqual(len(mgr._tournaments), 2)
        self.assertIsInstance(mgr._tournaments[0], axelrod.Tournament)
        self.assertEqual(mgr._tournaments[0].name, 'ordinary_strategies')

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


class TestProbEndTournamentManagerFactory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmf = axelrod.ProbEndTournamentManagerFactory

        cls.test_output_directory = './assets/'
        cls.test_with_ecological = True
        cls.test_rebuild_cache = False
        cls.test_cache_file = './test_cache.txt'

        with open(cls.test_cache_file, 'wb') as f:
            f.write(test_pickle())

        cls.test_exclusions = ['basic_strategies', 'cheating_strategies']
        cls.test_kwargs = {
            'processes': 2,
            'turns': 10,
            'repetitions': 200,
            'noise': 0
        }
        cls.test_exclusions = ['basic_strategies', 'cheating_strategies']
        cls.test_kwargs = {
            'processes': 2,
            'prob_end': .1,
            'repetitions': 200,
            'noise': 0
        }

        cls.expected_basic_strategies = axelrod.basic_strategies
        cls.expected_ordinary_strategies = (
            axelrod.ordinary_strategies)
        cls.expected_cheating_strategies = axelrod.cheating_strategies
        cls.expected_strategies = (
            axelrod.ordinary_strategies +
            axelrod.cheating_strategies)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_cache_file)

    def test_tournaments_dict(self):

        # Tests to ensure that the tournaments dictionary contains the correct
        # keys and values
        actual_basic_strategies = (
            self.tmf._tournaments_dict()['basic_strategies_prob_end'])
        actual_ordinary_strategies = self.tmf._tournaments_dict()['ordinary_strategies_prob_end']
        actual_cheating_strategies = (
            self.tmf._tournaments_dict()['cheating_strategies_prob_end'])
        actual_all_strategies = self.tmf._tournaments_dict()['strategies_prob_end']

        self.assertEqual(
            actual_basic_strategies, self.expected_basic_strategies)
        self.assertEqual(actual_ordinary_strategies, self.expected_ordinary_strategies)
        self.assertEqual(
            actual_cheating_strategies, self.expected_cheating_strategies)
        self.assertEqual(actual_all_strategies, self.expected_strategies)

        # Tests to ensure that the exclusions list works as intended
        with_exclusions = self.tmf._tournaments_dict(self.test_exclusions)
        self.assertFalse('basic_strategies' in with_exclusions)
        self.assertFalse('cheating_strategies' in with_exclusions)
        self.assertEqual(
            with_exclusions['strategies_prob_end'], self.expected_strategies)

    def test_add_tournaments(self):
        mgr = axelrod.ProbEndTournamentManager(
            self.test_output_directory,
            self.test_with_ecological,
            cache_file=self.test_cache_file)

        self.tmf._add_tournaments(mgr, self.test_exclusions, self.test_kwargs)
        self.assertEqual(len(mgr._tournaments), 2)
        self.assertIsInstance(mgr._tournaments[0], axelrod.Tournament)
        self.assertEqual(mgr._tournaments[0].name, 'ordinary_strategies_prob_end')

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
