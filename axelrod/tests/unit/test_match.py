import unittest
from collections import Counter

import axelrod
from axelrod import Action
from axelrod.deterministic_cache import DeterministicCache
from axelrod.tests.property import games

from hypothesis import example, given
from hypothesis.strategies import assume, floats, integers

C, D = Action.C, Action.D


class TestMatch(unittest.TestCase):
    @given(turns=integers(min_value=1, max_value=200), game=games())
    @example(turns=5, game=axelrod.DefaultGame)
    def test_init(self, turns, game):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), turns, game=game)
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
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), prob_end=prob_end, game=game)
        self.assertEqual(match.result, [])
        self.assertEqual(match.players, [p1, p2])
        self.assertEqual(match.turns, float("inf"))
        self.assertEqual(match.prob_end, prob_end)
        self.assertEqual(match.noise, 0)
        self.assertEqual(match.game.RPST(), game.RPST())

        self.assertEqual(match.players[0].match_attributes["length"], float("inf"))
        self.assertEqual(match._cache, {})

    @given(
        prob_end=floats(min_value=0, max_value=1),
        turns=integers(min_value=1, max_value=200),
        game=games(),
    )
    def test_init_with_prob_end_and_turns(self, turns, prob_end, game):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), turns=turns, prob_end=prob_end, game=game)
        self.assertEqual(match.result, [])
        self.assertEqual(match.players, [p1, p2])
        self.assertEqual(match.turns, turns)
        self.assertEqual(match.prob_end, prob_end)
        self.assertEqual(match.noise, 0)
        self.assertEqual(match.game.RPST(), game.RPST())

        self.assertEqual(match.players[0].match_attributes["length"], float("inf"))
        self.assertEqual(match._cache, {})

    def test_default_init(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2))
        self.assertEqual(match.result, [])
        self.assertEqual(match.players, [p1, p2])
        self.assertEqual(match.turns, axelrod.DEFAULT_TURNS)
        self.assertEqual(match.prob_end, 0)
        self.assertEqual(match.noise, 0)
        self.assertEqual(match.game.RPST(), (3, 1, 0, 5))

        self.assertEqual(
            match.players[0].match_attributes["length"], axelrod.DEFAULT_TURNS
        )
        self.assertEqual(match._cache, {})

    def test_example_prob_end(self):
        """
        Test that matches have diff length and also that cache has recorded the
        outcomes
        """
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), prob_end=0.5)
        expected_lengths = [3, 1, 5]
        for seed, expected_length in zip(range(3), expected_lengths):
            axelrod.seed(seed)
            self.assertEqual(match.players[0].match_attributes["length"], float("inf"))
            self.assertEqual(len(match.play()), expected_length)
            self.assertEqual(match.noise, 0)
            self.assertEqual(match.game.RPST(), (3, 1, 0, 5))
        self.assertEqual(len(match._cache), 1)
        self.assertEqual(match._cache[(p1, p2)], [(C, C)] * 5)

    @given(turns=integers(min_value=1, max_value=200), game=games())
    @example(turns=5, game=axelrod.DefaultGame)
    def test_non_default_attributes(self, turns, game):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match_attributes = {"length": 500, "game": game, "noise": 0.5}
        match = axelrod.Match(
            (p1, p2), turns, game=game, match_attributes=match_attributes
        )
        self.assertEqual(match.players[0].match_attributes["length"], 500)
        self.assertEqual(match.players[0].match_attributes["noise"], 0.5)

    @given(turns=integers(min_value=1, max_value=200))
    @example(turns=5)
    def test_len(self, turns):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), turns)
        self.assertEqual(len(match), turns)

    def test_len_error(self):
        """
        Length is not defined if it is infinite.
        """
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), prob_end=0.5)
        with self.assertRaises(TypeError):
            len(match)

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
            cache[(axelrod.Cooperator(), axelrod.Defector())], expected_result
        )

        # a deliberately incorrect result so we can tell it came from the cache
        expected_result = [(C, C), (D, D), (D, C), (C, C), (C, D)]
        cache[(axelrod.Cooperator(), axelrod.Defector())] = expected_result
        match = axelrod.Match(players, 3, deterministic_cache=cache)
        self.assertEqual(match.play(), expected_result[:3])

    def test_cache_grows(self):
        """
        We want to make sure that if we try to use the cache for more turns than
        what is stored, then it will instead regenerate the result and overwrite
        the cache.
        """
        cache = DeterministicCache()
        players = (axelrod.Cooperator(), axelrod.Defector())
        match = axelrod.Match(players, 3, deterministic_cache=cache)
        expected_result_5_turn = [(C, D), (C, D), (C, D), (C, D), (C, D)]
        expected_result_3_turn = [(C, D), (C, D), (C, D)]
        self.assertEqual(match.play(), expected_result_3_turn)
        match.turns = 5
        self.assertEqual(match.play(), expected_result_5_turn)
        # The cache should now hold the 5-turn result..
        self.assertEqual(
            cache[(axelrod.Cooperator(), axelrod.Defector())],
            expected_result_5_turn
        )

    def test_cache_doesnt_shrink(self):
        """
        We want to make sure that when we access the cache looking for fewer
        turns than what is stored, then it will not overwrite the cache with the
        shorter result.
        """
        cache = DeterministicCache()
        players = (axelrod.Cooperator(), axelrod.Defector())
        match = axelrod.Match(players, 5, deterministic_cache=cache)
        expected_result_5_turn = [(C, D), (C, D), (C, D), (C, D), (C, D)]
        expected_result_3_turn = [(C, D), (C, D), (C, D)]
        self.assertEqual(match.play(), expected_result_5_turn)
        match.turns = 3
        self.assertEqual(match.play(), expected_result_3_turn)
        # The cache should still hold the 5.
        self.assertEqual(
            cache[(axelrod.Cooperator(), axelrod.Defector())],
            expected_result_5_turn
        )

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
        self.assertEqual(match.final_score_per_turn(), (2 / turns, 7 / turns))

        match = axelrod.Match((player2, player1), turns)
        self.assertEqual(match.final_score_per_turn(), None)
        match.play()
        self.assertEqual(match.final_score_per_turn(), (7 / turns, 2 / turns))

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
        self.assertEqual(match.normalised_cooperation(), (3 / turns, 2 / turns))

        player1 = axelrod.Alternator()
        player2 = axelrod.Defector()

        match = axelrod.Match((player1, player2), turns)
        self.assertEqual(match.normalised_cooperation(), None)
        match.play()
        self.assertEqual(match.normalised_cooperation(), (2 / turns, 0 / turns))

    def test_state_distribution(self):
        turns = 3
        player1 = axelrod.Cooperator()
        player2 = axelrod.Alternator()

        match = axelrod.Match((player1, player2), turns)
        self.assertEqual(match.state_distribution(), None)

        match.play()
        expected = Counter({(C, C): 2, (C, D): 1})
        self.assertEqual(match.state_distribution(), expected)

        player1 = axelrod.Alternator()
        player2 = axelrod.Defector()

        match = axelrod.Match((player1, player2), turns)
        self.assertEqual(match.state_distribution(), None)

        match.play()
        expected = Counter({(C, D): 2, (D, D): 1})
        self.assertEqual(match.state_distribution(), expected)

    def test_normalised_state_distribution(self):
        turns = 3
        player1 = axelrod.Cooperator()
        player2 = axelrod.Alternator()

        match = axelrod.Match((player1, player2), turns)
        self.assertEqual(match.normalised_state_distribution(), None)

        match.play()
        expected = Counter({(C, C): 2 / turns, (C, D): 1 / turns})
        self.assertEqual(match.normalised_state_distribution(), expected)

        player1 = axelrod.Alternator()
        player2 = axelrod.Defector()

        match = axelrod.Match((player1, player2), turns)
        self.assertEqual(match.normalised_state_distribution(), None)

        match.play()
        expected = Counter({(C, D): 2 / turns, (D, D): 1 / turns})
        self.assertEqual(match.normalised_state_distribution(), expected)

    def test_sparklines(self):
        players = (axelrod.Cooperator(), axelrod.Alternator())
        match = axelrod.Match(players, 4)
        match.play()
        expected_sparklines = "████\n█ █ "
        self.assertEqual(match.sparklines(), expected_sparklines)
        expected_sparklines = "XXXX\nXYXY"
        self.assertEqual(match.sparklines("X", "Y"), expected_sparklines)


class TestSampleLength(unittest.TestCase):
    def test_sample_length(self):
        for seed, prob_end, expected_length in [
            (0, 0.5, 3),
            (1, 0.5, 1),
            (2, 0.6, 4),
            (3, 0.4, 1),
        ]:
            axelrod.seed(seed)
            self.assertEqual(axelrod.match.sample_length(prob_end), expected_length)

    def test_sample_with_0_prob(self):
        self.assertEqual(axelrod.match.sample_length(0), float("inf"))

    def test_sample_with_1_prob(self):
        self.assertEqual(axelrod.match.sample_length(1), 1)
