import unittest
import axelrod


class TestTournamentManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_logger = axelrod.NullLogger()
        cls.test_output_directory = './assets/'
        cls.test_tournament_name = 'test_tournament'
        cls.test_file_name = 'test_file_name'
        cls.test_file_extenstion = 'png'
        cls.test_strategies = [axelrod.Defector, axelrod.Cooperator]
        cls.test_players = [axelrod.Defector(), axelrod.Cooperator()]

        cls.expected_output_file_path = './assets/test_file_name.png'

    def test_init(self):
        mgr = axelrod.TournamentManager(self.test_logger, self.test_output_directory)
        self.assertEqual(mgr.output_directory, self.test_output_directory)
        self.assertEqual(mgr.tournaments, [])

    def test_one_player_per_strategy(self):
        mgr = axelrod.TournamentManager(self.test_logger, self.test_output_directory)
        players = mgr.one_player_per_strategy(self.test_strategies)
        self.assertIsInstance(players[0], axelrod.Defector)
        self.assertIsInstance(players[1], axelrod.Cooperator)

    def test_output_file_path(self):
        mgr = axelrod.TournamentManager(self.test_logger, self.test_output_directory)
        output_file_path = mgr.output_file_path(
            self.test_file_name, self.test_file_extenstion)
        self.assertEqual(output_file_path, self.expected_output_file_path)

    def test_add_tournament(self):
        mgr = axelrod.TournamentManager(self.test_logger, self.test_output_directory)
        mgr.add_tournament(self.test_tournament_name, self.test_players)
        self.assertEqual(len(mgr.tournaments), 1)
        self.assertIsInstance(mgr.tournaments[0], axelrod.Tournament)
        self.assertEqual(mgr.tournaments[0].name, self.test_tournament_name)
