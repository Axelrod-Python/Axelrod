import unittest
import axelrod

from axelrod.utils import setup_logging, run_tournaments

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


class TestTournamentManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()
        cls.players = [s() for s in axelrod.demo_strategies]

    def test_tournament_manager(self):
        strategies = [s() for s in axelrod.demo_strategies]
        tm = axelrod.TournamentManager("./", False, save_cache=False)
        tm.add_tournament("test", strategies, repetitions=2, turns=10,
                          noise=0.05)
        tm.run_tournaments()

        strategies = [s() for s in axelrod.basic_strategies]
        tm = axelrod.TournamentManager("./", False, load_cache=False,
                                       save_cache=True)
        tm.add_tournament("test", strategies, repetitions=2, turns=10, noise=0.)
        tm.run_tournaments()

        tm = axelrod.TournamentManager("./", False, load_cache=True,
                                       save_cache=True)
        tm.add_tournament("test", strategies, repetitions=2, turns=10, noise=0.)
        tm.run_tournaments()

    def test_utils(self):
        setup_logging(logging_destination="none")
        run_tournaments(cache_file='./cache.txt',
                    output_directory='./',
                    repetitions=2,
                    turns=10,
                    processes=None,
                    no_ecological=False,
                    rebuild_cache=False,
                    exclude_combined=True,
                    exclude_basic=False,
                    exclude_cheating=True,
                    exclude_ordinary=True,
                    noise=0)
