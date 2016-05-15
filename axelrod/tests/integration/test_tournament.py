import unittest
import axelrod
import tempfile


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
            ('Cooperator', [180, 180, 180, 180, 180]),
            ('Defector', [172, 172, 172, 172, 172]),
            ('Grudger', [199, 199, 199, 199, 199]),
            ('Soft Go By Majority', [199, 199, 199, 199, 199]),
            ('Tit For Tat', [199, 199, 199, 199, 199])]
        cls.expected_outcome.sort()

    def test_full_tournament(self):
        """A test to check that tournament runs with all non cheating strategies."""
        strategies = [strategy() for strategy in axelrod.ordinary_strategies]
        tournament = axelrod.Tournament(name='test', players=strategies,
                                        game=self.game, turns=2,
                                        repetitions=2)
        tmp_file = tempfile.NamedTemporaryFile()
        self.assertIsNone(tournament.play(progress_bar=False,
                                          filename=tmp_file.name,
                                          build_results=False))

    def test_serial_play(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=20,
            repetitions=self.test_repetitions)
        scores = tournament.play(progress_bar=False).scores
        actual_outcome = sorted(zip(self.player_names, scores))
        self.assertEqual(actual_outcome, self.expected_outcome)

    def test_parallel_play(self):
        tournament = axelrod.Tournament(
            name=self.test_name,
            players=self.players,
            game=self.game,
            turns=20,
            repetitions=self.test_repetitions)
        scores = tournament.play(processes=2, progress_bar=False).scores
        actual_outcome = sorted(zip(self.player_names, scores))
        self.assertEqual(actual_outcome, self.expected_outcome)
