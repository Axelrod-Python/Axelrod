"""Tests for the main tournament class."""

import unittest

import axelrod


class TestTournament(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()

    def test_initialisation(self):
        """Test that can initiate a tournament."""
        P1 = axelrod.Defector()
        P2 = axelrod.Defector()
        P3 = axelrod.Defector()
        tournament = axelrod.Tournament([P1, P2, P3])
        self.assertEqual([str(s) for s in tournament.players], ['Defector', 'Defector', 'Defector'])
        self.assertEqual(tournament.game.score(('C', 'C')), (2, 2))
        self.assertEqual(tournament.turns, 200)
        self.assertEqual(tournament.repetitions, 10)

    def test_full_tournament(self):
        """A test to check that tournament runs with all non cheating strategies."""
        strategies = [strategy() for strategy in axelrod.strategies]
        tournament = axelrod.Tournament(players=strategies, game=self.game, turns=500, repetitions=2)
        output_of_tournament = tournament.play().results
        self.assertEqual(type(output_of_tournament), list)
        self.assertEqual(len(output_of_tournament), len(strategies))

    def test_tournament(self):
        """Test tournament."""

        outcome = [
            ('Tit For Tat', [2001, 2001, 2001, 2001, 2001]),
            ('Cooperator', [2200, 2200, 2200, 2200, 2200]),
            ('Defector', [2388, 2388, 2388, 2388, 2388]),
            ('Grudger', [2001, 2001, 2001, 2001, 2001]),
            ('Go By Majority', [2001, 2001, 2001, 2001, 2001]),
        ]
        outcome.sort()

        P1 = axelrod.Cooperator()
        P2 = axelrod.TitForTat()
        P3 = axelrod.Defector()
        P4 = axelrod.Grudger()
        P5 = axelrod.GoByMajority()
        tournament = axelrod.Tournament(players=[P1, P2, P3, P4, P5], game=self.game, turns=200, repetitions=5)
        names = [str(p) for p in tournament.players]
        results = tournament.play().results
        scores = [[sum([r[i] for r in res]) for i in range(5)] for res in results]
        self.assertEqual(sorted(zip(names, scores)), outcome)


if __name__ == '__main__':
    unittest.main()
