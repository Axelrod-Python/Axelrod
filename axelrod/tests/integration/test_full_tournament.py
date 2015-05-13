import unittest
import axelrod


class TestFullTournament(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()

    def test_full_tournament(self):
        """A test to check that tournament runs with all non cheating strategies."""
        strategies = [strategy() for strategy in axelrod.basic_strategies + axelrod.ordinary_strategies]
        tournament = axelrod.Tournament(name='test', players=strategies, game=self.game, turns=500, repetitions=2)
        output_of_tournament = tournament.play().results
        self.assertEqual(type(output_of_tournament), list)
        self.assertEqual(len(output_of_tournament), len(strategies))
