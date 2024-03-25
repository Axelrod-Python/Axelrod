import unittest

from hypothesis import given, settings

import axelrod as axl
from axelrod.tests.property import (
    games,
    matches,
    prob_end_spatial_tournaments,
    prob_end_tournaments,
    spatial_tournaments,
    strategy_lists,
    tournaments,
)

stochastic_strategies = [
    s for s in axl.strategies if axl.Classifiers["stochastic"](s())
]


class TestStrategyList(unittest.TestCase):
    def test_call(self):
        strategies = strategy_lists().example()
        self.assertIsInstance(strategies, list)
        for p in strategies:
            self.assertIsInstance(p(), axl.Player)

    @given(strategies=strategy_lists(min_size=1, max_size=50))
    @settings(max_examples=5)
    def test_decorator(self, strategies):
        self.assertIsInstance(strategies, list)
        self.assertGreaterEqual(len(strategies), 1)
        self.assertLessEqual(len(strategies), 50)
        for strategy in strategies:
            self.assertIsInstance(strategy(), axl.Player)

    @given(strategies=strategy_lists(strategies=axl.basic_strategies))
    @settings(max_examples=5)
    def test_decorator_with_given_strategies(self, strategies):
        self.assertIsInstance(strategies, list)
        basic_player_names = [str(s()) for s in axl.basic_strategies]
        for strategy in strategies:
            player = strategy()
            self.assertIsInstance(player, axl.Player)
            self.assertIn(str(player), basic_player_names)


class TestMatch(unittest.TestCase):
    """
    Test that the composite method works
    """

    def test_call(self):
        match = matches().example()
        self.assertIsInstance(match, axl.Match)

    @given(match=matches(min_turns=10, max_turns=50, min_noise=0, max_noise=1))
    @settings(max_examples=5)
    def test_decorator(self, match):
        self.assertIsInstance(match, axl.Match)
        self.assertGreaterEqual(len(match), 10)
        self.assertLessEqual(len(match), 50)
        self.assertGreaterEqual(match.noise, 0)
        self.assertLessEqual(match.noise, 1)

    @given(match=matches(min_turns=10, max_turns=50, min_noise=0, max_noise=0))
    @settings(max_examples=5)
    def test_decorator_with_no_noise(self, match):
        self.assertIsInstance(match, axl.Match)
        self.assertGreaterEqual(len(match), 10)
        self.assertLessEqual(len(match), 50)
        self.assertEqual(match.noise, 0)


class TestTournament(unittest.TestCase):
    def test_call(self):
        tournament = tournaments().example()
        self.assertIsInstance(tournament, axl.Tournament)

    @given(
        tournament=tournaments(
            min_turns=2,
            max_turns=50,
            min_noise=0,
            max_noise=1,
            min_repetitions=2,
            max_repetitions=50,
            max_size=3,
        )
    )
    @settings(max_examples=5)
    def test_decorator(self, tournament):
        self.assertIsInstance(tournament, axl.Tournament)
        self.assertLessEqual(tournament.turns, 50)
        self.assertGreaterEqual(tournament.turns, 2)
        self.assertLessEqual(tournament.noise, 1)
        self.assertGreaterEqual(tournament.noise, 0)
        self.assertLessEqual(tournament.repetitions, 50)
        self.assertGreaterEqual(tournament.repetitions, 2)

    @given(tournament=tournaments(strategies=axl.basic_strategies, max_size=3))
    @settings(max_examples=5)
    def test_decorator_with_given_strategies(self, tournament):
        self.assertIsInstance(tournament, axl.Tournament)
        basic_player_names = [str(s()) for s in axl.basic_strategies]
        for p in tournament.players:
            self.assertIn(str(p), basic_player_names)


class TestProbEndTournament(unittest.TestCase):
    def test_call(self):
        tournament = tournaments().example()
        self.assertIsInstance(tournament, axl.Tournament)

    @given(
        tournament=prob_end_tournaments(
            min_prob_end=0,
            max_prob_end=1,
            min_noise=0,
            max_noise=1,
            min_repetitions=2,
            max_repetitions=50,
            max_size=3,
        )
    )
    @settings(max_examples=5)
    def test_decorator(self, tournament):
        self.assertIsInstance(tournament, axl.Tournament)
        self.assertLessEqual(tournament.prob_end, 1)
        self.assertGreaterEqual(tournament.prob_end, 0)
        self.assertLessEqual(tournament.noise, 1)
        self.assertGreaterEqual(tournament.noise, 0)
        self.assertLessEqual(tournament.repetitions, 50)
        self.assertGreaterEqual(tournament.repetitions, 2)

    @given(
        tournament=prob_end_tournaments(
            strategies=axl.basic_strategies, max_size=3
        )
    )
    @settings(max_examples=5)
    def test_decorator_with_given_strategies(self, tournament):
        self.assertIsInstance(tournament, axl.Tournament)
        basic_player_names = [str(s()) for s in axl.basic_strategies]
        for p in tournament.players:
            self.assertIn(str(p), basic_player_names)


class TestSpatialTournament(unittest.TestCase):
    def test_call(self):
        tournament = spatial_tournaments().example()
        self.assertIsInstance(tournament, axl.Tournament)

    @given(
        tournament=spatial_tournaments(
            min_turns=2,
            max_turns=50,
            min_noise=0,
            max_noise=1,
            min_repetitions=2,
            max_repetitions=50,
            max_size=3,
        )
    )
    @settings(max_examples=5)
    def test_decorator(self, tournament):
        self.assertIsInstance(tournament, axl.Tournament)
        self.assertLessEqual(tournament.turns, 50)
        self.assertGreaterEqual(tournament.turns, 2)
        self.assertLessEqual(tournament.noise, 1)
        self.assertGreaterEqual(tournament.noise, 0)
        self.assertLessEqual(tournament.repetitions, 50)
        self.assertGreaterEqual(tournament.repetitions, 2)

    @given(
        tournament=spatial_tournaments(
            strategies=axl.basic_strategies, max_size=3
        )
    )
    @settings(max_examples=5)
    def test_decorator_with_given_strategies(self, tournament):
        self.assertIsInstance(tournament, axl.Tournament)
        basic_player_names = [str(s()) for s in axl.basic_strategies]
        for p in tournament.players:
            self.assertIn(str(p), basic_player_names)


class TestProbEndSpatialTournament(unittest.TestCase):
    def test_call(self):
        tournament = prob_end_spatial_tournaments().example()
        self.assertIsInstance(tournament, axl.Tournament)

    @given(
        tournament=prob_end_spatial_tournaments(
            min_prob_end=0,
            max_prob_end=1,
            min_noise=0,
            max_noise=1,
            min_repetitions=2,
            max_repetitions=50,
            max_size=3,
        )
    )
    @settings(max_examples=5)
    def test_decorator(self, tournament):
        self.assertIsInstance(tournament, axl.Tournament)
        self.assertLessEqual(tournament.prob_end, 1)
        self.assertGreaterEqual(tournament.prob_end, 0)
        self.assertLessEqual(tournament.noise, 1)
        self.assertGreaterEqual(tournament.noise, 0)
        self.assertLessEqual(tournament.repetitions, 50)
        self.assertGreaterEqual(tournament.repetitions, 2)

    @given(
        tournament=prob_end_spatial_tournaments(
            strategies=axl.basic_strategies, max_size=3
        )
    )
    @settings(max_examples=5)
    def test_decorator_with_given_strategies(self, tournament):
        self.assertIsInstance(tournament, axl.Tournament)
        basic_player_names = [str(s()) for s in axl.basic_strategies]
        for p in tournament.players:
            self.assertIn(str(p), basic_player_names)


class TestGame(unittest.TestCase):
    def test_call(self):
        game = games().example()
        self.assertIsInstance(game, axl.Game)

    @given(game=games())
    @settings(max_examples=5)
    def test_decorator(self, game):
        self.assertIsInstance(game, axl.Game)
        r, p, s, t = game.RPST()
        self.assertTrue((2 * r) > (t + s) and (t > r > p > s))

    @given(game=games(prisoners_dilemma=False))
    @settings(max_examples=5)
    def test_decorator_unconstrained(self, game):
        self.assertIsInstance(game, axl.Game)
