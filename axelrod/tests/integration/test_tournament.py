import unittest
import axelrod


class TestTournament(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()
        cls.players = [
            axelrod.Cooperator(),
            axelrod.TitForTat(),
            axelrod.Defector(),
            axelrod.Grudger(),
            axelrod.GoByMajority()]
        cls.player_names = [str(p) for p in cls.players]
        cls.test_name = 'test'
        cls.test_repetitions = 5

        cls.expected_outcome = [
            ('Cooperator', [1800, 1800, 1800, 1800, 1800]),
            ('Defector', [1612, 1612, 1612, 1612, 1612]),
            ('Grudger', [1999, 1999, 1999, 1999, 1999]),
            ('Soft Go By Majority', [1999, 1999, 1999, 1999, 1999]),
            ('Tit For Tat', [1999, 1999, 1999, 1999, 1999])]
        cls.expected_outcome.sort()

    def test_full_tournament(self):
        """A test to check that tournament runs with all non cheating strategies."""
        strategies = [strategy() for strategy in axelrod.ordinary_strategies]
        tournament = axelrod.Tournament(name='test', players=strategies, game=self.game, turns=20, repetitions=2)
        output_of_tournament = tournament.play().results
        self.assertEqual(type(output_of_tournament), dict)
        self.assertEqual(len(output_of_tournament['payoff']), len(strategies))

    def test_serial_play(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=20,
            repetitions=self.test_repetitions)
        scores = tournament.play().scores
        actual_outcome = sorted(zip(self.player_names, scores))
        self.assertEqual(actual_outcome, self.expected_outcome)

    def test_parallel_play(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=20,
            repetitions=self.test_repetitions,
            processes=2)
        scores = tournament.play().scores
        actual_outcome = sorted(zip(self.player_names, scores))
        self.assertEqual(actual_outcome, self.expected_outcome)
