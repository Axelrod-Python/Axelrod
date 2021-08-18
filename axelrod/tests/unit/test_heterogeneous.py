import filecmp
import pathlib
import unittest

import axelrod as axl
from axelrod import MoranProcess
from axelrod.load_data_ import axl_filename
from axelrod.strategy_transformers import FinalTransformer
from axelrod.tests.property import tournaments
from hypothesis import given, settings

import unittest
from collections import Counter

C, D = axl.Action.C, axl.Action.D
random = axl.RandomGenerator()

masses = [1 * i for i in range(20)]

class MassBaseMatch(axl.Match):
    """Axelrod Match object with a modified final score function to enable mass to influence the final score as a multiplier"""
    def final_score_per_turn(self):
        base_scores = axl.Match.final_score_per_turn(self)
        return [player.mass * score for player, score in zip(self.players, base_scores)] 

def set_player_mass(players, masses):
    """Add mass attribute to player strategy classes to be accessable via self.mass"""
    for player, mass in zip(players, masses):
        setattr(player, "mass", mass)

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
        cls.masses = [100, -150, 0, 100, 500]
        cls.player_names = [str(p) for p in cls.players]
        cls.test_name = "test"
        cls.test_repetitions = 3
        set_player_mass(cls.players, cls.masses)

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
            match_class=MassBaseMatch,
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
            match_class=MassBaseMatch,
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
                match_class=MassBaseMatch,
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
                match_class=MassBaseMatch,
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
        tournament = axl.Tournament(players, turns=5, repetitions=3, noise=0.0, match_class=MassBaseMatch)
        results = tournament.play(progress_bar=False)
        self.assertEqual(results.ranked_names[0], "Defector")

        # If the noise is large enough, cooperator should win
        players = [axl.Cooperator(), axl.Defector()]
        tournament = axl.Tournament(players, turns=5, repetitions=3, noise=0.75, match_class=MassBaseMatch)
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
        tournament = axl.Tournament(players, prob_end=0.5, repetitions=1, match_class=MassBaseMatch)
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
            players, prob_end=0.5, repetitions=2, seed=3, match_class=MassBaseMatch
        )
        results = tournament.play(progress_bar=False)
        # Check that match length are different across the repetitions
        self.assertNotEqual(results.match_lengths[0], results.match_lengths[1])

#Moran process tests
class MassBasedMoranProcess(axl.MoranProcess):
    """Axelrod MoranProcess class """
    def __next__(self):
        set_player_mass(self.players, masses)
        super().__next__()
        return self

class TestMoranProcess(unittest.TestCase):
    def test_init(self):
        players = axl.Cooperator(), axl.Defector()
        masses = [10, 20]
        set_player_mass(players, masses)
        mp = MassBasedMoranProcess(players, match_class=MassBaseMatch)
        self.assertEqual(mp.turns, axl.DEFAULT_TURNS)
        self.assertIsNone(mp.prob_end)
        self.assertIsNone(mp.game)
        self.assertEqual(mp.noise, 0)
        self.assertEqual(mp.initial_players, players)
        self.assertEqual(mp.players, list(players))
        self.assertEqual(
            mp.populations, [Counter({"Cooperator": 1, "Defector": 1})]
        )
        self.assertIsNone(mp.winning_strategy_name)
        self.assertEqual(mp.mutation_rate, 0)
        self.assertEqual(mp.mode, "bd")
        self.assertEqual(mp.deterministic_cache, axl.DeterministicCache())
        self.assertEqual(
            mp.mutation_targets,
            {"Cooperator": [players[1]], "Defector": [players[0]]},
        )
        self.assertEqual(mp.interaction_graph._edges, [(0, 1), (1, 0)])
        self.assertEqual(
            mp.reproduction_graph._edges, [(0, 1), (1, 0), (0, 0), (1, 1)]
        )
        self.assertEqual(mp.fitness_transformation, None)
        self.assertEqual(mp.locations, [0, 1])
        self.assertEqual(mp.index, {0: 0, 1: 1})

        # Test non default graph cases
        players = axl.Cooperator(), axl.Defector(), axl.TitForTat()
        masses = [10, 20, 10]
        set_player_mass(players, masses)
        edges = [(0, 1), (2, 0), (1, 2)]
        graph = axl.graph.Graph(edges, directed=True)
        mp = MassBasedMoranProcess(players, match_class=MassBaseMatch, interaction_graph=graph)
        self.assertEqual(mp.interaction_graph._edges, [(0, 1), (2, 0), (1, 2)])
        self.assertEqual(
            sorted(mp.reproduction_graph._edges),
            sorted([(0, 1), (2, 0), (1, 2), (0, 0), (1, 1), (2, 2)]),
        )

        mp = MassBasedMoranProcess(
            players, interaction_graph=graph, reproduction_graph=graph
        )
        self.assertEqual(mp.interaction_graph._edges, [(0, 1), (2, 0), (1, 2)])
        self.assertEqual(mp.reproduction_graph._edges, [(0, 1), (2, 0), (1, 2)])

    def test_set_players(self):
        """Test that set players resets all players"""
        players = axl.Cooperator(), axl.Defector()
        masses = [10, 20]
        set_player_mass(players, masses)
        mp = MassBasedMoranProcess(players, match_class=MassBaseMatch)
        players[0].history.append(C, D)
        mp.set_players()
        self.assertEqual(players[0].cooperations, 0)

    def test_death_in_db(self):
        players = axl.Cooperator(), axl.Defector(), axl.TitForTat()
        masses = [10, 20, 10]
        set_player_mass(players, masses)
        mp = MoranProcess(players, match_class=MassBaseMatch, mutation_rate=0.5, mode="db", seed=1)
        self.assertEqual(mp.death(), 2)
        self.assertEqual(mp.dead, 2)
        mp = MoranProcess(players, match_class=MassBaseMatch, mutation_rate=0.5, mode="db", seed=2)
        self.assertEqual(mp.death(), 0)
        self.assertEqual(mp.dead, 0)
        mp = MoranProcess(players, match_class=MassBaseMatch, mutation_rate=0.5, mode="db", seed=9)
        self.assertEqual(mp.death(), 1)
        self.assertEqual(mp.dead, 1)

    def test_death_in_bd(self):
        players = axl.Cooperator(), axl.Defector(), axl.TitForTat()
        masses = [10, 20, 10]
        set_player_mass(players, masses)
        edges = [(0, 1), (2, 0), (1, 2)]
        graph = axl.graph.Graph(edges, directed=True)
        mp = MoranProcess(players, match_class=MassBaseMatch, mode="bd", interaction_graph=graph, seed=1)
        self.assertEqual(mp.death(0), 1)
        mp = MoranProcess(players, match_class=MassBaseMatch, mode="bd", interaction_graph=graph, seed=2)
        self.assertEqual(mp.death(0), 1)
        mp = MoranProcess(players, match_class=MassBaseMatch, mode="bd", interaction_graph=graph, seed=3)
        self.assertEqual(mp.death(0), 0)

    def test_birth_in_db(self):
        players = axl.Cooperator(), axl.Defector(), axl.TitForTat()
        masses = [10, 20, 10]
        set_player_mass(players, masses)
        mp = MoranProcess(players, match_class=MassBaseMatch, mode="db", seed=1)
        self.assertEqual(mp.death(), 2)
        self.assertEqual(mp.birth(0), 2)

    def test_birth_in_bd(self):
        players = axl.Cooperator(), axl.Defector(), axl.TitForTat()
        masses = [1, 1, 1]
        set_player_mass(players, masses)
        mp = MoranProcess(players, match_class=MassBaseMatch, mode="bd", seed=2)
        self.assertEqual(mp.birth(), 0)

    def test_fixation_check(self):
        players = axl.Cooperator(), axl.Cooperator()
        masses = [10, 20]
        set_player_mass(players, masses)
        mp = MassBasedMoranProcess(players, match_class=MassBaseMatch)
        self.assertTrue(mp.fixation_check())
        players = axl.Cooperator(), axl.Defector()
        mp = MassBasedMoranProcess(players, match_class=MassBaseMatch)
        self.assertFalse(mp.fixation_check())

    def test_next(self):
        players = axl.Cooperator(), axl.Defector()
        masses = [10, 20]
        set_player_mass(players, masses)
        mp = MassBasedMoranProcess(players, match_class=MassBaseMatch)
        self.assertIsInstance(next(mp), axl.MoranProcess)

    def test_matchup_indices(self):
        players = axl.Cooperator(), axl.Defector()
        masses = [10, 20]
        set_player_mass(players, masses)
        mp = MassBasedMoranProcess(players, match_class=MassBaseMatch)
        self.assertEqual(mp._matchup_indices(), {(0, 1)})

        players = axl.Cooperator(), axl.Defector(), axl.TitForTat()
        masses = [10, 20, 10]
        set_player_mass(players, masses)
        edges = [(0, 1), (2, 0), (1, 2)]
        graph = axl.graph.Graph(edges, directed=True)
        mp = MassBasedMoranProcess(players, match_class=MassBaseMatch, mode="bd", interaction_graph=graph)
        self.assertEqual(mp._matchup_indices(), {(0, 1), (1, 2), (2, 0)})

    def test_fps(self):
        players = axl.Cooperator(), axl.Defector()
        masses = [10, 20]
        set_player_mass(players, masses)
        mp = MoranProcess(players, match_class=MassBaseMatch, seed=1)
        self.assertEqual(mp.fitness_proportionate_selection([0, 0, 1]), 2)
        self.assertEqual(mp.fitness_proportionate_selection([1, 1, 1]), 2)
        self.assertEqual(mp.fitness_proportionate_selection([1, 1, 1]), 0)

    def test_exit_condition(self):
        p1, p2 = axl.Cooperator(), axl.Cooperator()
        masses = [10, 20]
        set_player_mass([p1, p2], masses)
        mp = MassBasedMoranProcess((p1, p2), match_class=MassBaseMatch)
        mp.play()
        self.assertEqual(len(mp), 1)