import unittest
import axelrod


class TestTournamentManagerFactory(unittest.TestCase):

    def test_tournaments_dict(self):
        tm = axelrod.TournamentManagerFactory

        expected_basic_strategies = axelrod.basic_strategies
        expected_strategies = (
            axelrod.basic_strategies +
            axelrod.ordinary_strategies)
        expected_cheating_strategies = axelrod.cheating_strategies
        expected_all_strategies = (
            axelrod.basic_strategies +
            axelrod.ordinary_strategies +
            axelrod.cheating_strategies)

        actual_basic_strategies = tm._tournaments_dict()['basic_strategies']
        actual_strategies = tm._tournaments_dict()['strategies']
        actual_cheating_strategies = (
            tm._tournaments_dict()['cheating_strategies'])
        actual_all_strategies = tm._tournaments_dict()['all_strategies']

        self.assertEqual(actual_basic_strategies, expected_basic_strategies)
        self.assertEqual(actual_strategies, expected_strategies)
        self.assertEqual(
            actual_cheating_strategies, expected_cheating_strategies)
        self.assertEqual(actual_all_strategies, expected_all_strategies)

        excluding_basic = tm._tournaments_dict(['basic_strategies'])
        self.assertFalse('basic_strategies' in excluding_basic)
        self.assertEqual(excluding_basic['strategies'], expected_strategies)

    def test_add_tournaments(self):
        pass

    def test_create_tournament_manager(self):
        pass
