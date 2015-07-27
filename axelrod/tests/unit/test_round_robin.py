import unittest
import random
import axelrod


class TestRoundRobin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()

    def test_init(self):
        p1, p2 = axelrod.Player(), axelrod.Player()
        rr = axelrod.RoundRobin(
            players=[p1, p2], game=self.game, turns=20, noise=0.2)
        self.assertEquals(rr.players, [p1, p2])
        self.assertEquals(rr.nplayers, 2)
        self.assertEquals(rr.game.score(('C', 'C')), (3, 3))
        self.assertEqual(rr.turns, 20)
        self.assertEqual(rr.deterministic_cache, {})
        self.assertEqual(rr.cache_mutable, True)
        self.assertEqual(rr._noise, 0.2)

    def test_deterministic_cache(self):
        p1, p2, p3 = axelrod.Cooperator(), axelrod.Defector(), axelrod.Random()
        rr = axelrod.RoundRobin(players=[p1, p2, p3], game=self.game, turns=20)
        self.assertEquals(rr.deterministic_cache, {})
        rr.play()
        self.assertEqual(rr.deterministic_cache[(axelrod.Defector, axelrod.Defector)], (20, 20))
        self.assertEqual(rr.deterministic_cache[(axelrod.Cooperator, axelrod.Cooperator)], (60, 60))
        self.assertEqual(rr.deterministic_cache[(axelrod.Cooperator, axelrod.Defector)], (0, 100))
        self.assertFalse((axelrod.Random, axelrod.Random) in rr.deterministic_cache)

    def test_noisy_cache(self):
        p1, p2, p3 = axelrod.Cooperator(), axelrod.Defector(), axelrod.Random()
        rr = axelrod.RoundRobin(
            players=[p1, p2, p3], game=self.game, turns=20, noise=0.2)
        rr.play()
        self.assertEqual(rr.deterministic_cache, {})

    def test_noisy_play(self):
        random.seed(1)
        p1, p2, p3 = axelrod.Cooperator(), axelrod.Defector(), axelrod.Random()
        rr = axelrod.RoundRobin(
            players=[p1, p2, p3], game=self.game, turns=20, noise=0.2)
        payoff = rr.play()
        expected_payoff = [[57, 10, 45], [80, 40, 57], [65, 22, 37]]
        self.assertEqual(payoff, expected_payoff)
