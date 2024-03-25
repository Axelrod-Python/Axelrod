"""Tests for the main tournament class."""

import io
import logging
import os
import pathlib
import pickle
import unittest
import warnings
from multiprocessing import Queue, cpu_count
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
from hypothesis import example, given, settings
from hypothesis.strategies import floats, integers
from tqdm import tqdm

import axelrod as axl
from axelrod.load_data_ import axl_filename
from axelrod.tests.property import (
    prob_end_tournaments,
    spatial_tournaments,
    strategy_lists,
    tournaments,
)
from axelrod.tournament import _close_objects

C, D = axl.Action.C, axl.Action.D

test_strategies = [
    axl.Cooperator,
    axl.TitForTat,
    axl.Defector,
    axl.Grudger,
    axl.GoByMajority,
]
test_repetitions = 5
test_turns = 100

test_prob_end = 0.5

test_edges = [(0, 1), (1, 2), (3, 4)]

deterministic_strategies = [
    s
    for s in axl.short_run_time_strategies
    if not axl.Classifiers["stochastic"](s())
]


class RecordedTQDM(tqdm):
    """This is a tqdm.tqdm that keeps a record of every RecordedTQDM created.
    It is used to test that progress bars were correctly created and then
    closed."""

    record = []

    def __init__(self, *args, **kwargs):
        super(RecordedTQDM, self).__init__(*args, **kwargs)
        RecordedTQDM.record.append(self)

    @classmethod
    def reset_record(cls):
        cls.record = []


class TestTournament(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = axl.Game()
        cls.players = [s() for s in test_strategies]
        cls.test_name = "test"
        cls.test_repetitions = test_repetitions
        cls.test_turns = test_turns

        cls.expected_payoff = [
            [600, 600, 0, 600, 600],
            [600, 600, 199, 600, 600],
            [1000, 204, 200, 204, 204],
            [600, 600, 199, 600, 600],
            [600, 600, 199, 600, 600],
        ]

        cls.expected_cooperation = [
            [200, 200, 200, 200, 200],
            [200, 200, 1, 200, 200],
            [0, 0, 0, 0, 0],
            [200, 200, 1, 200, 200],
            [200, 200, 1, 200, 200],
        ]

        path = pathlib.Path("test_outputs/test_tournament.csv")
        cls.filename = axl_filename(path)

    def setUp(self):
        self.test_tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=2,
            repetitions=1,
        )

    def test_init(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=self.test_turns,
            noise=0.2,
        )
        self.assertEqual(len(tournament.players), len(test_strategies))
        self.assertIsInstance(
            tournament.players[0].match_attributes["game"], axl.Game
        )
        self.assertEqual(tournament.game.score((C, C)), (3, 3))
        self.assertEqual(tournament.turns, self.test_turns)
        self.assertEqual(tournament.repetitions, 10)
        self.assertEqual(tournament.name, "test")
        self.assertIsInstance(tournament._logger, logging.Logger)
        self.assertEqual(tournament.noise, 0.2)
        anonymous_tournament = axl.Tournament(players=self.players)
        self.assertEqual(anonymous_tournament.name, "axelrod")

    def test_init_with_match_attributes(self):
        tournament = axl.Tournament(
            players=self.players, match_attributes={"length": float("inf")}
        )
        mg = tournament.match_generator
        match_params = mg.build_single_match_params()
        self.assertEqual(
            match_params["match_attributes"], {"length": float("inf")}
        )

    def test_warning(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=10,
            repetitions=1,
        )
        with warnings.catch_warnings(record=True) as w:
            # Check that a warning is raised if no results set is built and no
            # filename is given
            results = tournament.play(build_results=False, progress_bar=False)
            self.assertEqual(len(w), 1)

        with warnings.catch_warnings(record=True) as w:
            # Check that no warning is raised if no results set is built and a
            # is filename given

            tournament.play(
                build_results=False, filename=self.filename, progress_bar=False
            )
            self.assertEqual(len(w), 0)

    def test_setup_output_with_filename(self):

        self.test_tournament.setup_output(self.filename)

        self.assertEqual(self.test_tournament.filename, self.filename)
        self.assertIsNone(self.test_tournament._temp_file_descriptor)
        self.assertFalse(hasattr(self.test_tournament, "interactions_dict"))

    def test_setup_output_no_filename(self):
        self.test_tournament.setup_output()

        self.assertIsInstance(self.test_tournament.filename, str)
        self.assertIsInstance(self.test_tournament._temp_file_descriptor, int)
        self.assertFalse(hasattr(self.test_tournament, "interactions_dict"))

        os.close(self.test_tournament._temp_file_descriptor)
        os.remove(self.test_tournament.filename)

    def test_play_resets_num_interactions(self):
        self.assertEqual(self.test_tournament.num_interactions, 0)
        self.test_tournament.play(progress_bar=False)
        self.assertEqual(self.test_tournament.num_interactions, 15)

        self.test_tournament.play(progress_bar=False)
        self.assertEqual(self.test_tournament.num_interactions, 15)

    def test_play_changes_use_progress_bar(self):
        self.assertTrue(self.test_tournament.use_progress_bar)

        self.test_tournament.play(progress_bar=False)
        self.assertFalse(self.test_tournament.use_progress_bar)

        self.test_tournament.play(progress_bar=True)
        self.assertTrue(self.test_tournament.use_progress_bar)

    def test_play_changes_temp_file_descriptor(self):
        self.assertIsNone(self.test_tournament._temp_file_descriptor)

        # No file descriptor for a named file.
        self.test_tournament.play(filename=self.filename, progress_bar=False)
        self.assertIsNone(self.test_tournament._temp_file_descriptor)

        # Temp file creates file descriptor.
        self.test_tournament.play(filename=None, progress_bar=False)
        self.assertIsInstance(self.test_tournament._temp_file_descriptor, int)

    def test_play_tempfile_removed(self):
        self.test_tournament.play(filename=None, progress_bar=False)

        self.assertFalse(os.path.isfile(self.test_tournament.filename))

    def test_play_resets_filename_and_temp_file_descriptor_each_time(self):
        self.test_tournament.play(progress_bar=False)
        self.assertIsInstance(self.test_tournament._temp_file_descriptor, int)
        self.assertIsInstance(self.test_tournament.filename, str)
        old_filename = self.test_tournament.filename

        self.test_tournament.play(filename=self.filename, progress_bar=False)
        self.assertIsNone(self.test_tournament._temp_file_descriptor)
        self.assertEqual(self.test_tournament.filename, self.filename)
        self.assertNotEqual(old_filename, self.test_tournament.filename)

        self.test_tournament.play(progress_bar=False)
        self.assertIsInstance(self.test_tournament._temp_file_descriptor, int)
        self.assertIsInstance(self.test_tournament.filename, str)
        self.assertNotEqual(old_filename, self.test_tournament.filename)
        self.assertNotEqual(self.test_tournament.filename, self.filename)

    def test_get_file_objects_no_filename(self):
        file, writer = self.test_tournament._get_file_objects()
        self.assertIsNone(file)
        self.assertIsNone(writer)

    def test_get_file_object_with_filename(self):
        self.test_tournament.filename = self.filename
        file_object, writer = self.test_tournament._get_file_objects()
        self.assertIsInstance(file_object, io.TextIOWrapper)
        self.assertEqual(writer.__class__.__name__, "writer")
        file_object.close()

    def test_get_progress_bar(self):
        self.test_tournament.use_progress_bar = False
        pbar = self.test_tournament._get_progress_bar()
        self.assertIsNone(pbar)

        self.test_tournament.use_progress_bar = True
        pbar = self.test_tournament._get_progress_bar()
        self.assertIsInstance(pbar, tqdm)
        self.assertEqual(pbar.desc, "Playing matches")
        self.assertEqual(pbar.n, 0)
        self.assertEqual(pbar.total, self.test_tournament.match_generator.size)

        new_edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
        new_tournament = axl.Tournament(players=self.players, edges=new_edges)
        new_tournament.use_progress_bar = True
        pbar = new_tournament._get_progress_bar()
        self.assertEqual(pbar.desc, "Playing matches")
        self.assertEqual(pbar.n, 0)
        self.assertEqual(pbar.total, len(new_edges))

    def test_serial_play(self):
        # Test that we get an instance of ResultSet
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )
        results = tournament.play(progress_bar=False)
        self.assertIsInstance(results, axl.ResultSet)

        # Test that _run_serial_repetitions is called with empty matches list
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )
        results = tournament.play(progress_bar=False)
        self.assertEqual(tournament.num_interactions, 75)

    def test_serial_play_with_different_game(self):
        # Test that a non default game is passed to the result set
        game = axl.Game(p=-1, r=-1, s=-1, t=-1)
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=game,
            turns=1,
            repetitions=1,
        )
        results = tournament.play(progress_bar=False)
        self.assertLessEqual(np.max(results.scores), 0)

    @patch("tqdm.tqdm", RecordedTQDM)
    def test_no_progress_bar_play(self):
        """Test that progress bar is not created for progress_bar=False"""
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )

        # Test with build results
        RecordedTQDM.reset_record()
        results = tournament.play(progress_bar=False)
        self.assertIsInstance(results, axl.ResultSet)
        # Check that no progress bar was created.
        self.assertEqual(RecordedTQDM.record, [])

        # Test without build results
        RecordedTQDM.reset_record()
        results = tournament.play(
            progress_bar=False, build_results=False, filename=self.filename
        )
        self.assertIsNone(results)
        self.assertEqual(RecordedTQDM.record, [])

    def assert_play_pbar_correct_total_and_finished(self, pbar, total):
        self.assertEqual(pbar.desc, "Playing matches")
        self.assertEqual(pbar.total, total)
        self.assertEqual(pbar.n, total)
        self.assertTrue(pbar.disable, True)

    @patch("tqdm.tqdm", RecordedTQDM)
    def test_progress_bar_play(self):
        """Test that progress bar is created by default and with True argument"""
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )

        RecordedTQDM.reset_record()
        results = tournament.play()
        self.assertIsInstance(results, axl.ResultSet)
        # Check that progress bar was created, updated and closed.
        self.assertEqual(len(RecordedTQDM.record), 2)
        play_pbar = RecordedTQDM.record[0]
        self.assert_play_pbar_correct_total_and_finished(play_pbar, total=15)
        # Check all progress bars are closed.
        self.assertTrue(all(pbar.disable for pbar in RecordedTQDM.record))

        RecordedTQDM.reset_record()
        results = tournament.play(progress_bar=True)
        self.assertIsInstance(results, axl.ResultSet)
        self.assertEqual(len(RecordedTQDM.record), 2)
        play_pbar = RecordedTQDM.record[0]
        self.assert_play_pbar_correct_total_and_finished(play_pbar, total=15)

        # Test without build results
        RecordedTQDM.reset_record()
        results = tournament.play(
            progress_bar=True, build_results=False, filename=self.filename
        )
        self.assertIsNone(results)
        self.assertEqual(len(RecordedTQDM.record), 1)
        play_pbar = RecordedTQDM.record[0]
        self.assert_play_pbar_correct_total_and_finished(play_pbar, total=15)

    @patch("tqdm.tqdm", RecordedTQDM)
    def test_progress_bar_play_parallel(self):
        """Test that tournament plays when asking for progress bar for parallel
        tournament and that progress bar is created."""
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )

        # progress_bar = False
        RecordedTQDM.reset_record()
        results = tournament.play(progress_bar=False, processes=2)
        self.assertEqual(RecordedTQDM.record, [])
        self.assertIsInstance(results, axl.ResultSet)

        # progress_bar = True
        RecordedTQDM.reset_record()
        results = tournament.play(progress_bar=True, processes=2)
        self.assertIsInstance(results, axl.ResultSet)

        self.assertEqual(len(RecordedTQDM.record), 2)
        play_pbar = RecordedTQDM.record[0]
        self.assert_play_pbar_correct_total_and_finished(play_pbar, total=15)

        # progress_bar is default
        RecordedTQDM.reset_record()
        results = tournament.play(processes=2)
        self.assertIsInstance(results, axl.ResultSet)

        self.assertEqual(len(RecordedTQDM.record), 2)
        play_pbar = RecordedTQDM.record[0]
        self.assert_play_pbar_correct_total_and_finished(play_pbar, total=15)

    @given(
        tournament=tournaments(
            min_size=2,
            max_size=5,
            min_turns=2,
            max_turns=5,
            min_repetitions=2,
            max_repetitions=4,
        )
    )
    @settings(max_examples=50, deadline=None)
    @example(
        tournament=axl.Tournament(
            players=[s() for s in test_strategies],
            turns=test_turns,
            repetitions=test_repetitions,
        )
    )
    # This example is to make sure #465 is fixed.
    # As explained there: https://github.com/Axelrod-Python/Axelrod/issues/465,
    # this example was identified by hypothesis.
    @example(
        tournament=axl.Tournament(
            players=[axl.BackStabber(), axl.ThueMorse()], turns=2, repetitions=1
        )
    )
    def test_property_serial_play(self, tournament):
        """Test serial play using hypothesis"""
        # Test that we get an instance of ResultSet
        results = tournament.play(progress_bar=False)
        self.assertIsInstance(results, axl.ResultSet)
        self.assertEqual(results.num_players, len(tournament.players))
        self.assertEqual(results.players, [str(p) for p in tournament.players])

    def test_parallel_play(self):
        # Test that we get an instance of ResultSet
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )
        results = tournament.play(processes=2, progress_bar=False)
        self.assertIsInstance(results, axl.ResultSet)
        self.assertEqual(tournament.num_interactions, 75)

        # The following relates to #516
        players = [
            axl.Cooperator(),
            axl.Defector(),
            axl.BackStabber(),
            axl.PSOGambler2_2_2(),
            axl.ThueMorse(),
            axl.DoubleCrosser(),
        ]
        tournament = axl.Tournament(
            name=self.test_name,
            players=players,
            game=self.game,
            turns=20,
            repetitions=self.test_repetitions,
        )
        scores = tournament.play(processes=2, progress_bar=False).scores
        self.assertEqual(len(scores), len(players))

    def test_parallel_play_with_writing_to_file(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )

        results = tournament.play(
            processes=2, progress_bar=False, filename=self.filename
        )
        self.assertIsInstance(results, axl.ResultSet)
        self.assertEqual(tournament.num_interactions, 75)

    def test_run_serial(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )
        tournament._write_interactions_to_file = MagicMock(
            name="_write_interactions_to_file"
        )
        self.assertTrue(tournament._run_serial())

        # Get the calls made to write_interactions
        calls = tournament._write_interactions_to_file.call_args_list
        self.assertEqual(len(calls), 15)

    def test_run_parallel(self):
        class PickleableMock(MagicMock):
            def __reduce__(self):
                return MagicMock, ()

        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )
        tournament._write_interactions_to_file = PickleableMock(
            name="_write_interactions_to_file"
        )

        # For test coverage purposes. This confirms PickleableMock can be
        # pickled exactly once. Windows multi-processing must pickle this Mock
        # exactly once during testing.
        pickled = pickle.loads(pickle.dumps(tournament))
        self.assertIsInstance(pickled._write_interactions_to_file, MagicMock)
        self.assertRaises(pickle.PicklingError, pickle.dumps, pickled)

        self.assertTrue(tournament._run_parallel())

        # Get the calls made to write_interactions
        calls = tournament._write_interactions_to_file.call_args_list
        self.assertEqual(len(calls), 15)

    def test_n_workers(self):
        max_processes = cpu_count()

        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )
        self.assertEqual(tournament._n_workers(processes=1), max_processes)

        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )
        self.assertEqual(
            tournament._n_workers(processes=max_processes + 2), max_processes
        )

    @unittest.skipIf(
        cpu_count() < 2, "not supported on single processor machines"
    )
    def test_2_workers(self):
        # This is a separate test with a skip condition because we
        # cannot guarantee that the tests will always run on a machine
        # with more than one processor
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )
        self.assertEqual(tournament._n_workers(processes=2), 2)

    def test_start_workers(self):
        workers = 2
        work_queue = Queue()
        done_queue = Queue()
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )
        chunks = tournament.match_generator.build_match_chunks()
        for chunk in chunks:
            work_queue.put(chunk)
        tournament._start_workers(workers, work_queue, done_queue)

        stops = 0
        while stops < workers:
            payoffs = done_queue.get()
            if payoffs == "STOP":
                stops += 1
        self.assertEqual(stops, workers)

    def test_worker(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )

        work_queue = Queue()
        chunks = tournament.match_generator.build_match_chunks()
        count = 0
        for chunk in chunks:
            work_queue.put(chunk)
            count += 1
        work_queue.put("STOP")

        done_queue = Queue()
        tournament._worker(work_queue, done_queue)
        for r in range(count):
            new_matches = done_queue.get()
            for index_pair, matches in new_matches.items():
                self.assertIsInstance(index_pair, tuple)
                self.assertEqual(len(matches), self.test_repetitions)
        queue_stop = done_queue.get()
        self.assertEqual(queue_stop, "STOP")

    def test_build_result_set(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )
        results = tournament.play(progress_bar=False)
        self.assertIsInstance(results, axl.ResultSet)

    def test_no_build_result_set(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )

        tournament._calculate_results = MagicMock(name="_calculate_results")
        # Mocking this as it is called by play
        self.assertIsNone(
            tournament.play(
                filename=self.filename, progress_bar=False, build_results=False
            )
        )

        # Get the calls made to write_interactions
        calls = tournament._calculate_results.call_args_list
        self.assertEqual(len(calls), 0)

    @given(turns=integers(min_value=1, max_value=200))
    @settings(max_examples=5, deadline=None)
    @example(turns=3)
    @example(turns=axl.DEFAULT_TURNS)
    def test_play_matches(self, turns):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            repetitions=self.test_repetitions,
        )

        def make_chunk_generator():
            for player1_index in range(len(self.players)):
                for player2_index in range(player1_index, len(self.players)):
                    index_pair = (player1_index, player2_index)
                    match_params = {"turns": turns, "game": self.game}
                    yield (index_pair, match_params, self.test_repetitions, 0)

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
                    actions, results = repetition
                    self.assertEqual(len(actions), turns)
                    self.assertEqual(len(results), 10)

        # Check that matches no longer exist
        self.assertEqual((len(list(chunk_generator))), 0)

    def test_write_interactions(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=2,
            repetitions=2,
        )
        tournament._write_interactions_to_file = MagicMock(
            name="_write_interactions_to_file"
        )
        # Mocking this as it is called by play
        self.assertIsNone(
            tournament.play(
                filename=self.filename, progress_bar=False, build_results=False
            )
        )

        # Get the calls made to write_interactions
        calls = tournament._write_interactions_to_file.call_args_list
        self.assertEqual(len(calls), 15)

    def test_write_to_csv_with_results(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=2,
            repetitions=2,
        )
        tournament.play(filename=self.filename, progress_bar=False)
        df = pd.read_csv(self.filename)
        path = pathlib.Path("test_outputs/expected_test_tournament.csv")
        expected_df = pd.read_csv(axl_filename(path))
        self.assertTrue(df.equals(expected_df))

    def test_write_to_csv_without_results(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=2,
            repetitions=2,
        )
        tournament.play(
            filename=self.filename, progress_bar=False, build_results=False
        )
        df = pd.read_csv(self.filename)
        path = pathlib.Path(
            "test_outputs/expected_test_tournament_no_results.csv"
        )
        expected_df = pd.read_csv(axl_filename(path))
        self.assertTrue(df.equals(expected_df))

    @given(seed=integers(min_value=1, max_value=4294967295))
    @example(seed=2)
    @settings(max_examples=5, deadline=None)
    def test_seeding_equality(self, seed):
        """Tests that a tournament with a given seed will return the
        same results each time. This specifically checks when running using
        multiple cores so as to confirm that
        https://github.com/Axelrod-Python/Axelrod/issues/1277
        is fixed.

        Note that the final asserts test only specific properties of the results
        sets and not the entire result sets as some floating point errors can
        emerge.
        """
        rng = axl.RandomGenerator(seed=seed)
        players = [axl.Random(rng.random()) for _ in range(8)]
        tournament1 = axl.Tournament(
            name=self.test_name,
            players=players,
            game=self.game,
            turns=10,
            repetitions=100,
            seed=seed,
        )
        tournament2 = axl.Tournament(
            name=self.test_name,
            players=players,
            game=self.game,
            turns=10,
            repetitions=100,
            seed=seed,
        )
        for _ in range(4):
            results1 = tournament1.play(processes=2, progress_bar=False)
            results2 = tournament2.play(processes=2, progress_bar=False)
            self.assertEqual(results1.wins, results2.wins)
            self.assertEqual(results1.match_lengths, results2.match_lengths)
            self.assertEqual(results1.scores, results2.scores)
            self.assertEqual(results1.cooperation, results2.cooperation)

    def test_seeding_inequality(self):
        players = [axl.Random(0.4), axl.Random(0.6)]
        tournament1 = axl.Tournament(
            name=self.test_name,
            players=players,
            game=self.game,
            turns=2,
            repetitions=2,
            seed=0,
        )
        tournament2 = axl.Tournament(
            name=self.test_name,
            players=players,
            game=self.game,
            turns=2,
            repetitions=2,
            seed=10,
        )
        results1 = tournament1.play()
        results2 = tournament2.play()
        self.assertNotEqual(results1, results2)


class TestProbEndTournament(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = axl.Game()
        cls.players = [s() for s in test_strategies]
        cls.test_name = "test"
        cls.test_repetitions = test_repetitions
        cls.test_prob_end = test_prob_end

    def test_init(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            prob_end=self.test_prob_end,
            noise=0.2,
        )
        self.assertEqual(
            tournament.match_generator.prob_end, tournament.prob_end
        )
        self.assertEqual(len(tournament.players), len(test_strategies))
        self.assertEqual(tournament.game.score((C, C)), (3, 3))
        self.assertIsNone(tournament.turns)
        self.assertEqual(tournament.repetitions, 10)
        self.assertEqual(tournament.name, "test")
        self.assertIsInstance(tournament._logger, logging.Logger)
        self.assertEqual(tournament.noise, 0.2)
        anonymous_tournament = axl.Tournament(players=self.players)
        self.assertEqual(anonymous_tournament.name, "axelrod")

    @given(
        tournament=prob_end_tournaments(
            min_size=2,
            max_size=5,
            min_prob_end=0.1,
            max_prob_end=0.9,
            min_repetitions=2,
            max_repetitions=4,
            seed=100,
        )
    )
    @settings(max_examples=5, deadline=None)
    @example(
        tournament=axl.Tournament(
            players=[s() for s in test_strategies],
            prob_end=0.2,
            repetitions=test_repetitions,
            seed=101,
        )
    )
    def test_property_serial_play(self, tournament):
        """Test serial play using hypothesis"""
        # Test that we get an instance of ResultSet
        results = tournament.play(progress_bar=False)
        self.assertIsInstance(results, axl.ResultSet)
        self.assertEqual(results.num_players, len(tournament.players))
        self.assertEqual(results.players, [str(p) for p in tournament.players])


class TestSpatialTournament(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = axl.Game()
        cls.players = [s() for s in test_strategies]
        cls.test_name = "test"
        cls.test_repetitions = test_repetitions
        cls.test_turns = test_turns
        cls.test_edges = test_edges

    def test_init(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=self.test_turns,
            edges=self.test_edges,
            noise=0.2,
        )
        self.assertEqual(tournament.match_generator.edges, tournament.edges)
        self.assertEqual(len(tournament.players), len(test_strategies))
        self.assertEqual(tournament.game.score((C, C)), (3, 3))
        self.assertEqual(tournament.turns, 100)
        self.assertEqual(tournament.repetitions, 10)
        self.assertEqual(tournament.name, "test")
        self.assertIsInstance(tournament._logger, logging.Logger)
        self.assertEqual(tournament.noise, 0.2)
        self.assertEqual(tournament.match_generator.noise, 0.2)
        anonymous_tournament = axl.Tournament(players=self.players)
        self.assertEqual(anonymous_tournament.name, "axelrod")

    @given(
        strategies=strategy_lists(
            strategies=deterministic_strategies, min_size=2, max_size=2
        ),
        turns=integers(min_value=1, max_value=20),
        repetitions=integers(min_value=1, max_value=5),
        noise=floats(min_value=0, max_value=1),
        seed=integers(min_value=0, max_value=4294967295),
    )
    @settings(max_examples=5, deadline=None)
    def test_complete_tournament(
        self, strategies, turns, repetitions, noise, seed
    ):
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
        tournament = axl.Tournament(
            players,
            repetitions=repetitions,
            turns=turns,
            noise=noise,
            seed=seed,
        )
        # create a complete spatial tournament
        spatial_tournament = axl.Tournament(
            players,
            repetitions=repetitions,
            turns=turns,
            noise=noise,
            edges=edges,
            seed=seed,
        )

        results = tournament.play(progress_bar=False)
        spatial_results = spatial_tournament.play(progress_bar=False)

        self.assertEqual(results.ranked_names, spatial_results.ranked_names)
        self.assertEqual(results.num_players, spatial_results.num_players)
        self.assertEqual(results.repetitions, spatial_results.repetitions)
        self.assertEqual(
            results.payoff_diffs_means, spatial_results.payoff_diffs_means
        )
        self.assertEqual(results.payoff_matrix, spatial_results.payoff_matrix)
        self.assertEqual(results.payoff_stddevs, spatial_results.payoff_stddevs)
        self.assertEqual(results.payoffs, spatial_results.payoffs)
        self.assertEqual(
            results.cooperating_rating, spatial_results.cooperating_rating
        )
        self.assertEqual(results.cooperation, spatial_results.cooperation)
        self.assertEqual(
            results.normalised_cooperation,
            spatial_results.normalised_cooperation,
        )
        self.assertEqual(
            results.normalised_scores, spatial_results.normalised_scores
        )
        self.assertEqual(
            results.good_partner_matrix, spatial_results.good_partner_matrix
        )
        self.assertEqual(
            results.good_partner_rating, spatial_results.good_partner_rating
        )

    def test_particular_tournament(self):
        """A test for a tournament that has caused failures during some bug
        fixing"""
        players = [
            axl.Cooperator(),
            axl.Defector(),
            axl.TitForTat(),
            axl.Grudger(),
        ]
        edges = [(0, 2), (0, 3), (1, 2), (1, 3)]
        tournament = axl.Tournament(players, edges=edges)
        results = tournament.play(progress_bar=False)
        expected_ranked_names = [
            "Cooperator",
            "Tit For Tat",
            "Grudger",
            "Defector",
        ]
        self.assertEqual(results.ranked_names, expected_ranked_names)

        # Check that this tournament runs with noise
        tournament = axl.Tournament(players, edges=edges, noise=0.5)
        results = tournament.play(progress_bar=False)
        self.assertIsInstance(results, axl.ResultSet)


class TestProbEndingSpatialTournament(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = axl.Game()
        cls.players = [s() for s in test_strategies]
        cls.test_name = "test"
        cls.test_repetitions = test_repetitions
        cls.test_prob_end = test_prob_end
        cls.test_edges = test_edges

    def test_init(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            prob_end=self.test_prob_end,
            edges=self.test_edges,
            noise=0.2,
        )
        self.assertEqual(tournament.match_generator.edges, tournament.edges)
        self.assertEqual(len(tournament.players), len(test_strategies))
        self.assertEqual(tournament.game.score((C, C)), (3, 3))
        self.assertIsNone(tournament.turns)
        self.assertEqual(tournament.repetitions, 10)
        self.assertEqual(tournament.name, "test")
        self.assertIsInstance(tournament._logger, logging.Logger)
        self.assertEqual(tournament.noise, 0.2)
        self.assertEqual(tournament.match_generator.noise, 0.2)
        self.assertEqual(tournament.prob_end, self.test_prob_end)

    @given(
        strategies=strategy_lists(
            strategies=deterministic_strategies, min_size=2, max_size=2
        ),
        prob_end=floats(min_value=0.1, max_value=0.9),
        reps=integers(min_value=1, max_value=3),
        seed=integers(min_value=0, max_value=4294967295),
    )
    @settings(max_examples=5, deadline=None)
    def test_complete_tournament(self, strategies, prob_end, seed, reps):
        """
        A test to check that a spatial tournament on the complete graph
        gives the same results as the round robin.
        """
        players = [s() for s in strategies]

        # create a prob end round robin tournament

        tournament = axl.Tournament(
            players, prob_end=prob_end, repetitions=reps, seed=seed
        )
        results = tournament.play(progress_bar=False)

        # create a complete spatial tournament
        # edges
        edges = [
            (i, j) for i in range(len(players)) for j in range(i, len(players))
        ]

        spatial_tournament = axl.Tournament(
            players, prob_end=prob_end, repetitions=reps, edges=edges, seed=seed
        )
        spatial_results = spatial_tournament.play(progress_bar=False)
        self.assertEqual(results.match_lengths, spatial_results.match_lengths)
        self.assertEqual(results.ranked_names, spatial_results.ranked_names)
        self.assertEqual(results.wins, spatial_results.wins)
        self.assertEqual(results.scores, spatial_results.scores)
        self.assertEqual(results.cooperation, spatial_results.cooperation)

    @given(
        tournament=spatial_tournaments(
            strategies=axl.basic_strategies,
            max_turns=1,
            max_noise=0,
            max_repetitions=3,
        ),
        seed=integers(min_value=0, max_value=4294967295),
    )
    @settings(max_examples=5, deadline=None)
    def test_one_turn_tournament(self, tournament, seed):
        """
        Tests that gives same result as the corresponding spatial round robin
        spatial tournament
        """
        prob_end_tour = axl.Tournament(
            tournament.players,
            prob_end=1,
            edges=tournament.edges,
            repetitions=tournament.repetitions,
            seed=seed,
        )
        prob_end_results = prob_end_tour.play(progress_bar=False)
        one_turn_results = tournament.play(progress_bar=False)
        self.assertEqual(prob_end_results.scores, one_turn_results.scores)
        self.assertEqual(prob_end_results.wins, one_turn_results.wins)
        self.assertEqual(
            prob_end_results.cooperation, one_turn_results.cooperation
        )


class TestHelperFunctions(unittest.TestCase):
    def test_close_objects_with_none(self):
        self.assertIsNone(_close_objects(None, None))

    def test_close_objects_with_file_objs(self):
        f1 = open("to_delete_1", "w")
        f2 = open("to_delete_2", "w")
        f2.close()
        f2 = open("to_delete_2", "r")

        self.assertFalse(f1.closed)
        self.assertFalse(f2.closed)

        _close_objects(f1, f2)

        self.assertTrue(f1.closed)
        self.assertTrue(f2.closed)

        os.remove("to_delete_1")
        os.remove("to_delete_2")

    def test_close_objects_with_tqdm(self):
        pbar_1 = tqdm(range(5))
        pbar_2 = tqdm(total=10, desc="hi", file=io.StringIO())

        self.assertFalse(pbar_1.disable)
        self.assertFalse(pbar_2.disable)

        _close_objects(pbar_1, pbar_2)

        self.assertTrue(pbar_1.disable)
        self.assertTrue(pbar_2.disable)

    def test_close_objects_with_different_objects(self):
        file = open("to_delete_1", "w")
        pbar = tqdm(range(5))
        num = 5
        empty = None
        word = "hi"

        _close_objects(file, pbar, num, empty, word)

        self.assertTrue(pbar.disable)
        self.assertTrue(file.closed)

        os.remove("to_delete_1")
