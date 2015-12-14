import unittest
import axelrod
from axelrod import Actions

C, D = Actions.C, Actions.D


class TestMatch(unittest.TestCase):

    def test_init(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), 5)
        self.assertEqual(match._player1, p1)
        self.assertEqual(match._classes, (axelrod.Cooperator, axelrod.Cooperator))

    def test_stochastic(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), 5)
        self.assertFalse(match._stochastic)

        match = axelrod.Match((p1, p2), 5, noise=0.2)
        self.assertTrue(match._stochastic)

        p1 = axelrod.Random()
        match = axelrod.Match((p1, p2), 5)
        self.assertTrue(match._stochastic)

    def test_cache_update_required(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        match = axelrod.Match((p1, p2), 5, noise=0.2)
        self.assertFalse(match._cache_update_required)

        match = axelrod.Match((p1, p2), 5, cache_mutable=False)
        self.assertFalse(match._cache_update_required)

        match = axelrod.Match((p1, p2), 5)
        self.assertTrue(match._cache_update_required)

        p1 = axelrod.Random()
        match = axelrod.Match((p1, p2), 5)
        self.assertFalse(match._cache_update_required)

    def test_result(self):
        players = (axelrod.Cooperator(), axelrod.Defector())
        match = axelrod.Match(players, 3)
        expected_result = [(C, D), (C, D), (C, D)]
        self.assertEqual(match.result, expected_result)

        # a deliberately incorrect result so we can tell it came from the cache
        expected_result = [(C, C), (D, D), (D, C)]
        cache = {(axelrod.Cooperator, axelrod.Defector): expected_result}
        match = axelrod.Match(players, 3, cache)
        self.assertEqual(match.result, expected_result)

    def test_play(self):
        cache = {}
        players = (axelrod.Cooperator(), axelrod.Defector())
        match = axelrod.Match(players, 3, cache)
        expected_result = [(C, D), (C, D), (C, D)]
        self.assertEqual(match._play(), expected_result)
        self.assertEqual(
            cache[(axelrod.Cooperator, axelrod.Defector)], expected_result)
