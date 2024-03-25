import filecmp
import pathlib
import unittest

from hypothesis import given, settings

import axelrod as axl
from axelrod.load_data_ import axl_filename
from axelrod.strategy_transformers import FinalTransformer
from axelrod.tests.property import tournaments


class TestTournament(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = axl.Game()
        cls.players = [
            axl.Cooperator(),
            axl.TitForTat(),
            axl.Defector(),
            axl.Grudger(),
            axl.GoByMajority(),
        ]
        cls.player_names = [str(p) for p in cls.players]
        cls.test_name = "test"
        cls.test_repetitions = 3

        cls.expected_outcome = [
            ("Cooperator", [45, 45, 45]),
            ("Defector", [52, 52, 52]),
            ("Grudger", [49, 49, 49]),
            ("Soft Go By Majority", [49, 49, 49]),
            ("Tit For Tat", [49, 49, 49]),
        ]
        cls.expected_outcome.sort()

    @given(
        tournaments(
            strategies=axl.short_run_time_strategies,
            min_size=10,
            max_size=30,
            min_turns=2,
            max_turns=210,
            min_repetitions=1,
            max_repetitions=4,
        )
    )
    @settings(max_examples=1)
    def test_big_tournaments(self, tournament):
        """A test to check that tournament runs with a sample of non-cheating
        strategies."""
        path = pathlib.Path("test_outputs/test_tournament.csv")
        filename = axl_filename(path)
        self.assertIsNone(
            tournament.play(
                progress_bar=False, filename=filename, build_results=False
            )
        )

    def test_serial_play(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=5,
            repetitions=self.test_repetitions,
        )
        scores = tournament.play(progress_bar=False).scores
        actual_outcome = sorted(zip(self.player_names, scores))
        self.assertEqual(actual_outcome, self.expected_outcome)

    def test_parallel_play(self):
        tournament = axl.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=5,
            repetitions=self.test_repetitions,
        )
        scores = tournament.play(processes=2, progress_bar=False).scores
        actual_outcome = sorted(zip(self.player_names, scores))
        self.assertEqual(actual_outcome, self.expected_outcome)

    def test_repeat_tournament_deterministic(self):
        """A test to check that tournament gives same results."""
        deterministic_players = [
            s()
            for s in axl.short_run_time_strategies
            if not axl.Classifiers["stochastic"](s())
        ]
        files = []
        for _ in range(2):
            tournament = axl.Tournament(
                name="test",
                players=deterministic_players,
                game=self.game,
                turns=2,
                repetitions=2,
            )
            path = pathlib.Path(
                "test_outputs/stochastic_tournament_{}.csv".format(_)
            )
            files.append(axl_filename(path))
            tournament.play(
                progress_bar=False, filename=files[-1], build_results=False
            )
        self.assertTrue(filecmp.cmp(files[0], files[1]))

    def test_repeat_tournament_stochastic(self):
        """
        A test to check that tournament gives same results when setting seed.
        """
        files = []
        for _ in range(2):
            stochastic_players = [
                s()
                for s in axl.short_run_time_strategies
                if axl.Classifiers["stochastic"](s())
            ]
            tournament = axl.Tournament(
                name="test",
                players=stochastic_players,
                game=self.game,
                turns=2,
                repetitions=2,
                seed=17,
            )
            path = pathlib.Path(
                "test_outputs/stochastic_tournament_{}.csv".format(_)
            )
            files.append(axl_filename(path))
            tournament.play(
                progress_bar=False, filename=files[-1], build_results=False
            )
        self.assertTrue(filecmp.cmp(files[0], files[1]))


class TestNoisyTournament(unittest.TestCase):
    def test_noisy_tournament(self):
        # Defector should win for low noise
        players = [axl.Cooperator(), axl.Defector()]
        tournament = axl.Tournament(players, turns=5, repetitions=3, noise=0.0)
        results = tournament.play(progress_bar=False)
        self.assertEqual(results.ranked_names[0], "Defector")

        # If the noise is large enough, cooperator should win
        players = [axl.Cooperator(), axl.Defector()]
        tournament = axl.Tournament(players, turns=5, repetitions=3, noise=0.75)
        results = tournament.play(progress_bar=False)
        self.assertEqual(results.ranked_names[0], "Cooperator")


class TestProbEndTournament(unittest.TestCase):
    def test_players_do_not_know_match_length(self):
        """Create two players who should cooperate on last two turns if they
        don't know when those last two turns are.
        """
        p1 = FinalTransformer(["D", "D"])(axl.Cooperator)()
        p2 = FinalTransformer(["D", "D"])(axl.Cooperator)()
        players = [p1, p2]
        tournament = axl.Tournament(players, prob_end=0.5, repetitions=1)
        results = tournament.play(progress_bar=False)
        # Check that both plays always cooperated
        for rating in results.cooperating_rating:
            self.assertEqual(rating, 1)

    def test_matches_have_different_length(self):
        """
        A match between two players should have variable length across the
        repetitions
        """
        p1 = axl.Cooperator()
        p2 = axl.Cooperator()
        p3 = axl.Cooperator()
        players = [p1, p2, p3]
        tournament = axl.Tournament(
            players, prob_end=0.5, repetitions=2, seed=3
        )
        results = tournament.play(progress_bar=False)
        # Check that match length are different across the repetitions
        self.assertNotEqual(results.match_lengths[0], results.match_lengths[1])
