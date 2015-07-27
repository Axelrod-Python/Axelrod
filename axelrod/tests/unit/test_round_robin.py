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
        self.assertEqual(rr.players, [p1, p2])
        self.assertEqual(rr.nplayers, 2)
        self.assertEqual(rr.game.score(('C', 'C')), (3, 3))
        self.assertEqual(rr.turns, 20)
        self.assertEqual(rr.deterministic_cache, {})
        self.assertEqual(rr.cache_mutable, True)
        self.assertEqual(rr._noise, 0.2)

    def test_stochastic_interaction(self):
        p1, p2 = axelrod.Player(), axelrod.Player()
        rr = axelrod.RoundRobin(
            players=[p1, p2], game=self.game, turns=20, noise=0.2)
        self.assertTrue(rr._stochastic_interaction(p1, p2))
        rr = axelrod.RoundRobin(
            players=[p1, p2], game=self.game, turns=20)
        self.assertFalse(rr._stochastic_interaction(p1, p2))
        p1 = axelrod.Random()
        rr = axelrod.RoundRobin(
            players=[p1, p2], game=self.game, turns=20)
        self.assertTrue(rr._stochastic_interaction(p1, p2))

    def test_cache_update_required(self):
        p1, p2 = axelrod.Player(), axelrod.Player()
        rr = axelrod.RoundRobin(
            players=[p1, p2], game=self.game, turns=20, noise=0.2)
        self.assertFalse(rr._cache_update_required(p1, p2))
        rr = axelrod.RoundRobin(
            players=[p1, p2], game=self.game, turns=20)
        self.assertTrue(rr._cache_update_required(p1, p2))
        p1 = axelrod.Random()
        rr = axelrod.RoundRobin(
            players=[p1, p2], game=self.game, turns=20)
        self.assertFalse(rr._cache_update_required(p1, p2))

    def test_calculate_scores(self):
        p1, p2 = axelrod.Player(), axelrod.Player()
        p1.history = ['C', 'C', 'D', 'D']
        p2.history = ['C', 'D', 'C', 'D']
        rr = axelrod.RoundRobin(
            players=[p1, p2], game=self.game, turns=20)
        result = rr._calculate_scores(p1, p2)
        expected = (9, 9)
        self.assertEqual(result, expected)

    def test_deterministic_cache(self):
        p1, p2, p3 = axelrod.Cooperator(), axelrod.Defector(), axelrod.Random()
        rr = axelrod.RoundRobin(players=[p1, p2, p3], game=self.game, turns=20)
        self.assertEqual(rr.deterministic_cache, {})
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
