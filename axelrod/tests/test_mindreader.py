"""Test for the mindreader strategy."""

import axelrod

from test_player import TestPlayer


class TestMindReader(TestPlayer):

    name = "Mind Reader"
    player = axelrod.MindReader
    stochastic = False

    def test_strategy(self):
        """
        Will defect against nice strategies
        """
        P1 = axelrod.MindReader()
        P2 = axelrod.Cooperator()
        self.assertEqual(P1.strategy(P2), 'D')
 
    def test_vs_defect(self):
        """
        Will defect against pure defecting strategies
        """
        P1 = axelrod.MindReader()
        P2 = axelrod.Defector()
        self.assertEqual(P1.strategy(P2), 'D')

    def test_vs_grudger(self):
        """
        Will keep nasty strategies happy if it can
        """
        P1 = axelrod.MindReader()
        P2 = axelrod.Grudger()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_vs_tit_for_tat(self):
        """
        Will keep nasty strategies happy if it can
        """
        P1 = axelrod.MindReader()
        P2 = axelrod.Grudger()
        self.assertEqual(P1.strategy(P2), 'C')
 
    def test_simulate_matches(self):
        """
        Simulates a number of matches
        """
        P1 = axelrod.MindReader()
        P2 = axelrod.Grudger()
        P1.simulate_match(P2, 'C', 4)
        self.assertEqual(P2.history, ['C', 'C', 'C', 'C'])
 
    def test_history_is_same(self):
        """
        Checks that the history is not altered by the player
        """
        P1 = axelrod.MindReader()
        P2 = axelrod.Grudger()
        P1.history = ['C', 'C']
        P2.history = ['C', 'D']
        P1.strategy(P2)
        self.assertEqual(P1.history, ['C', 'C'])
        self.assertEqual(P2.history, ['C', 'D'])

    def test_vs_geller(self):
        """Ensures that a recursion error does not occour """
        P1 = axelrod.MindReader()
        P2 = axelrod.Geller()
        P1.strategy(P2)
        P2.strategy(P1)
        
    def tests_protected_mind_reader(self):
        """Ensures that no other player can alter its strategy """

        P1 = axelrod.ProtectedMindReader()
        P2 = axelrod.MindController()
        P3 = axelrod.Cooperator()
        P2.strategy(P1)
        self.assertEqual(P1.strategy(P3), 'D')

    def test_init(self):
        """Tests for init method """
        P1 = axelrod.MindReader()
        self.assertEqual(P1.history, [])

    def test_reset(self):
        """Tests to see if the class is reset correctly """
        P1 = axelrod.MindReader()
        P1.history = ['C', 'D', 'D', 'D']
        P1.reset()
        self.assertEqual(P1.history, [])
