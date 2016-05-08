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
        self.assertTrue(tournament._with_morality)
        self.assertIsInstance(tournament._logger, logging.Logger)
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
        results = tournament.play()
        self.assertEqual(len(results.interactions), 15)

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
        self.assertEqual(results.players, [str(p) for p in players])

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

    #def test_run_parallel(self):
        #tournament = axelrod.Tournament(
            #name=self.test_name,
            #players=self.players,
            #game=self.game,
            #turns=200,
            #repetitions=self.test_repetitions,
            #processes=2)
        #tournament._run_parallel()
        #self.assertEqual(len(tournament.interactions), 15)
        #for r in tournament.interactions.values():
            #self.assertEqual(len(r), self.test_repetitions)

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
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)
        chunks = tournament.match_generator.build_match_chunks()
        for chunk in chunks:
            work_queue.put(chunk)
        tournament._start_workers(workers, work_queue, done_queue)

        stops = 0
        while stops < workers:
            payoffs = done_queue.get()
            if payoffs == 'STOP':
                stops += 1
        self.assertEqual(stops, workers)

    #def test_process_done_queue(self):
        #workers = 2
        #done_queue = Queue()
        #interactions = {}
        #tournament = axelrod.Tournament(
            #name=self.test_name,
            #players=self.players,
            #game=self.game,
            #turns=200,
            #repetitions=self.test_repetitions)
        #d = {}
        #count = 0
        #for i, _ in enumerate(self.players):
            #for j, _ in enumerate(self.players):
                #d[(i, j)] = []
                #count += 1
        #done_queue.put(d)
        #for w in range(workers):
            #done_queue.put('STOP')
        #tournament._process_done_queue(workers, done_queue)
        #self.assertEqual(len(tournament.interactions), count)

    def test_worker(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)

        work_queue = Queue()
        chunks = tournament.match_generator.build_match_chunks()
        count = 0
        for chunk in chunks:
            work_queue.put(chunk)
            count += 1
        work_queue.put('STOP')

        done_queue = Queue()
        tournament._worker(work_queue, done_queue)
        for r in range(count):
            new_matches = done_queue.get()
            for index_pair, matches in new_matches.items():
                self.assertIsInstance(index_pair, tuple)
                self.assertEqual(len(matches), self.test_repetitions)
        queue_stop = done_queue.get()
        self.assertEqual(queue_stop, 'STOP')

    def test_build_result_set(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=200,
            repetitions=self.test_repetitions)
        tournament.play()
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

        def make_chunk_generator():
            """
            A generator that returns player index pairs and match objects for a
            round robin tournament.

            Parameters
            ----------
            noise : float, 0
                The probability that a player's intended action should be flipped
            chunked : bool, False
                Yield matches in chunks by repetition or not

            Yields
            -------
            tuples
                ((player1 index, player2 index), match object)
            """
            for player1_index in range(len(self.players)):
                for player2_index in range(player1_index, len(self.players)):
                    index_pair = (player1_index, player2_index)
                    match_params = (turns, self.game, None, 0)
                    yield (index_pair, match_params, self.test_repetitions)

        chunk_generator = make_chunk_generator()
        interactions = {}
        for chunk in chunk_generator:
            result = tournament._play_matches(chunk)
            for index_pair, inters in result.items():
                try:
                    interactions[index_pair].append(inters)
                except KeyError:
                    interactions[index_pair] = [inters]

        self.assertEqual(len(interactions), 15)

        for index_pair, inter in interactions.items():
            self.assertEqual(len(index_pair), 2)
            for plays in inter:
                # Check that have the expected number of repetitions
                self.assertEqual(len(plays), self.test_repetitions)
                for repetition in plays:
                    # Check that have the correct length for each rep
                    self.assertEqual(len(repetition), turns)

        # Check that matches no longer exist
        self.assertEqual((len(list(chunk_generator))), 0)

    def test_write_to_csv(self):
        tmp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=2,
            repetitions=2,
            filename=tmp_file.name)
        tournament.play()
        with open(tmp_file.name, 'r') as f:
            written_data = [[int(r[0]), int(r[1])] + r[2:] for r in csv.reader(f)]
            expected_data = [[0, 1, 'Cooperator', 'Tit For Tat', 'CC', 'CC'],
                             [0, 1, 'Cooperator', 'Tit For Tat', 'CC', 'CC'],
                             [1, 2, 'Tit For Tat', 'Defector', 'CD', 'DD'],
                             [1, 2, 'Tit For Tat', 'Defector', 'CD', 'DD'],
                             [0, 0, 'Cooperator', 'Cooperator', 'CC', 'CC'],
                             [0, 0, 'Cooperator', 'Cooperator', 'CC', 'CC'],
                             [3, 3, 'Grudger', 'Grudger', 'CC', 'CC'],
                             [3, 3, 'Grudger', 'Grudger', 'CC', 'CC'],
                             [2, 2, 'Defector', 'Defector', 'DD', 'DD'],
                             [2, 2, 'Defector', 'Defector', 'DD', 'DD'],
                             [4, 4, 'Soft Go By Majority', 'Soft Go By Majority', 'CC', 'CC'],
                             [4, 4, 'Soft Go By Majority', 'Soft Go By Majority', 'CC', 'CC'],
                             [1, 4, 'Tit For Tat', 'Soft Go By Majority', 'CC', 'CC'],
                             [1, 4, 'Tit For Tat', 'Soft Go By Majority', 'CC', 'CC'],
                             [1, 1, 'Tit For Tat', 'Tit For Tat', 'CC', 'CC'],
                             [1, 1, 'Tit For Tat', 'Tit For Tat', 'CC', 'CC'],
                             [1, 3, 'Tit For Tat', 'Grudger', 'CC', 'CC'],
                             [1, 3, 'Tit For Tat', 'Grudger', 'CC', 'CC'],
                             [2, 3, 'Defector', 'Grudger', 'DD', 'CD'],
                             [2, 3, 'Defector', 'Grudger', 'DD', 'CD'],
                             [0, 4, 'Cooperator', 'Soft Go By Majority', 'CC', 'CC'],
                             [0, 4, 'Cooperator', 'Soft Go By Majority', 'CC', 'CC'],
                             [2, 4, 'Defector', 'Soft Go By Majority', 'DD', 'CD'],
                             [2, 4, 'Defector', 'Soft Go By Majority', 'DD', 'CD'],
                             [0, 3, 'Cooperator', 'Grudger', 'CC', 'CC'],
                             [0, 3, 'Cooperator', 'Grudger', 'CC', 'CC'],
                             [3, 4, 'Grudger', 'Soft Go By Majority', 'CC', 'CC'],
                             [3, 4, 'Grudger', 'Soft Go By Majority', 'CC', 'CC'],
                             [0, 2, 'Cooperator', 'Defector', 'CC', 'DD'],
                             [0, 2, 'Cooperator', 'Defector', 'CC', 'DD']]
            self.assertEqual(sorted(written_data), sorted(expected_data))


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
        self.assertTrue(tournament._with_morality)
        self.assertIsInstance(tournament._logger, logging.Logger)
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
        self.assertEqual(results.players, [str(p) for p in players])
        for rep in results.interactions.values():
            self.assertEqual(len(rep), repetitions)
