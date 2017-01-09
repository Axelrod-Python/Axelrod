import unittest
from hypothesis import given, example
from hypothesis.strategies import integers, floats, assume
import axelrod
from axelrod import Actions
from axelrod.deterministic_cache import DeterministicCache
from axelrod.tests.property import games

C, D = Actions.C, Actions.D


class TestMatch(unittest.TestCase):

    @given(turns=integers(min_value=1, max_value=200), game=games())
    @example(turns=5, game=axelrod.DefaultGame)
    def test_init(self, turns, game):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), turns, game=game)
        self.assertEqual(match.result, [])
        self.assertEqual(match.players, [p1, p2])
        self.assertEqual(
            match.players[0].match_attributes['length'],
            turns
        )
        self.assertEqual(
            match._cache_key, (p1, p2, turns))
        self.assertEqual(match.turns, turns)
        self.assertEqual(match._cache, {})
        self.assertEqual(match.noise, 0)
        self.assertEqual(match.game.RPST(), game.RPST())

    @given(turns=integers(min_value=1, max_value=200), game=games())
    @example(turns=5, game=axelrod.DefaultGame)
    def test_non_default_attributes(self, turns, game):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match_attributes = {
            'length': 500,
            'game': game,
            'noise': 0.5
        }
        match = axelrod.Match((p1, p2), turns, game=game,
                              match_attributes=match_attributes)
        self.assertEqual(match.players[0].match_attributes['length'], 500)
        self.assertEqual(match.players[0].match_attributes['noise'], 0.5)

    @given(turns=integers(min_value=1, max_value=200))
    @example(turns=5)
    def test_len(self, turns):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), turns)
        self.assertEqual(len(match), turns)

    @given(p=floats(min_value=0, max_value=1))
    def test_stochastic(self, p):

        assume(0 < p < 1)

        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), 5)
        self.assertFalse(match._stochastic)

        match = axelrod.Match((p1, p2), 5, noise=p)
        self.assertTrue(match._stochastic)

        p1 = axelrod.Random()
        match = axelrod.Match((p1, p2), 5)
        self.assertTrue(match._stochastic)

    @given(p=floats(min_value=0, max_value=1))
    def test_cache_update_required(self, p):

        assume(0 < p < 1)

        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), 5, noise=p)
        self.assertFalse(match._cache_update_required)

        cache = DeterministicCache()
        cache.mutable = False
        match = axelrod.Match((p1, p2), 5, deterministic_cache=cache)
        self.assertFalse(match._cache_update_required)

        match = axelrod.Match((p1, p2), 5)
        self.assertTrue(match._cache_update_required)

        p1 = axelrod.Random()
        match = axelrod.Match((p1, p2), 5)
        self.assertFalse(match._cache_update_required)

    def test_play(self):
        cache = DeterministicCache()
        players = (axelrod.Cooperator(), axelrod.Defector())
        match = axelrod.Match(players, 3, deterministic_cache=cache)
        expected_result = [(C, D), (C, D), (C, D)]
        self.assertEqual(match.play(), expected_result)
        self.assertEqual(
            cache[(axelrod.Cooperator(), axelrod.Defector(), 3)], expected_result)

        # a deliberately incorrect result so we can tell it came from the cache
        expected_result = [(C, C), (D, D), (D, C)]
        cache[(axelrod.Cooperator(), axelrod.Defector(), 3)] = expected_result
        match = axelrod.Match(players, 3, deterministic_cache=cache)
        self.assertEqual(match.play(), expected_result)

    def test_scores(self):
        player1 = axelrod.TitForTat()
        player2 = axelrod.Defector()
        match = axelrod.Match((player1, player2), 3)
        self.assertEqual(match.scores(), [])
        match.play()
        self.assertEqual(match.scores(), [(0, 5), (1, 1), (1, 1)])

    def test_final_score(self):
        player1 = axelrod.TitForTat()
        player2 = axelrod.Defector()

        match = axelrod.Match((player1, player2), 3)
        self.assertEqual(match.final_score(), None)
        match.play()
        self.assertEqual(match.final_score(), (2, 7))

        match = axelrod.Match((player2, player1), 3)
        self.assertEqual(match.final_score(), None)
        match.play()
        self.assertEqual(match.final_score(), (7, 2))

    def test_final_score_per_turn(self):
        turns = 3
        player1 = axelrod.TitForTat()
        player2 = axelrod.Defector()

        match = axelrod.Match((player1, player2), turns)
        self.assertEqual(match.final_score_per_turn(), None)
        match.play()
        self.assertEqual(match.final_score_per_turn(), (2/float(turns), 7/float(turns)))

        match = axelrod.Match((player2, player1), turns)
        self.assertEqual(match.final_score_per_turn(), None)
        match.play()
        self.assertEqual(match.final_score_per_turn(), (7/float(turns), 2/float(turns)))

    def test_winner(self):
        player1 = axelrod.TitForTat()
        player2 = axelrod.Defector()

        match = axelrod.Match((player1, player2), 3)
        self.assertEqual(match.winner(), None)
        match.play()
        self.assertEqual(match.winner(), player2)

        match = axelrod.Match((player2, player1), 3)
        self.assertEqual(match.winner(), None)
        match.play()
        self.assertEqual(match.winner(), player2)

        player1 = axelrod.Defector()
        match = axelrod.Match((player1, player2), 3)
        self.assertEqual(match.winner(), None)
        match.play()
        self.assertEqual(match.winner(), False)

    def test_cooperation(self):
        turns = 3
        player1 = axelrod.Cooperator()
        player2 = axelrod.Alternator()

        match = axelrod.Match((player1, player2), turns)
        self.assertEqual(match.cooperation(), None)
        match.play()
        self.assertEqual(match.cooperation(), (3, 2))

        player1 = axelrod.Alternator()
        player2 = axelrod.Defector()

        match = axelrod.Match((player1, player2), turns)
        self.assertEqual(match.cooperation(), None)
        match.play()
        self.assertEqual(match.cooperation(), (2, 0))

    def test_normalised_cooperation(self):
        turns = 3
        player1 = axelrod.Cooperator()
        player2 = axelrod.Alternator()

        match = axelrod.Match((player1, player2), turns)
        self.assertEqual(match.normalised_cooperation(), None)
        match.play()
        self.assertEqual(match.normalised_cooperation(), (3/float(turns), 2/float(turns)))

        player1 = axelrod.Alternator()
        player2 = axelrod.Defector()

        match = axelrod.Match((player1, player2), turns)
        self.assertEqual(match.normalised_cooperation(), None)
        match.play()
        self.assertEqual(match.normalised_cooperation(), (2/float(turns), 0/float(turns)))

    def test_sparklines(self):
        players = (axelrod.Cooperator(), axelrod.Alternator())
        match = axelrod.Match(players, 4)
        match.play()
        expected_sparklines = u'████\n█ █ '
        self.assertEqual(match.sparklines(), expected_sparklines)
        expected_sparklines = u'XXXX\nXYXY'
        self.assertEqual(match.sparklines('X', 'Y'), expected_sparklines)
