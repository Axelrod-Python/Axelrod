"""Tests for the main tournament class."""

import axelrod
import logging
import multiprocessing
import unittest
import random

from hypothesis import given, example
from hypothesis.strategies import (integers, lists,
                                   sampled_from, random_module,
                                   Settings)

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
            [1000, 204, 200.0, 204, 204],
            [600, 600, 199, 600.0, 600],
            [600, 600, 199, 600, 600]]

        cls.expected_cooperation = [
            [200, 200, 200, 200, 200],
            [200, 200, 1, 200, 200],
            [0.0, 0.0, 0.0, 0.0, 0.0],
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
        self.assertEqual(len(tournament.players), len(self.players))
        self.assertEqual(
            tournament.players[0].tournament_attributes['length'],
            self.test_turns
        )
        self.assertIsInstance(
            tournament.players[0].tournament_attributes['game'], axelrod.Game
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

        # Test that _run_serial_repetitions is called with empty payoffs list
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
        tournament._run_serial_repetitions.assert_called_once_with(
            {'cooperation': [], 'payoff': []})
        self.assertFalse(tournament._run_parallel_repetitions.called)

    @given(s=lists(sampled_from(axelrod.strategies),
                   min_size=2,  # Errors are returned if less than 2 strategies
                   max_size=5, unique=True),
           turns=integers(min_value=2, max_value=50),
           repetitions=integers(min_value=2, max_value=4),
           settings=Settings(max_examples=50,
                             timeout=0),
           rm=random_module())
    @example(s=test_strategies, turns=test_turns, repetitions=test_repetitions,
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
        self.assertEqual(len(results.cooperation), len(players))
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

        # Test that _run_parallel_repetitions is called with
        # one entry in payoffs list
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions,
            processes=2)
        tournament._run_serial_repetitions = MagicMock(
            name='_run_serial_repetitions')
        tournament._run_parallel_repetitions = MagicMock(
            name='_run_parallel_repetitions')
        tournament.play()
        tournament._run_parallel_repetitions.assert_called_once_with({
            'payoff': [self.expected_payoff],
            'cooperation': [self.expected_cooperation]})
        self.assertFalse(tournament._run_serial_repetitions.called)

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
        outcome = {'payoff': [], 'cooperation': []}
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)
        tournament._run_single_repetition(outcome)
        self.assertEqual(len(outcome['payoff']), 1)
        self.assertEqual(len(outcome['cooperation']), 1)
        self.assertEqual(outcome['payoff'][0], self.expected_payoff)
        self.assertEqual(outcome['cooperation'][0], self.expected_cooperation)

    def test_run_serial_repetitions(self):
        outcome = {'payoff': [], 'cooperation': []}
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)
        tournament._run_serial_repetitions(outcome)
        self.assertEqual(len(outcome['payoff']), self.test_repetitions)
        self.assertEqual(len(outcome['cooperation']), self.test_repetitions)
        for r in range(self.test_repetitions):
            self.assertEqual(outcome['payoff'][r], self.expected_payoff)
            self.assertEqual(
                outcome['cooperation'][r], self.expected_cooperation)

    def test_run_parallel_repetitions(self):
        outcome = {'payoff': [], 'cooperation': []}
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions,
            processes=2)
        tournament._run_parallel_repetitions(outcome)
        self.assertEqual(len(outcome['payoff']), self.test_repetitions)
        self.assertEqual(len(outcome['cooperation']), self.test_repetitions)
        for r in range(self.test_repetitions):
            self.assertEqual(outcome['payoff'][r], self.expected_payoff)
            self.assertEqual(
                outcome['cooperation'][r], self.expected_cooperation)

    def test_n_workers(self):
        max_processes = multiprocessing.cpu_count()

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
        multiprocessing.cpu_count() < 2,
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
        work_queue = multiprocessing.Queue()
        done_queue = multiprocessing.Queue()
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
        done_queue = multiprocessing.Queue()
        outcome = {'payoff': [], 'cooperation': []}
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)
        for r in range(self.test_repetitions):
            done_queue.put(
                {'payoff': 'test_payoffs', 'cooperation': 'test_cooperation'})
        for w in range(workers):
            done_queue.put('STOP')
        tournament._process_done_queue(workers, done_queue, outcome)
        self.assertEqual(len(outcome['payoff']), self.test_repetitions)
        self.assertEqual(len(outcome['cooperation']), self.test_repetitions)
        for repetition in range(self.test_repetitions):
            self.assertEqual(outcome['payoff'][r], 'test_payoffs')
            self.assertEqual(outcome['cooperation'][r], 'test_cooperation')

    def test_worker(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)

        work_queue = multiprocessing.Queue()
        for repetition in range(self.test_repetitions):
            work_queue.put(repetition)
        work_queue.put('STOP')

        done_queue = multiprocessing.Queue()
        tournament._worker(work_queue, done_queue)
        for r in range(self.test_repetitions):
            output = done_queue.get()
            self.assertEqual(output['payoff'], self.expected_payoff)
            self.assertEqual(output['cooperation'], self.expected_cooperation)
        queue_stop = done_queue.get()
        self.assertEqual(queue_stop, 'STOP')

    def test_play_round_robin_mutable(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)
        output = tournament._play_round_robin()
        self.assertEqual(output['payoff'], self.expected_payoff)
        self.assertTrue(
            (axelrod.Cooperator, axelrod.Defector) in
            tournament.deterministic_cache)

    def test_play_round_robin_immutable(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)
        output = tournament._play_round_robin(cache_mutable=False)
        self.assertEqual(output['payoff'], self.expected_payoff)
        self.assertEqual(tournament.deterministic_cache, {})
