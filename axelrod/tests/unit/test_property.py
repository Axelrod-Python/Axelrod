from __future__ import absolute_import
import unittest
import axelrod
from axelrod.tests.property import (strategy_lists,
                                    matches, tournaments,
                                    prob_end_tournaments, games)

from hypothesis import given
from hypothesis.strategies import random_module

stochastic_strategies = [s for s in axelrod.strategies if
                         s().classifier['stochastic']]


class TestStrategyList(unittest.TestCase):

    def test_call(self):
        strategies = strategy_lists().example()
        self.assertIsInstance(strategies, list)
        for p in strategies:
            self.assertIsInstance(p(), axelrod.Player)

    @given(strategies=strategy_lists(min_size=1, max_size=50),
           rm=random_module())
    def test_decorator(self, strategies, rm):
        self.assertIsInstance(strategies, list)
        self.assertGreaterEqual(len(strategies), 1)
        self.assertLessEqual(len(strategies), 50)
        for strategy in strategies:
            self.assertIsInstance(strategy(), axelrod.Player)

    @given(strategies=strategy_lists(strategies=axelrod.basic_strategies),
           rm=random_module())
    def test_decorator_with_given_strategies(self, strategies, rm):
        self.assertIsInstance(strategies, list)
        basic_player_names = [str(s()) for s in axelrod.basic_strategies]
        for strategy in strategies:
            player = strategy()
            self.assertIsInstance(player, axelrod.Player)
            self.assertIn(str(player), basic_player_names)

    @given(strategies=strategy_lists(strategies=stochastic_strategies),
           rm=random_module())
    def test_decorator_with_stochastic_strategies(self, strategies, rm):
        self.assertIsInstance(strategies, list)
        stochastic_player_names = [str(s()) for s in stochastic_strategies]
        for strategy in strategies:
            player = strategy()
            self.assertIsInstance(player, axelrod.Player)
            self.assertIn(str(player), stochastic_player_names)


class TestMatch(unittest.TestCase):
    """
    Test that the composite method works
    """

    def test_call(self):
        match, seed = matches().example()
        self.assertTrue(str(seed).startswith('random.seed'))
        self.assertIsInstance(match, axelrod.Match)

    @given(match_and_seed=matches(min_turns=10, max_turns=50,
                                  min_noise=0, max_noise=1))
    def test_decorator(self, match_and_seed):
        match, seed = match_and_seed
        self.assertTrue(str(seed).startswith('random.seed'))

        self.assertIsInstance(match, axelrod.Match)
        self.assertGreaterEqual(len(match), 10)
        self.assertLessEqual(len(match), 50)
        self.assertGreaterEqual(match.noise, 0)
        self.assertLessEqual(match.noise, 1)

    @given(match_and_seed=matches(min_turns=10, max_turns=50,
                                  min_noise=0, max_noise=0))
    def test_decorator_with_no_noise(self, match_and_seed):
        match, seed = match_and_seed
        self.assertTrue(str(seed).startswith('random.seed'))

        self.assertIsInstance(match, axelrod.Match)
        self.assertGreaterEqual(len(match), 10)
        self.assertLessEqual(len(match), 50)
        self.assertEqual(match.noise, 0)


class TestTournament(unittest.TestCase):

    def test_call(self):
        tournament, seed = tournaments().example()
        self.assertTrue(str(seed).startswith('random.seed'))
        self.assertIsInstance(tournament, axelrod.Tournament)

    @given(tournament_and_seed=tournaments(min_turns=2, max_turns=50, min_noise=0,
                                           max_noise=1, min_repetitions=2,
                                           max_repetitions=50))
    def test_decorator(self, tournament_and_seed):
        tournament, seed = tournament_and_seed
        self.assertTrue(str(seed).startswith('random.seed'))

        self.assertIsInstance(tournament, axelrod.Tournament)
        self.assertLessEqual(tournament.turns, 50)
        self.assertGreaterEqual(tournament.turns, 2)
        self.assertLessEqual(tournament.noise, 1)
        self.assertGreaterEqual(tournament.noise, 0)
        self.assertLessEqual(tournament.repetitions, 50)
        self.assertGreaterEqual(tournament.repetitions, 2)

    @given(tournament_and_seed=tournaments(strategies=axelrod.basic_strategies))
    def test_decorator_with_given_strategies(self, tournament_and_seed):
        tournament, seed = tournament_and_seed
        self.assertTrue(str(seed).startswith('random.seed'))

        self.assertIsInstance(tournament, axelrod.Tournament)
        basic_player_names = [str(s()) for s in axelrod.basic_strategies]
        for p in tournament.players:
            self.assertIn(str(p), basic_player_names)

    @given(tournament_and_seed=tournaments(strategies=stochastic_strategies))
    def test_decorator_with_stochastic_strategies(self, tournament_and_seed):
        tournament, seed = tournament_and_seed
        self.assertTrue(str(seed).startswith('random.seed'))

        self.assertIsInstance(tournament, axelrod.Tournament)
        stochastic_player_names = [str(s()) for s in stochastic_strategies]
        for p in tournament.players:
            self.assertIn(str(p), stochastic_player_names)


class TestProbEndTournament(unittest.TestCase):

    def test_call(self):
        tournament, seed = prob_end_tournaments().example()
        self.assertTrue(str(seed).startswith('random.seed'))
        self.assertIsInstance(tournament, axelrod.Tournament)

    @given(tournament_and_seed=prob_end_tournaments(min_prob_end=0,
                                                    max_prob_end=1,
                                                    min_noise=0, max_noise=1,
                                                    min_repetitions=2,
                                                    max_repetitions=50))
    def test_decorator(self, tournament_and_seed):
        tournament, seed = tournament_and_seed
        self.assertTrue(str(seed).startswith('random.seed'))

        self.assertIsInstance(tournament, axelrod.ProbEndTournament)
        self.assertLessEqual(tournament.prob_end, 1)
        self.assertGreaterEqual(tournament.prob_end, 0)
        self.assertLessEqual(tournament.noise, 1)
        self.assertGreaterEqual(tournament.noise, 0)
        self.assertLessEqual(tournament.repetitions, 50)
        self.assertGreaterEqual(tournament.repetitions, 2)

    @given(tournament_and_seed=prob_end_tournaments(strategies=axelrod.basic_strategies))
    def test_decorator_with_given_strategies(self, tournament_and_seed):
        tournament, seed = tournament_and_seed
        self.assertTrue(str(seed).startswith('random.seed'))

        self.assertIsInstance(tournament, axelrod.ProbEndTournament)
        basic_player_names = [str(s()) for s in axelrod.basic_strategies]
        for p in tournament.players:
            self.assertIn(str(p), basic_player_names)

    @given(tournament_and_seed=prob_end_tournaments(strategies=stochastic_strategies))
    def test_decorator_with_stochastic_strategies(self, tournament_and_seed):
        tournament, seed = tournament_and_seed
        self.assertTrue(str(seed).startswith('random.seed'))

        self.assertIsInstance(tournament, axelrod.ProbEndTournament)
        stochastic_player_names = [str(s()) for s in stochastic_strategies]
        for p in tournament.players:
            self.assertIn(str(p), stochastic_player_names)

class TestGame(unittest.TestCase):

    def test_call(self):
        game = games().example()
        self.assertIsInstance(game, axelrod.Game)

    @given(game=games())
    def test_decorator(self, game):
        self.assertIsInstance(game, axelrod.Game)
        r, p, s, t = game.RPST()
        self.assertTrue((2 * r) > (t + s) and (t > r > p > s))

    @given(game=games(prisoners_dilemma=False))
    def test_decorator_unconstrained(self, game):
        self.assertIsInstance(game, axelrod.Game)
