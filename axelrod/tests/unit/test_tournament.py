"""Tests for the main tournament class."""

import csv
import logging
from multiprocessing import Queue, cpu_count
import unittest
from unittest.mock import MagicMock
import warnings

from hypothesis import given, example, settings
from hypothesis.strategies import integers, floats
from axelrod.tests.property import (tournaments,
                                    prob_end_tournaments,
                                    spatial_tournaments,
                                    strategy_lists)

import axelrod


C, D = axelrod.Action.C, axelrod.Action.D

test_strategies = [axelrod.Cooperator,
                   axelrod.TitForTat,
                   axelrod.Defector,
                   axelrod.Grudger,
                   axelrod.GoByMajority]
test_repetitions = 5
test_turns = 100

test_prob_end = .5

test_edges = [(0, 1), (1, 2), (3, 4)]

deterministic_strategies = [s for s in axelrod.strategies
                            if not s().classifier['stochastic']]


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

        cls.filename = "test_outputs/test_tournament.csv"

    def test_init(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=self.test_turns,
            noise=0.2)
        self.assertEqual(len(tournament.players), len(test_strategies))
        self.assertIsInstance(
            tournament.players[0].match_attributes['game'], axelrod.Game
        )
        self.assertEqual(tournament.game.score((C, C)), (3, 3))
        self.assertEqual(tournament.turns, self.test_turns)
        self.assertEqual(tournament.repetitions, 10)
        self.assertEqual(tournament.name, 'test')
        self.assertIsInstance(tournament._logger, logging.Logger)
        self.assertEqual(tournament.noise, 0.2)
        anonymous_tournament = axelrod.Tournament(players=self.players)
        self.assertEqual(anonymous_tournament.name, 'axelrod')

    def test_init_with_match_attributes(self):
        tournament = axelrod.Tournament(players=self.players,
                                        match_attributes={"length": -1})
        mg = tournament.match_generator
        match_params = mg.build_single_match_params()
        self.assertEqual(match_params["match_attributes"], {"length": -1})

    def test_warning(self):
        tournament = axelrod.Tournament(name=self.test_name,
                                        players=self.players,
                                        game=self.game,
                                        turns=10,
                                        repetitions=1)
        with warnings.catch_warnings(record=True) as w:
            # Check that a warning is raised if no results set is built and no
            # filename is given
            results = tournament.play(build_results=False, progress_bar=False)
            self.assertEqual(len(w), 1)

        with warnings.catch_warnings(record=True) as w:
            # Check that no warning is raised if no results set is built and a
            # is filename given

            tournament.play(build_results=False,
                            filename=self.filename, progress_bar=False)
            self.assertEqual(len(w), 0)

    def test_serial_play(self):
        # Test that we get an instance of ResultSet
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axelrod.DEFAULT_TURNS,
            repetitions=self.test_repetitions)
        results = tournament.play(progress_bar=False)
        self.assertIsInstance(results, axelrod.ResultSet)

        # Test that _run_serial_repetitions is called with empty matches list
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axelrod.DEFAULT_TURNS,
            repetitions=self.test_repetitions)
        results = tournament.play(progress_bar=False)
        self.assertEqual(tournament.num_interactions, 75)

    def test_serial_play_with_different_game(self):
        # Test that a non default game is passed to the result set
        game = axelrod.Game(p=-1, r=-1, s=-1, t=-1)
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=game,
            turns=1,
            repetitions=1)
        results = tournament.play(progress_bar=False)
        self.assertEqual(results.game.RPST(), (-1, -1, -1, -1))

    def test_no_progress_bar_play(self):
        """Test that progress bar is not created for progress_bar=False"""
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axelrod.DEFAULT_TURNS,
            repetitions=self.test_repetitions)


        # Test with build results
        results = tournament.play(progress_bar=False)
        self.assertIsInstance(results, axelrod.ResultSet)
        # Check that no progress bar was created
        call_progress_bar = lambda: tournament.progress_bar.total
        self.assertRaises(AttributeError, call_progress_bar)

        # Test without build results
        results = tournament.play(progress_bar=False, build_results=False,
                                  filename=self.filename)
        self.assertIsNone(results)
        results = axelrod.ResultSetFromFile(self.filename, progress_bar=False)
        self.assertIsInstance(results, axelrod.ResultSet)
        self.assertRaises(AttributeError, call_progress_bar)

    def test_progress_bar_play(self):
        """Test that progress bar is created by default and with True argument"""
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axelrod.DEFAULT_TURNS,
            repetitions=self.test_repetitions)

        results = tournament.play()
        self.assertIsInstance(results, axelrod.ResultSet)
        self.assertEqual(tournament.progress_bar.total, 15)
        self.assertEqual(tournament.progress_bar.total,
                         tournament.progress_bar.n)

        results = tournament.play(progress_bar=True)
        self.assertIsInstance(results, axelrod.ResultSet)
        self.assertEqual(tournament.progress_bar.total, 15)
        self.assertEqual(tournament.progress_bar.total,
                         tournament.progress_bar.n)

        # Test without build results
        results = tournament.play(progress_bar=True, build_results=False,
                                  filename=self.filename)
        self.assertIsNone(results)
        results = axelrod.ResultSetFromFile(self.filename)
        self.assertIsInstance(results, axelrod.ResultSet)
        self.assertEqual(tournament.progress_bar.total, 15)
        self.assertEqual(tournament.progress_bar.total,
                         tournament.progress_bar.n)

    @unittest.skipIf(axelrod.on_windows,
                     "Parallel processing not supported on Windows")
    def test_progress_bar_play_parallel(self):
        """Test that tournament plays when asking for progress bar for parallel
        tournament"""
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axelrod.DEFAULT_TURNS,
            repetitions=self.test_repetitions)

        results = tournament.play(processes=2)
        self.assertIsInstance(results, axelrod.ResultSet)

        results = tournament.play(progress_bar=True)
        self.assertIsInstance(results, axelrod.ResultSet)

    @given(tournament=tournaments(min_size=2, max_size=5, min_turns=2,
                                  max_turns=10, min_repetitions=2,
                                  max_repetitions=4))
    @settings(max_examples=10, timeout=0)
    @example(tournament=axelrod.Tournament(players=[s() for s in
        test_strategies], turns=test_turns, repetitions=test_repetitions)
        )

    # These two examples are to make sure #465 is fixed.
    # As explained there: https://github.com/Axelrod-Python/Axelrod/issues/465,
    # these two examples were identified by hypothesis.
    @example(tournament=
        axelrod.Tournament(players=[axelrod.BackStabber(),
                                    axelrod.MindReader()],
                           turns=2, repetitions=1),
        )
    @example(tournament=
        axelrod.Tournament(players=[axelrod.BackStabber(),
                                    axelrod.ThueMorse()],
                           turns=2, repetitions=1),
        )
    def test_property_serial_play(self, tournament):
        """Test serial play using hypothesis"""
        # Test that we get an instance of ResultSet
        results = tournament.play(progress_bar=False)
        self.assertIsInstance(results, axelrod.ResultSet)
        self.assertEqual(results.nplayers, len(tournament.players))
        self.assertEqual(results.players, [str(p) for p in tournament.players])

    @unittest.skipIf(axelrod.on_windows,
                     "Parallel processing not supported on Windows")
    def test_parallel_play(self):
        # Test that we get an instance of ResultSet
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axelrod.DEFAULT_TURNS,
            repetitions=self.test_repetitions)
        results = tournament.play(processes=2, progress_bar=False)
        self.assertIsInstance(results, axelrod.ResultSet)
        self.assertEqual(tournament.num_interactions, 75)

        # The following relates to #516
        players = [axelrod.Cooperator(), axelrod.Defector(),
                   axelrod.BackStabber(), axelrod.PSOGambler2_2_2(),
                   axelrod.ThueMorse(), axelrod.DoubleCrosser()]
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=players,
            game=self.game,
            turns=20,
            repetitions=self.test_repetitions)
        scores = tournament.play(processes=2, progress_bar=False).scores
        self.assertEqual(len(scores), len(players))

    def test_run_serial(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axelrod.DEFAULT_TURNS,
            repetitions=self.test_repetitions)
        tournament._write_interactions = MagicMock(
                    name='_write_interactions')
        self.assertTrue(tournament._run_serial())

        # Get the calls made to write_interactions
        calls = tournament._write_interactions.call_args_list
        self.assertEqual(len(calls), 15)

    @unittest.skipIf(axelrod.on_windows,
                     "Parallel processing not supported on Windows")
    def test_run_parallel(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axelrod.DEFAULT_TURNS,
            repetitions=self.test_repetitions)
        tournament._write_interactions = MagicMock(
                    name='_write_interactions')
        self.assertTrue(tournament._run_parallel())

        # Get the calls made to write_interactions
        calls = tournament._write_interactions.call_args_list
        self.assertEqual(len(calls), 15)

    @unittest.skipIf(axelrod.on_windows,
                     "Parallel processing not supported on Windows")
    def test_n_workers(self):
        max_processes = cpu_count()

        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axelrod.DEFAULT_TURNS,
            repetitions=self.test_repetitions)
        self.assertEqual(tournament._n_workers(processes=1), max_processes)

        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axelrod.DEFAULT_TURNS,
            repetitions=self.test_repetitions)
        self.assertEqual(tournament._n_workers(processes=max_processes+2),
                                               max_processes)

    @unittest.skipIf(axelrod.on_windows,
                     "Parallel processing not supported on Windows")
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
            turns=axelrod.DEFAULT_TURNS,
            repetitions=self.test_repetitions,)
        self.assertEqual(tournament._n_workers(processes=2), 2)

    @unittest.skipIf(axelrod.on_windows,
                     "Parallel processing not supported on Windows")
    def test_start_workers(self):
        workers = 2
        work_queue = Queue()
        done_queue = Queue()
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axelrod.DEFAULT_TURNS,
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

    @unittest.skipIf(axelrod.on_windows,
                     "Parallel processing not supported on Windows")
    def test_worker(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axelrod.DEFAULT_TURNS,
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
            turns=axelrod.DEFAULT_TURNS,
            repetitions=self.test_repetitions)
        results = tournament.play(progress_bar=False)
        self.assertIsInstance(results, axelrod.ResultSet)

        # Test in memory
        results = tournament.play(progress_bar=False, in_memory=True)
        self.assertIsInstance(results, axelrod.ResultSet)

    def test_no_build_result_set(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axelrod.DEFAULT_TURNS,
            repetitions=self.test_repetitions)

        results = tournament.play(build_results=False, filename=self.filename,
                                  progress_bar=False)
        self.assertIsNone(results)

        # Checking that results were written properly
        results = axelrod.ResultSetFromFile(self.filename, progress_bar=False)
        self.assertIsInstance(results, axelrod.ResultSet)

    @given(turns=integers(min_value=1, max_value=200))
    @example(turns=3)
    @example(turns=axelrod.DEFAULT_TURNS)
    def test_play_matches(self, turns):
        tournament = axelrod.Tournament(name=self.test_name,
                                        players=self.players,
                                        game=self.game,
                                        repetitions=self.test_repetitions)

        def make_chunk_generator():
            for player1_index in range(len(self.players)):
                for player2_index in range(player1_index, len(self.players)):
                    index_pair = (player1_index, player2_index)
                    match_params = {"turns": turns, "game": self.game}
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

    def test_match_cache_is_used(self):
        """
        Create two Random players that are classified as deterministic.
        As they are deterministic the cache will be used.
        """
        FakeRandom = axelrod.Random
        FakeRandom.classifier["stochastic"] = False
        p1 = FakeRandom()
        p2 = FakeRandom()
        tournament = axelrod.Tournament((p1, p2), turns=5, repetitions=2)
        results = tournament.play(progress_bar=False)
        for player_scores in results.scores:
            self.assertEqual(player_scores[0], player_scores[1])

    def test_write_interactions(self):
        tournament = axelrod.Tournament(

            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=2,
            repetitions=2)
        tournament._write_interactions = MagicMock(name='_write_interactions')
        # Mocking this as it is called by play
        tournament._build_result_set = MagicMock(name='_build_result_set')
        self.assertTrue(tournament.play(filename=self.filename,
                                        progress_bar=False))
        tournament.outputfile.close()  # Normally closed by `build_result_set`

        # Get the calls made to write_interactions
        calls = tournament._write_interactions.call_args_list
        self.assertEqual(len(calls), 15)

        # Test when running in memory
        tournament._write_interactions = MagicMock(name='_write_interactions')
        self.assertTrue(tournament.play(filename=self.filename,
                                        progress_bar=False,
                                        in_memory=False))
        # Get the calls made to write_interactions
        calls = tournament._write_interactions.call_args_list
        self.assertEqual(len(calls), 15)
        tournament.outputfile.close()  # Normally closed by `write_interactions`

    def test_write_to_csv(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=2,
            repetitions=2)
        tournament.play(filename=self.filename, progress_bar=False)
        with open(self.filename, 'r') as f:
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
        tournament = axelrod.Tournament(name=self.test_name,
                                        players=self.players,
                                        game=self.game,
                                        prob_end=self.test_prob_end,
                                        noise=0.2)
        self.assertEqual(tournament.match_generator.prob_end, tournament.prob_end)
        self.assertEqual(len(tournament.players), len(test_strategies))
        self.assertEqual(tournament.game.score((C, C)), (3, 3))
        self.assertIsNone(tournament.turns)
        self.assertEqual(tournament.repetitions, 10)
        self.assertEqual(tournament.name, 'test')
        self.assertIsInstance(tournament._logger, logging.Logger)
        self.assertEqual(tournament.noise, 0.2)
        anonymous_tournament = axelrod.Tournament(players=self.players)
        self.assertEqual(anonymous_tournament.name, 'axelrod')

    @given(tournament=prob_end_tournaments(min_size=2, max_size=5,
                                           min_prob_end=.1,
                                           max_prob_end=.9,
                                           min_repetitions=2,
                                           max_repetitions=4))
    @settings(max_examples=50, timeout=0)
    @example(tournament=
        axelrod.Tournament(players=[s() for s in test_strategies],
                           prob_end=.2, repetitions=test_repetitions))

    # These two examples are to make sure #465 is fixed.
    # As explained there: https://github.com/Axelrod-Python/Axelrod/issues/465,
    # these two examples were identified by hypothesis.
    @example(tournament=
        axelrod.Tournament(players=[axelrod.BackStabber(),
                                    axelrod.MindReader()],
                           prob_end=.2, repetitions=1))
    @example(tournament=
        axelrod.Tournament(players=[axelrod.ThueMorse(),
                                           axelrod.MindReader()],
                                  prob_end=.2, repetitions=1))
    def test_property_serial_play(self, tournament):
        """Test serial play using hypothesis"""
        # Test that we get an instance of ResultSet
        results = tournament.play(progress_bar=False)
        self.assertIsInstance(results, axelrod.ResultSet)
        self.assertEqual(results.nplayers, len(tournament.players))
        self.assertEqual(results.players, [str(p) for p in tournament.players])


class TestSpatialTournament(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()
        cls.players = [s() for s in test_strategies]
        cls.test_name = 'test'
        cls.test_repetitions = test_repetitions
        cls.test_turns = test_turns
        cls.test_edges = test_edges

    def test_init(self):
        tournament = axelrod.Tournament(name=self.test_name,
                                        players=self.players,
                                        game=self.game,
                                        turns=self.test_turns,
                                        edges=self.test_edges,
                                        noise=0.2)
        self.assertEqual(tournament.match_generator.edges, tournament.edges)
        self.assertEqual(len(tournament.players), len(test_strategies))
        self.assertEqual(tournament.game.score((C, C)), (3, 3))
        self.assertEqual(tournament.turns, 100)
        self.assertEqual(tournament.repetitions, 10)
        self.assertEqual(tournament.name, 'test')
        self.assertIsInstance(tournament._logger, logging.Logger)
        self.assertEqual(tournament.noise, 0.2)
        self.assertEqual(tournament.match_generator.noise, 0.2)
        anonymous_tournament = axelrod.Tournament(players=self.players)
        self.assertEqual(anonymous_tournament.name, 'axelrod')

    @given(strategies=strategy_lists(strategies=deterministic_strategies,
                                     min_size=2, max_size=2),
           turns=integers(min_value=1, max_value=20),
           repetitions=integers(min_value=1, max_value=5),
           noise=floats(min_value=0, max_value=1),
           seed=integers(min_value=0, max_value=4294967295))
    @settings(max_examples=50, timeout=0)
    def test_complete_tournament(self, strategies, turns, repetitions,
                                 noise, seed):
        """
        A test to check that a spatial tournament on the complete multigraph
        gives the same results as the round robin.
        """

        players = [s() for s in strategies]
        # edges
        edges = []
        for i in range(0, len(players)):
            for j in range(i, len(players)):
                edges.append((i, j))

        # create a round robin tournament
        tournament = axelrod.Tournament(players, repetitions=repetitions,
                                        turns=turns, noise=noise)
        # create a complete spatial tournament
        spatial_tournament = axelrod.Tournament(players,
                                                repetitions=repetitions,
                                                turns=turns,
                                                noise=noise,
                                                edges=edges)

        axelrod.seed(seed)
        results = tournament.play(progress_bar=False)
        axelrod.seed(seed)
        spatial_results = spatial_tournament.play(progress_bar=False)

        self.assertEqual(results.ranked_names, spatial_results.ranked_names)
        self.assertEqual(results.nplayers, spatial_results.nplayers)
        self.assertEqual(results.repetitions, spatial_results.repetitions)
        self.assertEqual(results.payoff_diffs_means,
                         spatial_results.payoff_diffs_means)
        self.assertEqual(results.payoff_matrix, spatial_results.payoff_matrix)
        self.assertEqual(results.payoff_stddevs, spatial_results.payoff_stddevs)
        self.assertEqual(results.payoffs, spatial_results.payoffs)
        self.assertEqual(results.cooperating_rating,
                         spatial_results.cooperating_rating)
        self.assertEqual(results.cooperation, spatial_results.cooperation)
        self.assertEqual(results.normalised_cooperation,
                         spatial_results.normalised_cooperation)
        self.assertEqual(results.normalised_scores,
                         spatial_results.normalised_scores)
        self.assertEqual(results.good_partner_matrix,
                         spatial_results.good_partner_matrix)
        self.assertEqual(results.good_partner_rating,
                         spatial_results.good_partner_rating)

    def test_particular_tournament(self):
        """A test for a tournament that has caused failures during some bug
        fixing"""
        players = [axelrod.Cooperator(), axelrod.Defector(),
                   axelrod.TitForTat(), axelrod.Grudger()]
        edges = [(0, 2), (0, 3), (1, 2), (1, 3)]
        tournament = axelrod.Tournament(players, edges=edges)
        results = tournament.play(progress_bar=False)
        expected_ranked_names = ['Cooperator', 'Tit For Tat',
                                 'Grudger', 'Defector']
        self.assertEqual(results.ranked_names, expected_ranked_names)

        # Check that this tournament runs with noise
        tournament = axelrod.Tournament(players, edges=edges, noise=.5)
        results = tournament.play(progress_bar=False)
        self.assertIsInstance(results, axelrod.ResultSet)


class TestProbEndingSpatialTournament(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()
        cls.players = [s() for s in test_strategies]
        cls.test_name = 'test'
        cls.test_repetitions = test_repetitions
        cls.test_prob_end = test_prob_end
        cls.test_edges = test_edges

    def test_init(self):
        tournament = axelrod.Tournament(name=self.test_name,
                                        players=self.players,
                                        game=self.game,
                                        prob_end=self.test_prob_end,
                                        edges=self.test_edges,
                                        noise=0.2)
        self.assertEqual(tournament.match_generator.edges, tournament.edges)
        self.assertEqual(len(tournament.players), len(test_strategies))
        self.assertEqual(tournament.game.score((C, C)), (3, 3))
        self.assertIsNone(tournament.turns)
        self.assertEqual(tournament.repetitions, 10)
        self.assertEqual(tournament.name, 'test')
        self.assertIsInstance(tournament._logger, logging.Logger)
        self.assertEqual(tournament.noise, 0.2)
        self.assertEqual(tournament.match_generator.noise, 0.2)
        self.assertEqual(tournament.prob_end, self.test_prob_end)

    @given(strategies=strategy_lists(strategies=deterministic_strategies,
                                     min_size=2, max_size=2),
           prob_end=floats(min_value=.1, max_value=.9),
           reps=integers(min_value=1, max_value=3),
           seed=integers(min_value=0, max_value=4294967295))
    @settings(max_examples=50, timeout=0)
    def test_complete_tournament(self, strategies, prob_end,
                                 seed, reps):
        """
        A test to check that a spatial tournament on the complete graph
        gives the same results as the round robin.
        """
        players = [s() for s in strategies]

        # create a prob end round robin tournament
        tournament = axelrod.Tournament(players, prob_end=prob_end,
                                        repetitions=reps)
        axelrod.seed(seed)
        results = tournament.play(progress_bar=False)

        # create a complete spatial tournament
        # edges
        edges = [(i, j) for i in range(len(players))
                 for j in range(i, len(players))]

        spatial_tournament = axelrod.Tournament(players, prob_end=prob_end,
                                                repetitions=reps,
                                                edges=edges)
        axelrod.seed(seed)
        spatial_results = spatial_tournament.play(progress_bar=False)
        self.assertEqual(results.match_lengths, spatial_results.match_lengths)
        self.assertEqual(results.ranked_names, spatial_results.ranked_names)
        self.assertEqual(results.wins, spatial_results.wins)
        self.assertEqual(results.scores, spatial_results.scores)
        self.assertEqual(results.cooperation,
                         spatial_results.cooperation)


    @given(tournament=spatial_tournaments(strategies=axelrod.basic_strategies,
                                          max_turns=1, max_noise=0,
                                          max_repetitions=3),
           seed=integers(min_value=0, max_value=4294967295))
    @settings(max_examples=50, timeout=0)
    def test_one_turn_tournament(self, tournament, seed):
        """
        Tests that gives same result as the corresponding spatial round robin
        spatial tournament
        """
        prob_end_tour = axelrod.Tournament(tournament.players,
                                           prob_end=1,
                                           edges=tournament.edges,
                                           repetitions=tournament.repetitions)
        axelrod.seed(seed)
        prob_end_results = prob_end_tour.play(progress_bar=False)
        axelrod.seed(seed)
        one_turn_results = tournament.play(progress_bar=False)
        self.assertEqual(prob_end_results.scores,
                         one_turn_results.scores)
        self.assertEqual(prob_end_results.wins,
                         one_turn_results.wins)
        self.assertEqual(prob_end_results.cooperation,
                         one_turn_results.cooperation)
