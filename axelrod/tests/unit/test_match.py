import unittest
import axelrod.match as am
import axelrod


class TestMatch(unittest.TestCase):

    def test_actions(self):
        pass

    def test_pair_of_players(self):
        players = [
            axelrod.Cooperator(), axelrod.Defector(), axelrod.TitForTat()]
        player1, player2, key = am.pair_of_players(players, 0, 2)
        self.assertEqual(player1.name, 'Cooperator')
        self.assertEqual(player2.name, 'Tit For Tat')
        self.assertEqual(key[0], axelrod.Cooperator)
        self.assertEqual(key[1], axelrod.TitForTat)
        player1, player2, key = am.pair_of_players(players, 0, 0)
        self.assertEqual(player1.name, player2.name)
        self.assertEqual(key[0], key[1])
        self.assertNotEqual(player1, player2)
        # Check that the two player instances are wholly independent
        player1.name = 'player 1'
        player2.name = 'player 2'
        self.assertNotEqual(player1.name, player2.name)

    def test_is_stochastic_match(self):
        p1, p2 = axelrod.Player(), axelrod.Player()
        self.assertTrue(am.is_stochastic_match(p1, p2, 0.2))
        self.assertFalse(am.is_stochastic_match(p1, p2, 0))
        p1 = axelrod.Random()
        self.assertTrue(am.is_stochastic_match(p1, p2, 0))

    def test_play_match(self):
        pass

    def test_cache_update_required(self):
        p1, p2 = axelrod.Player(), axelrod.Player()
        self.assertFalse(am.cache_update_required(p1, p2, True, 0.2))
        self.assertFalse(am.cache_update_required(p1, p2, False, 0))
        self.assertTrue(am.cache_update_required(p1, p2, True, 0))
        p1 = axelrod.Random()
        self.assertFalse(am.cache_update_required(p1, p2, True, 0))
