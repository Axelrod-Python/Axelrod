import unittest
import axelrod


class TestMatch(unittest.TestCase):

    def test_init(self):
        p1, p2 = axelrod.Player(), axelrod.Player()
        match = axelrod.Match((p1, p2), 5)
        self.assertEqual(match._player1, p1)

    def test_stochastic(self):
        p1, p2 = axelrod.Player(), axelrod.Player()
        match = axelrod.Match((p1, p2), 5)
        self.assertFalse(match._stochastic)

        match = axelrod.Match((p1, p2), 5, noise=0.2)
        self.assertTrue(match._stochastic)

        p1 = axelrod.Random()
        match = axelrod.Match((p1, p2), 5)
        self.assertTrue(match._stochastic)

    def test_play_required(self):
        p1, p2 = axelrod.Player(), axelrod.Player()
        match = axelrod.Match((p1, p2), 5)
        self.assertTrue(match._play_required)

        cache = {(axelrod.Player, axelrod.Player): 'test'}
        match = axelrod.Match((p1, p2), 5, cache)
        self.assertFalse(match._play_required)

        p1 = axelrod.Random()
        match = axelrod.Match((p1, p2), 5)
        self.assertTrue(match._play_required)

    def test_cache_update_required(self):
        p1, p2 = axelrod.Player(), axelrod.Player()
        match = axelrod.Match((p1, p2), 5, noise=0.2)
        self.assertFalse(match._cache_update_required)

        match = axelrod.Match((p1, p2), 5, cache_mutable=False)
        self.assertFalse(match._cache_update_required)

        match = axelrod.Match((p1, p2), 5)
        self.assertTrue(match._cache_update_required)

        p1 = axelrod.Random()
        match = axelrod.Match((p1, p2), 5)
        self.assertFalse(match._cache_update_required)

    def test_results(self):
        pass

    def test_play(self):
        pass
