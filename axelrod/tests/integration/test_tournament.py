import unittest
import axelrod
import tempfile
import filecmp

from axelrod.strategy_transformers import FinalTransformer

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
        strategies = [strategy() for strategy in axelrod.strategies]
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

    def test_repeat_tournament_deterministic(self):
        """A test to check that tournament gives same results."""
        deterministic_players = [s() for s in axelrod.strategies
                                 if not s().classifier['stochastic']]
        files = []
        for _ in range(2):
            tournament = axelrod.Tournament(name='test',
                                            players=deterministic_players,
                                            game=self.game, turns=2,
                                            repetitions=2)
            files.append(tempfile.NamedTemporaryFile())
            tournament.play(progress_bar=False, filename=files[-1].name,
                            build_results=False)
        self.assertTrue(filecmp.cmp(files[0].name, files[1].name))

    def test_repeat_tournament_stochastic(self):
        """
        A test to check that tournament gives same results when setting seed.
        """
        files = []
        for _ in range(2):
            axelrod.seed(0)
            stochastic_players = [s() for s in axelrod.strategies
                                  if s().classifier['stochastic']]
            tournament = axelrod.Tournament(name='test',
                                            players=stochastic_players,
                                            game=self.game, turns=2,
                                            repetitions=2)
            files.append(tempfile.NamedTemporaryFile())
            tournament.play(progress_bar=False, filename=files[-1].name,
                            build_results=False)
        self.assertTrue(filecmp.cmp(files[0].name, files[1].name))


class TestNoisyTournament(unittest.TestCase):
    def test_noisy_tournament(self):
        # Defector should win for low noise
        players = [axelrod.Cooperator(), axelrod.Defector()]
        tournament = axelrod.Tournament(players, turns=20, repetitions=10,
                                        with_morality=False, noise=0.)
        results = tournament.play(progress_bar=False)
        self.assertEqual(results.ranked_names[0], "Defector")

        # If the noise is large enough, cooperator should win
        players = [axelrod.Cooperator(), axelrod.Defector()]
        tournament = axelrod.Tournament(players, turns=20, repetitions=10,
                                        with_morality=False, noise=0.75)
        results = tournament.play(progress_bar=False)
        self.assertEqual(results.ranked_names[0], "Cooperator")


class TestProbEndTournament(unittest.TestCase):
    def test_players_do_not_know_match_length(self):
        """Create two players who should cooperate on last two turns if they
        don't know when those last two turns are.
        """
        p1 = FinalTransformer(['D', 'D'])(axelrod.Cooperator)()
        p2 = FinalTransformer(['D', 'D'])(axelrod.Cooperator)()
        players = [p1, p2]
        tournament = axelrod.ProbEndTournament(players, prob_end=.1,
                                               repetitions=1)
        results = tournament.play(progress_bar=False)
        # Check that both plays always cooperated
        for rating in results.cooperating_rating:
            self.assertEqual(rating, 1)
