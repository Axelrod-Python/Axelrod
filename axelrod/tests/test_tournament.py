"""
Tests for the main module.
"""
import unittest
import axelrod
import random

class TestInitialisation(unittest.TestCase):

    def test_initialisation(self):
        """
        Test that can initiate a tournament
        """
        P1 = axelrod.Defector()
        P2 = axelrod.Defector()
        P3 = axelrod.Defector()
        tournament = axelrod.Axelrod(P1, P2, P3)
        self.assertEqual([str(s) for s in tournament.players], ['Defector', 'Defector', 'Defector'])


class TestRoundRobin(unittest.TestCase):

    def test_round_robin_defector_v_cooperator(self):
        """
        Test round robin: the defector viciously punishes the cooperator
        """
        P1 = axelrod.Defector()
        P2 = axelrod.Cooperator()
        tournament = axelrod.Axelrod(P1, P2)
        tournament.round_robin(turns=10)
        self.assertEqual([(str(player), player.score) for player in sorted(tournament.players, key=lambda x: x.score)], [('Defector', 0), ('Cooperator', 50)])

    def test_round_robin_defector_v_titfortat(self):
        """
        Test round robin: the defector does well against tit for tat
        """
        P1 = axelrod.Defector()
        P2 = axelrod.TitForTat()
        tournament = axelrod.Axelrod(P1, P2)
        tournament.round_robin(turns=10)
        self.assertEqual([(str(player), player.score) for player in sorted(tournament.players, key=lambda x: x.score)], [('Defector', 36), ('Tit For Tat', 41)])

    def test_round_robin_cooperator_v_titfortat(self):
        """
        Test round robin: the cooperator does very well WITH tit for tat
        """
        P1 = axelrod.Cooperator()
        P2 = axelrod.TitForTat()
        tournament = axelrod.Axelrod(P1, P2)
        tournament.round_robin(turns=10)
        self.assertEqual([(str(player), player.score) for player in sorted(tournament.players, key=lambda x: x.score)], [('Cooperator', 20), ('Tit For Tat', 20)])

    def test_round_robin_cooperator_v_titfortat_v_defector(self):
        """
        Test round robin: the defector seems to dominate in this small population
        """
        P1 = axelrod.Cooperator()
        P2 = axelrod.TitForTat()
        P3 = axelrod.Defector()
        tournament = axelrod.Axelrod(P1, P2, P3)
        tournament.round_robin(turns=10)
        self.assertEqual([(str(player), player.score) for player in sorted(tournament.players, key=lambda x: x.score)], [('Defector', 36), ('Tit For Tat', 61), ('Cooperator', 70)])

    def test_round_robin_cooperator_v_titfortat_v_defector_v_grudger(self):
        """
        Test round robin: tit for tat does a lot better this time around
        """
        P1 = axelrod.Cooperator()
        P2 = axelrod.TitForTat()
        P3 = axelrod.Defector()
        P4 = axelrod.Grudger()
        tournament = axelrod.Axelrod(P1, P2, P3, P4)
        tournament.round_robin(turns=10)
        self.assertEqual([(str(player), player.score) for player in sorted(tournament.players, key=lambda x: x.score)], [('Defector', 72), ('Tit For Tat', 81), ('Grudger', 81), ('Cooperator', 90)])

    def test_round_robin_cooperator_v_titfortat_v_defector_v_grudger_v_go_by_majority(self):
        """
        Test round robin: Tit for tat now wins
        """
        P1 = axelrod.Cooperator()
        P2 = axelrod.TitForTat()
        P3 = axelrod.Defector()
        P4 = axelrod.Grudger()
        P5 = axelrod.GoByMajority()
        tournament = axelrod.Axelrod(P1, P2, P3, P4, P5)
        tournament.round_robin(turns=10)
        self.assertEqual([(str(player), player.score) for player in sorted(tournament.players, key=lambda x: x.score)], [('Tit For Tat', 101), ('Grudger', 101), ('Go By Majority', 101), ('Defector', 108), ('Cooperator', 110)])

class Tournament(unittest.TestCase):

    def test_full_tournament(self):
        """
        A test to check that tournament runs with all non cheating strategies
        """
        strategies = [strategy() for strategy in axelrod.strategies]
        tournament = axelrod.Axelrod(*strategies)
        output_of_tournament = tournament.tournament(turns=500, repetitions=2)
        self.assertEqual(type(output_of_tournament), dict)
        self.assertEqual(len(output_of_tournament), len(strategies))


    def test_tournament(self):
        """
        Test tournament
        """
        P1 = axelrod.Cooperator()
        P2 = axelrod.TitForTat()
        P3 = axelrod.Defector()
        P4 = axelrod.Grudger()
        P5 = axelrod.GoByMajority()
        tournament = axelrod.Axelrod(P1, P2, P3, P4, P5)
        results = tournament.tournament(turns=200, repetitions=5)
        self.assertEqual(sorted([(str(player), results[player]) for player in sorted(results.keys())]), sorted([
       ('Tit For Tat', [2001, 2001, 2001, 2001, 2001]),
       ('Cooperator', [2200, 2200, 2200, 2200, 2200]),
       ('Defector', [2388, 2388, 2388, 2388, 2388]),
       ('Grudger', [2001, 2001, 2001, 2001, 2001]),
       ('Go By Majority', [2001, 2001, 2001, 2001, 2001])]))

    def test_calculate_score_for_mix(self):
        """
        Test that scores are calculated correctly
        """
        P1 = axelrod.Defector()
        P1.history = ['C', 'C', 'D']
        P2 = axelrod.Defector()
        P2.history = ['C', 'D', 'D']
        tournament = axelrod.Axelrod(P1, P2)
        self.assertEqual(tournament.calculate_scores(P1, P2), (11, 6))

    def test_calculate_score_for_all_cooperate(self):
        """
        Test that scores are calculated correctly
        """
        P1 = axelrod.Player()
        P1.history = ['C', 'C', 'C']
        P2 = axelrod.Player()
        P2.history = ['C', 'C', 'C']
        tournament = axelrod.Axelrod(P1, P2)
        self.assertEqual(tournament.calculate_scores(P1, P2), (6, 6))

    def test_calculate_score_for_all_defect(self):
        """
        Test that scores are calculated correctly
        """
        P1 = axelrod.Player()
        P1.history = ['D', 'D', 'D']
        P2 = axelrod.Player()
        P2.history = ['D', 'D', 'D']
        tournament = axelrod.Axelrod(P1, P2)
        self.assertEqual(tournament.calculate_scores(P1, P2), (12, 12))

class TestPlayer(unittest.TestCase):

    def test_initialisation(self):
        """
        Test that can initiate a player
        """
        P1 = axelrod.Player()
        self.assertEqual((P1.history, P1.score), ([], 0))

    def test_play(self):
        """
        Test that play method looks for attribute strategy (which does not exist)
        """
        P1, P2 = axelrod.Player(), axelrod.Player()
        self.assertRaises(AttributeError, P1.play, P2)
        self.assertRaises(AttributeError, P2.play, P1)


if __name__ == '__main__':
    unittest.main()
