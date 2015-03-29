import unittest
import axelrod


class TestTournamentManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_output_directory = './assets/'
        cls.test_with_ecological = True
        cls.test_tournament_name = 'test_tournament'
        cls.test_file_name = 'test_file_name'
        cls.test_file_extenstion = 'png'
        cls.test_strategies = [axelrod.Defector, axelrod.Cooperator]
        cls.test_players = [axelrod.Defector(), axelrod.Cooperator()]

        cls.expected_output_file_path = './assets/test_file_name.png'

    def test_init(self):
        mgr = axelrod.TournamentManager(
            self.test_output_directory,
            self.test_with_ecological)
        self.assertEqual(mgr.output_directory, self.test_output_directory)
        self.assertEqual(mgr.tournaments, [])
        self.assertEqual(mgr.with_ecological, self.test_with_ecological)
        self.assertTrue(mgr.pass_cache)

    def test_one_player_per_strategy(self):
        mgr = axelrod.TournamentManager(
            self.test_output_directory,
            self.test_with_ecological)
        players = mgr.one_player_per_strategy(self.test_strategies)
        self.assertIsInstance(players[0], axelrod.Defector)
        self.assertIsInstance(players[1], axelrod.Cooperator)

    def test_output_file_path(self):
        mgr = axelrod.TournamentManager(
            self.test_output_directory,
            self.test_with_ecological)
        output_file_path = mgr.output_file_path(
            self.test_file_name, self.test_file_extenstion)
        self.assertEqual(output_file_path, self.expected_output_file_path)

    def test_add_tournament(self):
        mgr = axelrod.TournamentManager(
            self.test_output_directory,
            self.test_with_ecological)
        mgr.add_tournament(
            players=self.test_players, name=self.test_tournament_name)
        self.assertEqual(len(mgr.tournaments), 1)
        self.assertIsInstance(mgr.tournaments[0], axelrod.Tournament)
        self.assertEqual(mgr.tournaments[0].name, self.test_tournament_name)

    def test_valid_cache(self):
        mgr = axelrod.TournamentManager(
            output_directory=self.test_output_directory,
            with_ecological=self.test_with_ecological, load_cache=False)
        mgr.add_tournament(
                players=self.test_players, name=self.test_tournament_name)
        self.assertTrue(mgr.valid_cache(200))
        mgr.deterministic_cache['test_key'] = 'test_value'
        self.assertFalse(mgr.valid_cache(200))
        mgr.cache_valid_for_turns = 500
        self.assertFalse(mgr.valid_cache(200))
        self.assertTrue(mgr.valid_cache(500))
