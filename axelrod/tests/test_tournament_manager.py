import unittest
import axelrod


class TestTournamentManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_output_directory = './assets/'
        cls.test_strategies = [axelrod.Defector, axelrod.Cooperator]

    def test_init(self):
        mgr = axelrod.TournamentManager(self.test_output_directory)
        self.assertEqual(mgr.output_directory, self.test_output_directory)
        self.assertEqual(mgr.tournaments, [])

    def test_one_player_per_strategy(self):
        mgr = axelrod.TournamentManager(self.test_output_directory)
        players = mgr.one_player_per_strategy(self.test_strategies)
        self.assertIsInstance(players[0], axelrod.Defector)
        self.assertIsInstance(players[1], axelrod.Cooperator)
