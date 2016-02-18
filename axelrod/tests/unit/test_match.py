# -*- coding: utf-8 -*-

import unittest
import axelrod
from axelrod import Actions

from hypothesis import given, example
from hypothesis.strategies import integers, floats, random_module, assume

C, D = Actions.C, Actions.D


class TestMatch(unittest.TestCase):

    @given(turns=integers(min_value=1, max_value=200),
           prob_end=floats(min_value=0, max_value=1))
    @example(turns=5, prob_end=None)
    def test_init(self, turns, prob_end):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), turns, prob_end=prob_end)
        self.assertEqual(match.result, [])
        self.assertEqual(match._player1, p1)
        self.assertEqual(match._player2, p2)
        self.assertEqual(
            match._classes, (axelrod.Cooperator, axelrod.Cooperator))
        self.assertEqual(match._turns, turns)
        self.assertEqual(match._prob_end, prob_end)
        self.assertEqual(match._cache, {})
        self.assertEqual(match._cache_mutable, True)
        self.assertEqual(match._noise, 0)

        # Checking that prob_end has default None
        match = axelrod.Match((p1, p2), turns)
        self.assertEqual(match.result, [])
        self.assertEqual(match._player1, p1)
        self.assertEqual(match._player2, p2)
        self.assertEqual(
            match._classes, (axelrod.Cooperator, axelrod.Cooperator))
        self.assertEqual(match._turns, turns)
        self.assertEqual(match._prob_end, None)
        self.assertEqual(match._cache, {})
        self.assertEqual(match._cache_mutable, True)
        self.assertEqual(match._noise, 0)

    @given(p=floats(min_value=0, max_value=1),
           rm=random_module())
    def test_stochastic(self, p, rm):

        assume(0 < p < 1)

        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), 5)
        self.assertFalse(match._stochastic)

        match = axelrod.Match((p1, p2), 5, noise=p)
        self.assertTrue(match._stochastic)

        match = axelrod.Match((p1, p2), 5, prob_end=p)
        self.assertTrue(match._stochastic)

        p1 = axelrod.Random()
        match = axelrod.Match((p1, p2), 5)
        self.assertTrue(match._stochastic)

    @given(p=floats(min_value=0, max_value=1),
           rm=random_module())
    def test_cache_update_required(self, p, rm):

        assume(0 < p < 1)

        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), 5, noise=p)
        self.assertFalse(match._cache_update_required)

        match = axelrod.Match((p1, p2), 5, prob_end=p)
        self.assertFalse(match._cache_update_required)

        match = axelrod.Match((p1, p2), 5, cache_mutable=False)
        self.assertFalse(match._cache_update_required)

        match = axelrod.Match((p1, p2), 5)
        self.assertTrue(match._cache_update_required)

        p1 = axelrod.Random()
        match = axelrod.Match((p1, p2), 5)
        self.assertFalse(match._cache_update_required)

    def test_play(self):
        cache = {}
        players = (axelrod.Cooperator(), axelrod.Defector())
        match = axelrod.Match(players, 3, cache)
        expected_result = [(C, D), (C, D), (C, D)]
        self.assertEqual(match.play(), expected_result)
        self.assertEqual(
            cache[(axelrod.Cooperator, axelrod.Defector)], expected_result)

        # a deliberately incorrect result so we can tell it came from the cache
        expected_result = [(C, C), (D, D), (D, C)]
        cache = {(axelrod.Cooperator, axelrod.Defector): expected_result}
        match = axelrod.Match(players, 3, cache)
        self.assertEqual(match.play(), expected_result)

    @given(turns=integers(min_value=1, max_value=200),
           prob_end=floats(min_value=0, max_value=1),
           rm=random_module())
    def test_prob_end_play(self, turns, prob_end, rm):

        players = (axelrod.Cooperator(), axelrod.Defector())
        match = axelrod.Match(players, turns, prob_end=prob_end)
        self.assertTrue(0 <= len(match.play()))

        # If game has no ending the length will be turns
        match = axelrod.Match(players, turns, prob_end=0)
        self.assertEqual(len(match.play()), turns)

        # If game has 1 prob of ending it lasts only one turn
        match = axelrod.Match(players, turns, prob_end=1)
        self.assertEqual(len(match.play()), 1)

    @given(prob_end=floats(min_value=0.25, max_value=0.75),
           rm=random_module())
    def test_prob_end_play_with_no_turns(self, prob_end, rm):
        players = (axelrod.Cooperator(), axelrod.Defector())
        match = axelrod.Match(players, float("inf"), prob_end=prob_end)
        self.assertTrue(0 <= len(match.play()))

    def test_sparklines(self):
        players = (axelrod.Cooperator(), axelrod.Alternator())
        match = axelrod.Match(players, 4)
        match.play()
        expected_sparklines = u'████\n█ █ '
        self.assertEqual(match.sparklines(), expected_sparklines)
        expected_sparklines = u'XXXX\nXYXY'
        self.assertEqual(match.sparklines('X', 'Y'), expected_sparklines)
