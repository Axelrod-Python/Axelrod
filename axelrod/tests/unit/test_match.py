# -*- coding: utf-8 -*-

import unittest
import axelrod
from axelrod import Actions

from hypothesis import given, example
from hypothesis.strategies import integers, floats, random_module, assume

C, D = Actions.C, Actions.D


class TestMatch(unittest.TestCase):

    @given(turns=integers(min_value=1, max_value=200))
    @example(turns=5)
    def test_init(self, turns):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), turns)
        self.assertEqual(match.result, [])
        self.assertEqual(match.players, [p1, p2])
        self.assertEqual(
            match._classes, (axelrod.Cooperator, axelrod.Cooperator))
        self.assertEqual(match._turns, turns)
        self.assertEqual(match._cache, {})
        self.assertEqual(match._cache_mutable, True)
        self.assertEqual(match._noise, 0)

    @given(turns=integers(min_value=1, max_value=200))
    @example(turns=5)
    def test_len(self, turns):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), turns)
        self.assertEqual(len(match), turns)

    @given(p=floats(min_value=0, max_value=1),
           rm=random_module())
    def test_stochastic(self, p, rm):

        assume(0 < p < 1)

        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), 5)
        self.assertFalse(match._stochastic)

        match = axelrod.Match((p1, p2), 5, noise=p)
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

    def test_scores(self):
        player1 = axelrod.TitForTat()
        player2 = axelrod.Defector()
        match = axelrod.Match((player1, player2), 3)
        self.assertEqual(match.scores(), [])
        match.play()
        self.assertEqual(match.scores(), [(0, 5), (1, 1), (1, 1)])

    def test_sparklines(self):
        players = (axelrod.Cooperator(), axelrod.Alternator())
        match = axelrod.Match(players, 4)
        match.play()
        expected_sparklines = u'████\n█ █ '
        self.assertEqual(match.sparklines(), expected_sparklines)
        expected_sparklines = u'XXXX\nXYXY'
        self.assertEqual(match.sparklines('X', 'Y'), expected_sparklines)
