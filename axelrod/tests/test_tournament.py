import unittest
import axelrod

class TestTournament(unittest.TestCase):

    def setUp(self):
        pass

    def test_initialisation(self):
        """
        Test that can initiate a tournament
        """
        P1 = axelrod.Defector()
        P2 = axelrod.Defector()
        P3 = axelrod.Defector()
        tournament = axelrod.Axelrod(P1, P2, P3)
        self.assertEqual([str(s) for s in tournament.players], ['Defector', 'Defector', 'Defector'])

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

if __name__ == '__main__':
    unittest.main()
