import unittest
import random
import axelrod

C, D = axelrod.Actions.C, axelrod.Actions.D

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
        self.assertEqual(rr.game.score((C, C)), (3, 3))
        self.assertEqual(rr.turns, 20)
        self.assertEqual(rr.deterministic_cache, {})
        self.assertEqual(rr.cache_mutable, True)
        self.assertEqual(rr._noise, 0.2)

    def test_play(self):
        p1, p2, p3 = axelrod.Cooperator(), axelrod.Defector(), axelrod.Random()
        rr = axelrod.RoundRobin(
            players=[p1, p2, p3], game=self.game, turns=20)
        results = rr.play()
        expected_payoff = [[60.0, 0, 33], [100, 20.0, 56], [78, 11, 46.5]]
        expected_cooperation = [
            [20, 20, 20], [0, 0, 0], [11, 9, 13]]
        self.assertEqual(results['payoff'], expected_payoff)
        self.assertEqual(results['cooperation'], expected_cooperation)

    def test_noisy_play(self):
        random.seed(1)
        p1, p2, p3 = axelrod.Cooperator(), axelrod.Defector(), axelrod.Random()
        rr = axelrod.RoundRobin(
            players=[p1, p2, p3], game=self.game, turns=20, noise=0.2)
        results = rr.play()
        expected_payoff = [[57, 10, 45], [80, 40, 57], [65, 22, 37]]
        expected_cooperation = [
            [15, 16, 17], [2, 3, 4], [13, 11, 9]]
        self.assertEqual(results['payoff'], expected_payoff)
        self.assertEqual(results['cooperation'], expected_cooperation)

    def test_empty_matrix(self):
        p1, p2 = axelrod.Player(), axelrod.Player()
        rr = axelrod.RoundRobin(
            players=[p1, p2], game=self.game, turns=20)
        result = rr._empty_matrix(2, 2)
        expected = [[0, 0], [0, 0]]
        self.assertEqual(result, expected)

    def test_score_single_interaction(self):
        players = [
            axelrod.Alternator(), axelrod.Defector(), axelrod.TitForTat()]
        rr = axelrod.RoundRobin(
            players=players, game=self.game, turns=20)
        scores, cooperation_rates = rr._score_single_interaction(0, 2)
        expected_scores = (53, 48)
        expected_cooperation_rates = (10, 11)
        self.assertEqual(expected_scores, scores)
        self.assertEqual(expected_cooperation_rates, cooperation_rates)

    # TODO
    # Use MagicMock to test that _play_single_interaction is called / not
    # called in the correct cirucumstances.

    def test_update_matrices(self):
        players = [
            axelrod.Alternator(), axelrod.Defector(), axelrod.TitForTat()]
        rr = axelrod.RoundRobin(
            players=players, game=self.game, turns=20)
        scores = (53, 48)
        cooperation_rates = (0.5, 0.55)
        payoffs = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        cooperation = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        rr._update_matrices(
            0, 2, scores, payoffs, cooperation_rates, cooperation)
        expected_payoffs = [[0, 0, 53], [0, 0, 0], [48, 0, 0]]
        expected_cooperation = [[0, 0, 0.5], [0, 0, 0], [0.55, 0, 0]]
        self.assertEqual(expected_payoffs, payoffs)
        self.assertEqual(expected_cooperation, cooperation)

    def test_pair_of_players(self):
        players = [
            axelrod.Cooperator(), axelrod.Defector(), axelrod.TitForTat()]
        rr = axelrod.RoundRobin(
            players=players, game=self.game, turns=20)
        player1, player2, key = rr._pair_of_players(0, 2)
        self.assertEqual(player1.name, 'Cooperator')
        self.assertEqual(player2.name, 'Tit For Tat')
        self.assertEqual(key[0], axelrod.Cooperator)
        self.assertEqual(key[1], axelrod.TitForTat)
        player1, player2, key = rr._pair_of_players(0, 0)
        self.assertEqual(player1.name, player2.name)
        self.assertEqual(key[0], key[1])
        self.assertNotEqual(player1, player2)
        # Check that the two player instances are wholly independent
        player1.name = 'player 1'
        player2.name = 'player 2'
        self.assertNotEqual(player1.name, player2.name)

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

    def test_play_single_interaction(self):
        players = [
            axelrod.Alternator(), axelrod.Defector(), axelrod.TitForTat()]
        rr = axelrod.RoundRobin(
            players=players, game=self.game, turns=20)
        player1 = players[0]
        player2 = players[2]
        classes = (player1.__class__, player2.__class__)
        scores, cooperation_rates = (
            rr._play_single_interaction(player1, player2, classes))
        expected_scores = (53, 48)
        expected_cooperation_rates = (10, 11)
        self.assertEqual(expected_scores, scores)
        self.assertEqual(expected_cooperation_rates, cooperation_rates)

    def test_calculate_scores(self):
        p1, p2 = axelrod.Player(), axelrod.Player()
        p1.history = [C, C, D, D]
        p2.history = [C, D, C, D]
        rr = axelrod.RoundRobin(
            players=[p1, p2], game=self.game, turns=20)
        result = rr._calculate_scores(p1, p2)
        expected = (9, 9)
        self.assertEqual(result, expected)

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

    def test_calculate_cooperation(self):
        p1, p2 = axelrod.Player(), axelrod.Player()
        p1.history = [C, C, D, D]
        rr = axelrod.RoundRobin(
            players=[p1, p2], game=self.game, turns=20)
        result = rr._calculate_cooperation(p1)
        expected = 2
        self.assertEqual(result, expected)
