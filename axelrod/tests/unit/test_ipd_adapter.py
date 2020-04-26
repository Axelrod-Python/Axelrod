"""Tests adapters defined in ipd_adapter.

Tests that the public API (public methods and variables with accessors) matches
API on the Ipd versions of Player, Game, Match, and Tournament, by copying
relevant portions of those tests.
"""

from collections import Counter
import io
import logging
from multiprocessing import Queue, cpu_count
import os
import pathlib
import pickle
import random
import unittest
from unittest.mock import MagicMock, patch
import warnings

from hypothesis import example, given, settings
from hypothesis.strategies import assume, floats, integers, sampled_from
import numpy as np
import pandas as pd
from tqdm import tqdm

import axelrod as axl
from axelrod.deterministic_cache import DeterministicCache
from axelrod.load_data_ import axl_filename
from axelrod.player import simultaneous_play
from axelrod.tests.property import (
    games,
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

short_run_time_short_mem = [
    s
    for s in axl.short_run_time_strategies
    if axl.Classifiers["memory_depth"](s()) <= 10
]

# Classifiers for TitForTat
_test_classifier = {
    "memory_depth": 1,  # Four-Vector = (1.,0.,1.,0.)
    "stochastic": False,
    "makes_use_of": set(),
    "long_run_time": False,
    "inspects_source": False,
    "manipulates_source": False,
    "manipulates_state": False,
}


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


class TestGame(unittest.TestCase):
    def test_default_scores(self):
        expected_scores = {
            (C, D): (0, 5),
            (D, C): (5, 0),
            (D, D): (1, 1),
            (C, C): (3, 3),
        }
        self.assertEqual(axl.Game().scores, expected_scores)

    def test_default_RPST(self):
        expected_values = (3, 1, 0, 5)
        self.assertEqual(axl.Game().RPST(), expected_values)

    def test_default_score(self):
        game = axl.Game()
        self.assertEqual(game.score((C, C)), (3, 3))
        self.assertEqual(game.score((D, D)), (1, 1))
        self.assertEqual(game.score((C, D)), (0, 5))
        self.assertEqual(game.score((D, C)), (5, 0))

    def test_default_equality(self):
        self.assertEqual(axl.Game(), axl.Game())

    def test_not_default_equality(self):
        self.assertEqual(axl.Game(1, 2, 3, 4), axl.Game(1, 2, 3, 4))
        self.assertNotEqual(axl.Game(1, 2, 3, 4), axl.Game(1, 2, 3, 5))
        self.assertNotEqual(axl.Game(1, 2, 3, 4), axl.Game())

    def test_wrong_class_equality(self):
        self.assertNotEqual(axl.Game(), "wrong class")

    @given(r=integers(), p=integers(), s=integers(), t=integers())
    @settings(max_examples=5)
    def test_random_init(self, r, p, s, t):
        """Test init with random scores using the hypothesis library."""
        expected_scores = {
            (C, D): (s, t),
            (D, C): (t, s),
            (D, D): (p, p),
            (C, C): (r, r),
        }
        game = axl.Game(r, s, t, p)
        self.assertEqual(game.scores, expected_scores)

    @given(r=integers(), p=integers(), s=integers(), t=integers())
    @settings(max_examples=5)
    def test_random_RPST(self, r, p, s, t):
        """Test RPST method with random scores using the hypothesis library."""
        game = axl.Game(r, s, t, p)
        self.assertEqual(game.RPST(), (r, p, s, t))

    @given(r=integers(), p=integers(), s=integers(), t=integers())
    @settings(max_examples=5)
    def test_random_score(self, r, p, s, t):
        """Test score method with random scores using the hypothesis library."""
        game = axl.Game(r, s, t, p)
        self.assertEqual(game.score((C, C)), (r, r))
        self.assertEqual(game.score((D, D)), (p, p))
        self.assertEqual(game.score((C, D)), (s, t))
        self.assertEqual(game.score((D, C)), (t, s))

    @given(game=games())
    @settings(max_examples=5)
    def test_random_repr(self, game):
        """Test repr with random scores using the hypothesis library."""
        expected_repr = "Axelrod game: (R,P,S,T) = {}".format(game.RPST())
        self.assertEqual(expected_repr, game.__repr__())
        self.assertEqual(expected_repr, str(game))

    def test_scores_setter(self):
        expected_scores = {
            (C, D): (1, 2),
            (D, C): (2, 1),
            (D, D): (3, 3),
            (C, C): (4, 4),
        }
        game = axl.Game()
        game.scores = expected_scores
        self.assertDictEqual(game.scores, expected_scores)


class TestMatch(unittest.TestCase):
    @given(turns=integers(min_value=1, max_value=200), game=games())
    @example(turns=5, game=axl.DefaultGame)
    def test_init(self, turns, game):
        p1, p2 = axl.Cooperator(), axl.Cooperator()
        match = axl.Match((p1, p2), turns, game=game)
        self.assertEqual(match.result, [])
        self.assertEqual(match.players, [p1, p2])
        self.assertEqual(match.turns, turns)
        self.assertEqual(match.prob_end, 0)
        self.assertEqual(match.noise, 0)
        self.assertEqual(match.game.RPST(), game.RPST())

        self.assertEqual(match.players[0].match_attributes["length"], turns)
        self.assertEqual(match._cache, {})

    @given(prob_end=floats(min_value=0, max_value=1), game=games())
    def test_init_with_prob_end(self, prob_end, game):
        p1, p2 = axl.Cooperator(), axl.Cooperator()
        match = axl.Match((p1, p2), prob_end=prob_end, game=game)
        self.assertEqual(match.result, [])
        self.assertEqual(match.players, [p1, p2])
        self.assertEqual(match.turns, float("inf"))
        self.assertEqual(match.prob_end, prob_end)
        self.assertEqual(match.noise, 0)
        self.assertEqual(match.game.RPST(), game.RPST())

        self.assertEqual(
            match.players[0].match_attributes["length"], float("inf")
        )
        self.assertEqual(match._cache, {})

    @given(
        prob_end=floats(min_value=0, max_value=1),
        turns=integers(min_value=1, max_value=200),
        game=games(),
    )
    def test_init_with_prob_end_and_turns(self, turns, prob_end, game):
        p1, p2 = axl.Cooperator(), axl.Cooperator()
        match = axl.Match((p1, p2), turns=turns, prob_end=prob_end, game=game)
        self.assertEqual(match.result, [])
        self.assertEqual(match.players, [p1, p2])
        self.assertEqual(match.turns, turns)
        self.assertEqual(match.prob_end, prob_end)
        self.assertEqual(match.noise, 0)
        self.assertEqual(match.game.RPST(), game.RPST())

        self.assertEqual(
            match.players[0].match_attributes["length"], float("inf")
        )
        self.assertEqual(match._cache, {})

    def test_default_init(self):
        p1, p2 = axl.Cooperator(), axl.Cooperator()
        match = axl.Match((p1, p2))
        self.assertEqual(match.result, [])
        self.assertEqual(match.players, [p1, p2])
        self.assertEqual(match.turns, axl.DEFAULT_TURNS)
        self.assertEqual(match.prob_end, 0)
        self.assertEqual(match.noise, 0)
        self.assertEqual(match.game.RPST(), (3, 1, 0, 5))

        self.assertEqual(
            match.players[0].match_attributes["length"], axl.DEFAULT_TURNS
        )
        self.assertEqual(match._cache, {})

    def test_example_prob_end(self):
        """
        Test that matches have diff length and also that cache has recorded the
        outcomes
        """
        p1, p2 = axl.Cooperator(), axl.Cooperator()
        match = axl.Match((p1, p2), prob_end=0.5)
        expected_lengths = [3, 1, 5]
        for seed, expected_length in zip(range(3), expected_lengths):
            axl.seed(seed)
            self.assertEqual(
                match.players[0].match_attributes["length"], float("inf")
            )
            self.assertEqual(len(match.play()), expected_length)
            self.assertEqual(match.noise, 0)
            self.assertEqual(match.game.RPST(), (3, 1, 0, 5))
        self.assertEqual(len(match._cache), 1)
        self.assertEqual(match._cache[(p1, p2)], [(C, C)] * 5)

    @given(turns=integers(min_value=1, max_value=200), game=games())
    @example(turns=5, game=axl.DefaultGame)
    def test_non_default_attributes(self, turns, game):
        p1, p2 = axl.Cooperator(), axl.Cooperator()
        match_attributes = {"length": 500, "game": game, "noise": 0.5}
        match = axl.Match(
            (p1, p2), turns, game=game, match_attributes=match_attributes
        )
        self.assertEqual(match.players[0].match_attributes["length"], 500)
        self.assertEqual(match.players[0].match_attributes["noise"], 0.5)

    @given(turns=integers(min_value=1, max_value=200))
    @example(turns=5)
    def test_len(self, turns):
        p1, p2 = axl.Cooperator(), axl.Cooperator()
        match = axl.Match((p1, p2), turns)
        self.assertEqual(len(match), turns)

    def test_len_error(self):
        """
        Length is not defined if it is infinite.
        """
        p1, p2 = axl.Cooperator(), axl.Cooperator()
        match = axl.Match((p1, p2), prob_end=0.5)
        with self.assertRaises(TypeError):
            len(match)

    @given(p=floats(min_value=0, max_value=1))
    def test_stochastic(self, p):

        assume(0 < p < 1)

        p1, p2 = axl.Cooperator(), axl.Cooperator()
        match = axl.Match((p1, p2), 5)
        self.assertFalse(match._stochastic)

        match = axl.Match((p1, p2), 5, noise=p)
        self.assertTrue(match._stochastic)

        p1 = axl.Random()
        match = axl.Match((p1, p2), 5)
        self.assertTrue(match._stochastic)

    @given(p=floats(min_value=0, max_value=1))
    def test_cache_update_required(self, p):

        assume(0 < p < 1)

        p1, p2 = axl.Cooperator(), axl.Cooperator()
        match = axl.Match((p1, p2), 5, noise=p)
        self.assertFalse(match._cache_update_required)

        cache = DeterministicCache()
        cache.mutable = False
        match = axl.Match((p1, p2), 5, deterministic_cache=cache)
        self.assertFalse(match._cache_update_required)

        match = axl.Match((p1, p2), 5)
        self.assertTrue(match._cache_update_required)

        p1 = axl.Random()
        match = axl.Match((p1, p2), 5)
        self.assertFalse(match._cache_update_required)

    def test_play(self):
        cache = DeterministicCache()
        players = (axl.Cooperator(), axl.Defector())
        match = axl.Match(players, 3, deterministic_cache=cache)
        expected_result = [(C, D), (C, D), (C, D)]
        self.assertEqual(match.play(), expected_result)
        self.assertEqual(
            cache[(axl.Cooperator(), axl.Defector())], expected_result
        )

        # a deliberately incorrect result so we can tell it came from the cache
        expected_result = [(C, C), (D, D), (D, C), (C, C), (C, D)]
        cache[(axl.Cooperator(), axl.Defector())] = expected_result
        match = axl.Match(players, 3, deterministic_cache=cache)
        self.assertEqual(match.play(), expected_result[:3])

    def test_cache_grows(self):
        """
        We want to make sure that if we try to use the cache for more turns than
        what is stored, then it will instead regenerate the result and overwrite
        the cache.
        """
        cache = DeterministicCache()
        players = (axl.Cooperator(), axl.Defector())
        match = axl.Match(players, 3, deterministic_cache=cache)
        expected_result_5_turn = [(C, D), (C, D), (C, D), (C, D), (C, D)]
        expected_result_3_turn = [(C, D), (C, D), (C, D)]
        self.assertEqual(match.play(), expected_result_3_turn)
        match.turns = 5
        self.assertEqual(match.play(), expected_result_5_turn)
        # The cache should now hold the 5-turn result..
        self.assertEqual(
            cache[(axl.Cooperator(), axl.Defector())], expected_result_5_turn
        )

    def test_cache_doesnt_shrink(self):
        """
        We want to make sure that when we access the cache looking for fewer
        turns than what is stored, then it will not overwrite the cache with the
        shorter result.
        """
        cache = DeterministicCache()
        players = (axl.Cooperator(), axl.Defector())
        match = axl.Match(players, 5, deterministic_cache=cache)
        expected_result_5_turn = [(C, D), (C, D), (C, D), (C, D), (C, D)]
        expected_result_3_turn = [(C, D), (C, D), (C, D)]
        self.assertEqual(match.play(), expected_result_5_turn)
        match.turns = 3
        self.assertEqual(match.play(), expected_result_3_turn)
        # The cache should still hold the 5.
        self.assertEqual(
            cache[(axl.Cooperator(), axl.Defector())], expected_result_5_turn
        )

    def test_scores(self):
        player1 = axl.TitForTat()
        player2 = axl.Defector()
        match = axl.Match((player1, player2), 3)
        self.assertEqual(match.scores(), [])
        match.play()
        self.assertEqual(match.scores(), [(0, 5), (1, 1), (1, 1)])

    def test_final_score(self):
        player1 = axl.TitForTat()
        player2 = axl.Defector()

        match = axl.Match((player1, player2), 3)
        self.assertEqual(match.final_score(), None)
        match.play()
        self.assertEqual(match.final_score(), (2, 7))

        match = axl.Match((player2, player1), 3)
        self.assertEqual(match.final_score(), None)
        match.play()
        self.assertEqual(match.final_score(), (7, 2))

    def test_final_score_per_turn(self):
        turns = 3
        player1 = axl.TitForTat()
        player2 = axl.Defector()

        match = axl.Match((player1, player2), turns)
        self.assertEqual(match.final_score_per_turn(), None)
        match.play()
        self.assertEqual(match.final_score_per_turn(), (2 / turns, 7 / turns))

        match = axl.Match((player2, player1), turns)
        self.assertEqual(match.final_score_per_turn(), None)
        match.play()
        self.assertEqual(match.final_score_per_turn(), (7 / turns, 2 / turns))

    def test_winner(self):
        player1 = axl.TitForTat()
        player2 = axl.Defector()

        match = axl.Match((player1, player2), 3)
        self.assertEqual(match.winner(), None)
        match.play()
        self.assertEqual(match.winner(), player2)

        match = axl.Match((player2, player1), 3)
        self.assertEqual(match.winner(), None)
        match.play()
        self.assertEqual(match.winner(), player2)

        player1 = axl.Defector()
        match = axl.Match((player1, player2), 3)
        self.assertEqual(match.winner(), None)
        match.play()
        self.assertEqual(match.winner(), False)

    def test_cooperation(self):
        turns = 3
        player1 = axl.Cooperator()
        player2 = axl.Alternator()

        match = axl.Match((player1, player2), turns)
        self.assertEqual(match.cooperation(), None)
        match.play()
        self.assertEqual(match.cooperation(), (3, 2))

        player1 = axl.Alternator()
        player2 = axl.Defector()

        match = axl.Match((player1, player2), turns)
        self.assertEqual(match.cooperation(), None)
        match.play()
        self.assertEqual(match.cooperation(), (2, 0))

    def test_normalised_cooperation(self):
        turns = 3
        player1 = axl.Cooperator()
        player2 = axl.Alternator()

        match = axl.Match((player1, player2), turns)
        self.assertEqual(match.normalised_cooperation(), None)
        match.play()
        self.assertEqual(match.normalised_cooperation(), (3 / turns, 2 / turns))

        player1 = axl.Alternator()
        player2 = axl.Defector()

        match = axl.Match((player1, player2), turns)
        self.assertEqual(match.normalised_cooperation(), None)
        match.play()
        self.assertEqual(match.normalised_cooperation(), (2 / turns, 0 / turns))

    def test_state_distribution(self):
        turns = 3
        player1 = axl.Cooperator()
        player2 = axl.Alternator()

        match = axl.Match((player1, player2), turns)
        self.assertEqual(match.state_distribution(), None)

        match.play()
        expected = Counter({(C, C): 2, (C, D): 1})
        self.assertEqual(match.state_distribution(), expected)

        player1 = axl.Alternator()
        player2 = axl.Defector()

        match = axl.Match((player1, player2), turns)
        self.assertEqual(match.state_distribution(), None)

        match.play()
        expected = Counter({(C, D): 2, (D, D): 1})
        self.assertEqual(match.state_distribution(), expected)

    def test_normalised_state_distribution(self):
        turns = 3
        player1 = axl.Cooperator()
        player2 = axl.Alternator()

        match = axl.Match((player1, player2), turns)
        self.assertEqual(match.normalised_state_distribution(), None)

        match.play()
        expected = Counter({(C, C): 2 / turns, (C, D): 1 / turns})
        self.assertEqual(match.normalised_state_distribution(), expected)

        player1 = axl.Alternator()
        player2 = axl.Defector()

        match = axl.Match((player1, player2), turns)
        self.assertEqual(match.normalised_state_distribution(), None)

        match.play()
        expected = Counter({(C, D): 2 / turns, (D, D): 1 / turns})
        self.assertEqual(match.normalised_state_distribution(), expected)

    def test_sparklines(self):
        players = (axl.Cooperator(), axl.Alternator())
        match = axl.Match(players, 4)
        match.play()
        expected_sparklines = "████\n█ █ "
        self.assertEqual(match.sparklines(), expected_sparklines)
        expected_sparklines = "XXXX\nXYXY"
        self.assertEqual(match.sparklines("X", "Y"), expected_sparklines)

    def test_result_setter(self):
        players = (axl.Cooperator(), axl.Alternator())
        match = axl.Match(players)

        expected_result = [(C, C), (C, D), (D, C)]
        match.result = expected_result
        self.assertListEqual(match.result, expected_result)

    def test_noise_setter(self):
        players = (axl.Cooperator(), axl.Alternator())
        match = axl.Match(players)

        expected_noise = 0.123
        match.noise = expected_noise
        self.assertAlmostEqual(match.noise, expected_noise)

    def test_game_setter(self):
        players = (axl.Cooperator(), axl.Alternator())
        match = axl.Match(players)

        expected_game = axl.Game(1, 2, 3, 4)
        match.game = expected_game
        self.assertEqual(match.game, expected_game)

    def test_cache_setter(self):
        players = (axl.Cooperator(), axl.Alternator())
        match = axl.Match(players)

        expected_cache = axl.DeterministicCache()
        expected_cache.mutable = False  # Non-default value
        match._cache = expected_cache
        self.assertFalse(match._cache.mutable)

    def test_prob_end_setter(self):
        players = (axl.Cooperator(), axl.Alternator())
        match = axl.Match(players)

        expected_prob_end = 0.123
        match.prob_end = expected_prob_end
        self.assertAlmostEqual(match.prob_end, expected_prob_end)

    def test_turns_setter(self):
        players = (axl.Cooperator(), axl.Alternator())
        match = axl.Match(players)

        expected_turns = 123
        match.turns = expected_turns
        self.assertEqual(match.turns, expected_turns)

    def test_reset_setter(self):
        players = (axl.Cooperator(), axl.Alternator())
        match = axl.Match(players)

        expected_reset = False  # Non-default value
        match.reset = expected_reset
        self.assertFalse(match.reset)


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
            tournament.players[0].match_attributes["game"], axl.IpdGame
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
        file, writer = self.test_tournament._tournament._get_file_objects()
        self.assertIsNone(file)
        self.assertIsNone(writer)

    def test_get_file_object_with_filename(self):
        self.test_tournament.filename = self.filename
        (
            file_object,
            writer,
        ) = self.test_tournament._tournament._get_file_objects()
        self.assertIsInstance(file_object, io.TextIOWrapper)
        self.assertEqual(writer.__class__.__name__, "writer")
        file_object.close()

    def test_get_progress_bar(self):
        self.test_tournament.use_progress_bar = False
        pbar = self.test_tournament._tournament._get_progress_bar()
        self.assertIsNone(pbar)

        self.test_tournament.use_progress_bar = True
        pbar = self.test_tournament._tournament._get_progress_bar()
        self.assertIsInstance(pbar, tqdm)
        self.assertEqual(pbar.desc, "Playing matches")
        self.assertEqual(pbar.n, 0)
        self.assertEqual(pbar.total, self.test_tournament.match_generator.size)

        new_edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
        new_tournament = axl.Tournament(players=self.players, edges=new_edges)
        new_tournament.use_progress_bar = True
        pbar = new_tournament._tournament._get_progress_bar()
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
    @settings(max_examples=50)
    @example(
        tournament=axl.Tournament(
            players=[s() for s in test_strategies],
            turns=test_turns,
            repetitions=test_repetitions,
        )
    )
    # These two examples are to make sure #465 is fixed.
    # As explained there: https://github.com/Axelrod-Python/Axelrod/issues/465,
    # these two examples were identified by hypothesis.
    @example(
        tournament=axl.Tournament(
            players=[axl.BackStabber(), axl.MindReader()],
            turns=2,
            repetitions=1,
        )
    )
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
        tournament._tournament._write_interactions_to_file = MagicMock(
            name="_write_interactions_to_file"
        )
        self.assertTrue(tournament._tournament._run_serial())

        # Get the calls made to write_interactions
        calls = (
            tournament._tournament._write_interactions_to_file.call_args_list
        )
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
        tournament._tournament._write_interactions_to_file = PickleableMock(
            name="_write_interactions_to_file"
        )

        # For test coverage purposes. This confirms PickleableMock can be
        # pickled exactly once. Windows multi-processing must pickle this Mock
        # exactly once during testing.
        pickled = pickle.loads(pickle.dumps(tournament))
        self.assertIsInstance(
            pickled._tournament._write_interactions_to_file, MagicMock
        )
        self.assertRaises(pickle.PicklingError, pickle.dumps, pickled)

        self.assertTrue(tournament._tournament._run_parallel())

        # Get the calls made to write_interactions
        calls = (
            tournament._tournament._write_interactions_to_file.call_args_list
        )
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
        self.assertEqual(
            tournament._tournament._n_workers(processes=1), max_processes
        )

        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=axl.DEFAULT_TURNS,
            repetitions=self.test_repetitions,
        )
        self.assertEqual(
            tournament._tournament._n_workers(processes=max_processes + 2),
            max_processes,
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
        self.assertEqual(tournament._tournament._n_workers(processes=2), 2)

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
        tournament._tournament._start_workers(workers, work_queue, done_queue)

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
        tournament._tournament._worker(work_queue, done_queue)
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

        tournament._tournament._calculate_results = MagicMock(
            name="_calculate_results"
        )
        # Mocking this as it is called by play
        self.assertIsNone(
            tournament.play(
                filename=self.filename, progress_bar=False, build_results=False
            )
        )

        # Get the calls made to write_interactions
        calls = tournament._tournament._calculate_results.call_args_list
        self.assertEqual(len(calls), 0)

    @given(turns=integers(min_value=1, max_value=200))
    @settings(max_examples=5)
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
                    yield (index_pair, match_params, self.test_repetitions)

        chunk_generator = make_chunk_generator()
        interactions = {}
        for chunk in chunk_generator:
            result = tournament._tournament._play_matches(chunk)
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

    def test_match_cache_is_used(self):
        """
        Create two Random players that are classified as deterministic.
        As they are deterministic the cache will be used.
        """
        FakeRandom = axl.Random
        FakeRandom.classifier["stochastic"] = False
        p1 = FakeRandom()
        p2 = FakeRandom()
        tournament = axl.Tournament((p1, p2), turns=5, repetitions=2)
        results = tournament.play(progress_bar=False)
        for player_scores in results.scores:
            self.assertEqual(player_scores[0], player_scores[1])

    def test_write_interactions(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=2,
            repetitions=2,
        )
        tournament._tournament._write_interactions_to_file = MagicMock(
            name="_write_interactions_to_file"
        )
        # Mocking this as it is called by play
        self.assertIsNone(
            tournament.play(
                filename=self.filename, progress_bar=False, build_results=False
            )
        )

        # Get the calls made to write_interactions
        calls = (
            tournament._tournament._write_interactions_to_file.call_args_list
        )
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

    def test_players_setter(self):
        expected_players = [axl.Cooperator(), axl.Defector()]
        self.test_tournament.players = expected_players
        self.assertListEqual(self.test_tournament.players, expected_players)

    def test_game(self):
        expected_game = axl.Game(1, 2, 3, 4)
        self.test_tournament.players = expected_game
        self.assertEqual(self.test_tournament.players, expected_game)

    def test_turns_setter(self):
        expected_turns = 123
        self.test_tournament.turns = expected_turns
        self.assertEqual(self.test_tournament.turns, expected_turns)

    def test_repetitions_setter(self):
        expected_repetitions = 123
        self.test_tournament.repetitions = expected_repetitions
        self.assertEqual(self.test_tournament.repetitions, expected_repetitions)

    def test_name_setter(self):
        expected_name = "name_to_set"
        self.test_tournament.name = expected_name
        self.assertEqual(self.test_tournament.name, expected_name)

    def test_noise_setter(self):
        expected_noise = 0.123
        self.test_tournament.noise = expected_noise
        self.assertAlmostEqual(self.test_tournament.noise, expected_noise)

    def test_match_generator_setter(self):
        expected_match_generator_turns = 123
        self.test_tournament.match_generator.turns = (
            expected_match_generator_turns
        )
        self.assertEqual(
            self.test_tournament.match_generator.turns,
            expected_match_generator_turns,
        )

    def test_num_interactions_setter(self):
        expected_num_interactions = 123
        self.test_tournament.num_interactions = expected_num_interactions
        self.assertEqual(
            self.test_tournament.num_interactions, expected_num_interactions
        )

    def test_use_progress_bar_setter(self):
        expected_use_progress_bar = False
        self.test_tournament.use_progress_bar = expected_use_progress_bar
        self.assertFalse(self.test_tournament.use_progress_bar)

    def test_filename_setter(self):
        expected_filename = "fn.txt"
        self.test_tournament.filename = expected_filename
        self.assertEqual(self.test_tournament.filename, expected_filename)


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
        )
    )
    @settings(max_examples=5)
    @example(
        tournament=axl.Tournament(
            players=[s() for s in test_strategies],
            prob_end=0.2,
            repetitions=test_repetitions,
        )
    )
    # These two examples are to make sure #465 is fixed.
    # As explained there: https://github.com/Axelrod-Python/Axelrod/issues/465,
    # these two examples were identified by hypothesis.
    @example(
        tournament=axl.Tournament(
            players=[axl.BackStabber(), axl.MindReader()],
            prob_end=0.2,
            repetitions=1,
        )
    )
    @example(
        tournament=axl.Tournament(
            players=[axl.ThueMorse(), axl.MindReader()],
            prob_end=0.2,
            repetitions=1,
        )
    )
    def test_property_serial_play(self, tournament):
        """Test serial play using hypothesis"""
        # Test that we get an instance of ResultSet
        results = tournament.play(progress_bar=False)
        self.assertIsInstance(results, axl.ResultSet)
        self.assertEqual(results.num_players, len(tournament.players))
        self.assertEqual(results.players, [str(p) for p in tournament.players])

    def test_prob_end_setter(self):
        # create a round robin tournament
        players = [axl.Cooperator(), axl.Defector()]
        tournament = axl.Tournament(players)

        expected_prob_end = 0.123
        tournament.prob_end = expected_prob_end
        self.assertAlmostEqual(tournament.prob_end, expected_prob_end)


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
    @settings(max_examples=5)
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
            players, repetitions=repetitions, turns=turns, noise=noise
        )
        # create a complete spatial tournament
        spatial_tournament = axl.Tournament(
            players,
            repetitions=repetitions,
            turns=turns,
            noise=noise,
            edges=edges,
        )

        axl.seed(seed)
        results = tournament.play(progress_bar=False)
        axl.seed(seed)
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

    def test_edges_setter(self):
        # create a round robin tournament
        players = [axl.Cooperator(), axl.Defector()]
        tournament = axl.Tournament(players)

        expected_edges = [(1, 2), (3, 4)]
        tournament.edges = expected_edges
        self.assertListEqual(tournament.edges, expected_edges)


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
    @settings(max_examples=5)
    def test_complete_tournament(self, strategies, prob_end, seed, reps):
        """
        A test to check that a spatial tournament on the complete graph
        gives the same results as the round robin.
        """
        players = [s() for s in strategies]

        # create a prob end round robin tournament
        tournament = axl.Tournament(
            players, prob_end=prob_end, repetitions=reps
        )
        axl.seed(seed)
        results = tournament.play(progress_bar=False)

        # create a complete spatial tournament
        # edges
        edges = [
            (i, j) for i in range(len(players)) for j in range(i, len(players))
        ]

        spatial_tournament = axl.Tournament(
            players, prob_end=prob_end, repetitions=reps, edges=edges
        )
        axl.seed(seed)
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
    @settings(max_examples=5)
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
        )
        axl.seed(seed)
        prob_end_results = prob_end_tour.play(progress_bar=False)
        axl.seed(seed)
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


class TestAdapterTitForTat(axl.Player):
    name = "Tit For Tat"
    classifier = _test_classifier

    def strategy(self, opponent) -> axl.Action:
        """This is the actual strategy"""
        # First move
        if not self.history:
            return C
        # React to the opponent's last move
        if opponent.history[-1] == D:
            return D
        return C


def test_memory(player, opponent, memory_length, seed=0, turns=10):
    """
    Checks if a player reacts to the plays of an opponent in the same way if
    only the given amount of memory is used.
    """
    # Play the match normally.
    axl.seed(seed)
    match = axl.IpdMatch((player, opponent), turns=turns)
    plays = [p[0] for p in match.play()]

    # Play with limited history.
    player.reset()
    opponent.reset()
    player._history = axl.LimitedHistory(memory_length)
    opponent._history = axl.LimitedHistory(memory_length)
    axl.seed(seed)
    match = axl.IpdMatch((player, opponent), turns=turns, reset=False)
    limited_plays = [p[0] for p in match.play()]

    return plays == limited_plays


class TestPlayer(unittest.TestCase):
    """Test Player on TestAdapterTitForTat."""

    player = TestAdapterTitForTat
    name = "TestAdapterTitForTat"
    expected_class_classifier = _test_classifier

    def test_initialisation(self):
        """Test that the player initiates correctly."""
        if self.__class__ != TestPlayer:
            player = self.player()
            self.assertEqual(len(player.history), 0)
            self.assertEqual(
                player.match_attributes,
                {"length": -1, "game": axl.DefaultGame, "noise": 0},
            )
            self.assertEqual(player.cooperations, 0)
            self.assertEqual(player.defections, 0)
            # self.classifier_test(self.expected_class_classifier)

    def test_repr(self):
        """Test that the representation is correct."""
        if self.__class__ != TestPlayer:
            self.assertEqual(str(self.player()), self.name)

    def test_match_attributes(self):
        player = self.player()
        # Default
        player.set_match_attributes()
        t_attrs = player.match_attributes
        self.assertEqual(t_attrs["length"], -1)
        self.assertEqual(t_attrs["noise"], 0)
        self.assertEqual(t_attrs["game"].RPST(), (3, 1, 0, 5))

        # Common
        player.set_match_attributes(length=200)
        t_attrs = player.match_attributes
        self.assertEqual(t_attrs["length"], 200)
        self.assertEqual(t_attrs["noise"], 0)
        self.assertEqual(t_attrs["game"].RPST(), (3, 1, 0, 5))

        # Noisy
        player.set_match_attributes(length=200, noise=0.5)
        t_attrs = player.match_attributes
        self.assertEqual(t_attrs["noise"], 0.5)

    def equality_of_players_test(self, p1, p2, seed, opponent):
        a1 = opponent()
        a2 = opponent()
        self.assertEqual(p1, p2)
        for player, op in [(p1, a1), (p2, a2)]:
            axl.seed(seed)
            for _ in range(10):
                simultaneous_play(player, op)
        self.assertEqual(p1, p2)
        p1 = pickle.loads(pickle.dumps(p1))
        p2 = pickle.loads(pickle.dumps(p2))
        self.assertEqual(p1, p2)

    @given(
        opponent=sampled_from(short_run_time_short_mem),
        seed=integers(min_value=1, max_value=200),
    )
    @settings(max_examples=1)
    def test_equality_of_clone(self, seed, opponent):
        p1 = self.player()
        p2 = p1.clone()
        self.equality_of_players_test(p1, p2, seed, opponent)

    @given(
        opponent=sampled_from(axl.short_run_time_strategies),
        seed=integers(min_value=1, max_value=200),
    )
    @settings(max_examples=1)
    def test_equality_of_pickle_clone(self, seed, opponent):
        p1 = self.player()
        p2 = pickle.loads(pickle.dumps(p1))
        self.equality_of_players_test(p1, p2, seed, opponent)

    def test_reset_history_and_attributes(self):
        """Make sure resetting works correctly."""
        for opponent in [
            axl.Defector(),
            axl.Random(),
            axl.Alternator(),
            axl.Cooperator(),
        ]:

            player = self.player()
            clone = player.clone()
            for seed in range(10):
                axl.seed(seed)
                player.play(opponent)

            player.reset()
            self.assertEqual(player, clone)

    def test_reset_clone(self):
        """Make sure history resetting with cloning works correctly, regardless
        if self.test_reset() is overwritten."""
        player = self.player()
        clone = player.clone()
        self.assertEqual(player, clone)

    @given(seed=integers(min_value=1, max_value=20000000))
    @settings(max_examples=1)
    def test_clone(self, seed):
        # Test that the cloned player produces identical play
        player1 = self.player()
        if player1.name in ["Darwin", "Human"]:
            # Known exceptions
            return
        player2 = player1.clone()
        self.assertEqual(len(player2.history), 0)
        self.assertEqual(player2.cooperations, 0)
        self.assertEqual(player2.defections, 0)
        self.assertEqual(player2.state_distribution, {})
        self.assertEqual(player2.classifier, player1.classifier)
        self.assertEqual(player2.match_attributes, player1.match_attributes)

        turns = 50
        r = random.random()
        for op in [
            axl.Cooperator(),
            axl.Defector(),
            axl.TitForTat(),
            axl.Random(p=r),
        ]:
            player1.reset()
            player2.reset()
            for p in [player1, player2]:
                axl.seed(seed)
                m = axl.IpdMatch((p, op), turns=turns)
                m.play()
            self.assertEqual(len(player1.history), turns)
            self.assertEqual(player1.history, player2.history)

    @given(
        strategies=strategy_lists(
            max_size=5, strategies=short_run_time_short_mem
        ),
        seed=integers(min_value=1, max_value=200),
        turns=integers(min_value=1, max_value=200),
    )
    @settings(max_examples=1)
    def test_memory_depth_upper_bound(self, strategies, seed, turns):
        """
        Test that the memory depth is indeed an upper bound.
        """

        def get_memory_depth_or_zero(player):
            # Some of the test strategies have no entry in the classifiers
            # table, so there isn't logic to load default value of zero.
            memory = axl.Classifiers["memory_depth"](player)
            return memory if memory else 0

        player = self.player()
        memory = get_memory_depth_or_zero(player)
        if memory < float("inf"):
            for strategy in strategies:
                player.reset()
                opponent = strategy()
                max_memory = max(memory, get_memory_depth_or_zero(opponent))
                self.assertTrue(
                    test_memory(
                        player=player,
                        opponent=opponent,
                        seed=seed,
                        turns=turns,
                        memory_length=max_memory,
                    ),
                    msg="{} failed for seed={} and opponent={}".format(
                        player.name, seed, opponent
                    ),
                )
