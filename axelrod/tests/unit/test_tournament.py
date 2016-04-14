"""Tests for the main tournament class."""

import axelrod
import logging
from multiprocess import Queue, cpu_count
import unittest
import random

import tempfile
import csv

from hypothesis import given, example, settings
from hypothesis.strategies import integers, lists, sampled_from, random_module, floats

try:
    # Python 3
    from unittest.mock import MagicMock
except ImportError:
    # Python 2
    from mock import MagicMock

test_strategies = [axelrod.Cooperator,
                   axelrod.TitForTat,
                   axelrod.Defector,
                   axelrod.Grudger,
                   axelrod.GoByMajority]
test_repetitions = 5
test_turns = 100

test_prob_end = .5


class TestTournament(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()
        cls.players = [s() for s in test_strategies]
        cls.test_name = 'test'
        cls.test_repetitions = test_repetitions
        cls.test_turns = test_turns

        cls.expected_payoff = [
            [600, 600, 0, 600, 600],
            [600, 600, 199, 600, 600],
            [1000, 204, 200, 204, 204],
            [600, 600, 199, 600, 600],
            [600, 600, 199, 600, 600]]

        cls.expected_cooperation = [
            [200, 200, 200, 200, 200],
            [200, 200, 1, 200, 200],
            [0, 0, 0, 0, 0],
            [200, 200, 1, 200, 200],
            [200, 200, 1, 200, 200]]

    def test_init(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=self.test_turns,
            processes=4,
            noise=0.2)
        self.assertEqual(len(tournament.players), len(test_strategies))
        self.assertIsInstance(
            tournament.players[0].match_attributes['game'], axelrod.Game
        )
        self.assertEqual(tournament.game.score(('C', 'C')), (3, 3))
        self.assertEqual(tournament.turns, self.test_turns)
        self.assertEqual(tournament.repetitions, 10)
        self.assertEqual(tournament.name, 'test')
        self.assertEqual(tournament._processes, 4)
        self.assertFalse(tournament.prebuilt_cache)
        self.assertTrue(tournament._with_morality)
        self.assertIsInstance(tournament._logger, logging.Logger)
        self.assertEqual(tournament.deterministic_cache, {})
        self.assertEqual(tournament.noise, 0.2)
        self.assertEqual(tournament._parallel_repetitions, 10)
        anonymous_tournament = axelrod.Tournament(players=self.players)
        self.assertEqual(anonymous_tournament.name, 'axelrod')

    def test_serial_play(self):
        # Test that we get an instance of ResultSet
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)
        results = tournament.play()
        self.assertIsInstance(results, axelrod.ResultSet)

        # Test that _run_serial_repetitions is called with empty matches list
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)
        tournament._run_serial_repetitions = MagicMock(
            name='_run_serial_repetitions')
        tournament._run_parallel_repetitions = MagicMock(
            name='_run_parallel_repetitions')
        tournament.play()
        tournament._run_serial_repetitions.assert_called_once_with([])
        self.assertFalse(tournament._run_parallel_repetitions.called)

    @given(s=lists(sampled_from(axelrod.strategies),
                   min_size=2,  # Errors are returned if less than 2 strategies
                   max_size=5, unique=True),
           turns=integers(min_value=2, max_value=50),
           repetitions=integers(min_value=2, max_value=4),
           rm=random_module())
    @settings(max_examples=50, timeout=0)
    @example(s=test_strategies, turns=test_turns, repetitions=test_repetitions,
             rm=random.seed(0))

    # These two examples are to make sure #465 is fixed.
    # As explained there: https://github.com/Axelrod-Python/Axelrod/issues/465,
    # these two examples were identified by hypothesis.
    @example(s=[axelrod.BackStabber, axelrod.MindReader], turns=2, repetitions=1,
             rm=random.seed(0))
    @example(s=[axelrod.ThueMorse, axelrod.MindReader], turns=2, repetitions=1,
             rm=random.seed(0))
    def test_property_serial_play(self, s, turns, repetitions, rm):
        """Test serial play using hypothesis"""
        # Test that we get an instance of ResultSet

        players = [strat() for strat in s]

        tournament = axelrod.Tournament(
            name=self.test_name,
            players=players,
            game=self.game,
            turns=turns,
            repetitions=repetitions)
        results = tournament.play()
        self.assertIsInstance(results, axelrod.ResultSet)
        self.assertEqual(results.nplayers, len(players))
        self.assertEqual(results.players, players)

    def test_parallel_play(self):
        # Test that we get an instance of ResultSet
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions,
            processes=2)
        results = tournament.play()
        self.assertIsInstance(results, axelrod.ResultSet)

        # The following relates to #516
        players = [axelrod.Cooperator(), axelrod.Defector(),
                   axelrod.BackStabber(), axelrod.PSOGambler(),
                   axelrod.ThueMorse(), axelrod.DoubleCrosser()]
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=players,
            game=self.game,
            turns=20,
            repetitions=self.test_repetitions,
            processes=2)
        scores = tournament.play().scores
        self.assertEqual(len(scores), len(players))

    def test_build_cache_required(self):
        # Noisy, no prebuilt cache, empty deterministic cache
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            processes=4,
            noise=0.2,
            prebuilt_cache=False)
        self.assertFalse(tournament._build_cache_required())

        # Noisy, with prebuilt cache, empty deterministic cache
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            processes=4,
            noise=0.2,
            prebuilt_cache=True)
        self.assertFalse(tournament._build_cache_required())

        # Not noisy, with prebuilt cache, deterministic cache has content
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            processes=4,
            prebuilt_cache=True)
        tournament.deterministic_cache = {'test': 100}
        self.assertFalse(tournament._build_cache_required())

        # Not noisy, no prebuilt cache, deterministic cache has content
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            processes=4,
            prebuilt_cache=False)
        tournament.deterministic_cache = {'test': 100}
        self.assertTrue(tournament._build_cache_required())

        # Not noisy, with prebuilt cache, empty deterministic cache
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            processes=4,
            prebuilt_cache=True)
        self.assertTrue(tournament._build_cache_required())

        # Not noisy, no prebuilt cache, empty deterministic cache
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            processes=4,
            prebuilt_cache=False)
        self.assertTrue(tournament._build_cache_required())

    def test_build_cache(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions,
            processes=2)
        tournament._run_single_repetition = MagicMock(
            name='_run_single_repetition')
        tournament._build_cache([])
        tournament._run_single_repetition.assert_called_once_with([])
        self.assertEqual(
            tournament._parallel_repetitions, self.test_repetitions - 1)

    def test_run_single_repetition(self):
        interactions = []
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)
        tournament._run_single_repetition(interactions)
        self.assertEqual(len(tournament.interactions), 1)
        self.assertEqual(len(tournament.interactions[0]), 15)

    def test_run_serial_repetitions(self):
        interactions = []
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)
        tournament._run_serial_repetitions(interactions)
        self.assertEqual(len(tournament.interactions), self.test_repetitions)

    def test_run_parallel_repetitions(self):
        interactions = []
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions,
            processes=2)
        tournament._run_parallel_repetitions(interactions)
        self.assertEqual(len(interactions), self.test_repetitions)
        for r in interactions:
            self.assertEqual(len(r.values()), 15)

    def test_n_workers(self):
        max_processes = cpu_count()

        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions,
            processes=1)
        self.assertEqual(tournament._n_workers(), max_processes)

        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions,
            processes=max_processes + 2)
        self.assertEqual(tournament._n_workers(), max_processes)

    @unittest.skipIf(
        cpu_count() < 2,
        "not supported on single processor machines")
    def test_2_workers(self):
        # This is a separate test with a skip condition because we
        # cannot guarantee that the tests will always run on a machine
        # with more than one processor
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions,
            processes=2)
        self.assertEqual(tournament._n_workers(), 2)

    def test_start_workers(self):
        workers = 2
        work_queue = Queue()
        done_queue = Queue()
        for repetition in range(self.test_repetitions):
            work_queue.put(repetition)
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)
        tournament._start_workers(workers, work_queue, done_queue)

        stops = 0
        while stops < workers:
            payoffs = done_queue.get()
            if payoffs == 'STOP':
                stops += 1
        self.assertEqual(stops, workers)

    def test_process_done_queue(self):
        workers = 2
        done_queue = Queue()
        matches = []
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)
        for r in range(self.test_repetitions):
            done_queue.put({})
        for w in range(workers):
            done_queue.put('STOP')
        tournament._process_done_queue(workers, done_queue, matches)
        self.assertEqual(len(matches), self.test_repetitions)

    def test_worker(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)

        work_queue = Queue()
        for repetition in range(self.test_repetitions):
            work_queue.put(repetition)
        work_queue.put('STOP')

        done_queue = Queue()
        tournament._worker(work_queue, done_queue)
        for r in range(self.test_repetitions):
            new_matches = done_queue.get()
            self.assertEqual(len(new_matches), 15)
            for index_pair, match in new_matches.items():
                self.assertIsInstance(index_pair, tuple)
                self.assertIsInstance(match, list)
        queue_stop = done_queue.get()
        self.assertEqual(queue_stop, 'STOP')

    def test_build_result_set(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)
        results = tournament._build_result_set()
        self.assertIsInstance(results, axelrod.ResultSet)

    @given(turns=integers(min_value=1, max_value=200))
    @example(turns=3)
    @example(turns=200)
    def test_play_matches(self, turns):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            repetitions=self.test_repetitions)


        def make_generator():
            """Return a generator used by this method"""
            player_classes = [axelrod.Cooperator, axelrod.TitForTat,
                              axelrod.Defector, axelrod.Grudger]
            for i, player_cls in enumerate(player_classes):
                for j, opponent_cls in enumerate(player_classes):
                    if j >= i:  # These matches correspond to a round robin
                        players = (player_cls(), opponent_cls())
                        match = axelrod.Match(players, turns=turns)
                        yield ((i, j), match)

        matches_generator = make_generator()
        interactions = tournament._play_matches(matches_generator)

        self.assertEqual(len(interactions), 10)

        for index_pair, inter in interactions.items():
            self.assertEqual(len(inter), turns)
            self.assertEqual(len(index_pair), 2)
            for plays in inter:
                self.assertIsInstance(plays, tuple)
                self.assertEqual(len(plays), 2)

        # Check that matches no longer exist?
        self.assertEqual((len(list(matches_generator))), 0)

    def test_play_and_write_to_csv(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=2,
            repetitions=2)
        tmp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tournament.play(filename=tmp_file.name)
        with open(tmp_file.name, 'r') as f:
            written_data = [[int(r[0]), int(r[1])] + r[2:] for r in csv.reader(f)]
            expected_data = [[0, 1, 'Cooperator', 'Tit For Tat', 'CCCC', 'CCCC'],
                             [1, 2, 'Tit For Tat', 'Defector', 'CDDD', 'CDDD'],
                             [0, 0, 'Cooperator', 'Cooperator', 'CCCC', 'CCCC'],
                             [3, 3, 'Grudger', 'Grudger', 'CCCC', 'CCCC'],
                             [2, 2, 'Defector', 'Defector', 'DDDD', 'DDDD'],
                             [4, 4, 'Soft Go By Majority', 'Soft Go By Majority',
                              'CCCC', 'CCCC'],
                             [1, 4, 'Tit For Tat', 'Soft Go By Majority',
                              'CCCC', 'CCCC'],
                             [1, 1, 'Tit For Tat', 'Tit For Tat', 'CCCC', 'CCCC'],
                             [1, 3, 'Tit For Tat', 'Grudger', 'CCCC', 'CCCC'],
                             [2, 3, 'Defector', 'Grudger', 'DCDD', 'DCDD'],
                             [0, 4, 'Cooperator', 'Soft Go By Majority',
                              'CCCC', 'CCCC'],
                             [2, 4, 'Defector', 'Soft Go By Majority',
                              'DCDD', 'DCDD'],
                             [0, 3, 'Cooperator', 'Grudger', 'CCCC', 'CCCC'],
                             [3, 4, 'Grudger', 'Soft Go By Majority',
                              'CCCC', 'CCCC'],
                             [0, 2, 'Cooperator', 'Defector', 'CDCD', 'CDCD']]
            self.assertEqual(sorted(written_data), sorted(expected_data))

    def test_write_to_csv(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=2,
            repetitions=2)
        tournament.play()
        tmp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tournament._write_to_csv(tmp_file.name)
        with open(tmp_file.name, 'r') as f:
            written_data = [[int(r[0]), int(r[1])] + r[2:] for r in csv.reader(f)]
            expected_data = [[0, 1, 'Cooperator', 'Tit For Tat', 'CCCC', 'CCCC'],
                             [1, 2, 'Tit For Tat', 'Defector', 'CDDD', 'CDDD'],
                             [0, 0, 'Cooperator', 'Cooperator', 'CCCC', 'CCCC'],
                             [3, 3, 'Grudger', 'Grudger', 'CCCC', 'CCCC'],
                             [2, 2, 'Defector', 'Defector', 'DDDD', 'DDDD'],
                             [4, 4, 'Soft Go By Majority', 'Soft Go By Majority',
                              'CCCC', 'CCCC'],
                             [1, 4, 'Tit For Tat', 'Soft Go By Majority',
                              'CCCC', 'CCCC'],
                             [1, 1, 'Tit For Tat', 'Tit For Tat', 'CCCC', 'CCCC'],
                             [1, 3, 'Tit For Tat', 'Grudger', 'CCCC', 'CCCC'],
                             [2, 3, 'Defector', 'Grudger', 'DCDD', 'DCDD'],
                             [0, 4, 'Cooperator', 'Soft Go By Majority',
                              'CCCC', 'CCCC'],
                             [2, 4, 'Defector', 'Soft Go By Majority',
                              'DCDD', 'DCDD'],
                             [0, 3, 'Cooperator', 'Grudger', 'CCCC', 'CCCC'],
                             [3, 4, 'Grudger', 'Soft Go By Majority',
                              'CCCC', 'CCCC'],
                             [0, 2, 'Cooperator', 'Defector', 'CDCD', 'CDCD']]
            self.assertEqual(sorted(written_data), sorted(expected_data))

    def test_data_for_csv(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=2,
            repetitions=2)
        tournament.play()
        expected_data = [[0, 1, 'Cooperator', 'Tit For Tat', 'CCCC', 'CCCC'],
                         [1, 2, 'Tit For Tat', 'Defector', 'CDDD', 'CDDD'],
                         [0, 0, 'Cooperator', 'Cooperator', 'CCCC', 'CCCC'],
                         [3, 3, 'Grudger', 'Grudger', 'CCCC', 'CCCC'],
                         [2, 2, 'Defector', 'Defector', 'DDDD', 'DDDD'],
                         [4, 4, 'Soft Go By Majority', 'Soft Go By Majority',
                          'CCCC', 'CCCC'],
                         [1, 4, 'Tit For Tat', 'Soft Go By Majority',
                          'CCCC', 'CCCC'],
                         [1, 1, 'Tit For Tat', 'Tit For Tat', 'CCCC', 'CCCC'],
                         [1, 3, 'Tit For Tat', 'Grudger', 'CCCC', 'CCCC'],
                         [2, 3, 'Defector', 'Grudger', 'DCDD', 'DCDD'],
                         [0, 4, 'Cooperator', 'Soft Go By Majority',
                          'CCCC', 'CCCC'],
                         [2, 4, 'Defector', 'Soft Go By Majority',
                          'DCDD', 'DCDD'],
                         [0, 3, 'Cooperator', 'Grudger', 'CCCC', 'CCCC'],
                         [3, 4, 'Grudger', 'Soft Go By Majority',
                          'CCCC', 'CCCC'],
                         [0, 2, 'Cooperator', 'Defector', 'CDCD', 'CDCD']]
        generator_data = tournament._data_for_csv()
        for row, expected_row in zip(sorted(generator_data), sorted(expected_data)):
            self.assertEqual(row, expected_row)


class TestProbEndTournament(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()
        cls.players = [s() for s in test_strategies]
        cls.test_name = 'test'
        cls.test_repetitions = test_repetitions
        cls.test_prob_end = test_prob_end

    def test_init(self):
        tournament = axelrod.ProbEndTournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            prob_end=self.test_prob_end,
            noise=0.2)
        self.assertEqual(tournament.match_generator.prob_end, tournament.prob_end)
        self.assertEqual(len(tournament.players), len(test_strategies))
        self.assertEqual(tournament.game.score(('C', 'C')), (3, 3))
        self.assertEqual(tournament.turns, float("inf"))
        self.assertEqual(tournament.repetitions, 10)
        self.assertEqual(tournament.name, 'test')
        self.assertEqual(tournament._processes, None)
        self.assertFalse(tournament.prebuilt_cache)
        self.assertTrue(tournament._with_morality)
        self.assertIsInstance(tournament._logger, logging.Logger)
        self.assertEqual(tournament.deterministic_cache, {})
        self.assertEqual(tournament.noise, 0.2)
        self.assertEqual(tournament._parallel_repetitions, 10)
        anonymous_tournament = axelrod.Tournament(players=self.players)
        self.assertEqual(anonymous_tournament.name, 'axelrod')

    @given(s=lists(sampled_from(axelrod.strategies),
                   min_size=2,  # Errors are returned if less than 2 strategies
                   max_size=5, unique=True),
           prob_end=floats(min_value=.1, max_value=.9),
           repetitions=integers(min_value=2, max_value=4),
           rm=random_module())
    @settings(max_examples=50, timeout=0)
    @example(s=test_strategies, prob_end=test_prob_end,
             repetitions=test_repetitions,
             rm=random.seed(0))
    def test_build_cache_never_required(self, s, prob_end, repetitions, rm):
        """
        As the matches have a sampled length a cache is never required.
        """
        players = [strat() for strat in s]

        tournament = axelrod.ProbEndTournament(
            name=self.test_name,
            players=players,
            game=self.game,
            prob_end=prob_end,
            repetitions=repetitions)
        self.assertFalse(tournament._build_cache_required())


    @given(s=lists(sampled_from(axelrod.strategies),
                   min_size=2,  # Errors are returned if less than 2 strategies
                   max_size=5, unique=True),
           prob_end=floats(min_value=.1, max_value=.9),
           repetitions=integers(min_value=2, max_value=4),
           rm=random_module())
    @settings(max_examples=50, timeout=0)
    @example(s=test_strategies, prob_end=.2, repetitions=test_repetitions,
             rm=random.seed(0))

    # These two examples are to make sure #465 is fixed.
    # As explained there: https://github.com/Axelrod-Python/Axelrod/issues/465,
    # these two examples were identified by hypothesis.
    @example(s=[axelrod.BackStabber, axelrod.MindReader], prob_end=.2, repetitions=1,
             rm=random.seed(0))
    @example(s=[axelrod.ThueMorse, axelrod.MindReader], prob_end=.2, repetitions=1,
             rm=random.seed(0))
    def test_property_serial_play(self, s, prob_end, repetitions, rm):
        """Test serial play using hypothesis"""
        # Test that we get an instance of ResultSet

        players = [strat() for strat in s]

        tournament = axelrod.ProbEndTournament(
            name=self.test_name,
            players=players,
            game=self.game,
            prob_end=prob_end,
            repetitions=repetitions)
        results = tournament.play()
        self.assertIsInstance(results, axelrod.ResultSet)
        self.assertEqual(results.nplayers, len(players))
        self.assertEqual(results.players, players)
        self.assertEqual(len(results.interactions), repetitions)
