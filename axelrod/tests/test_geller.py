"""
Test for the geller strategy
"""
import unittest
import axelrod

class TestGeller(unittest.TestCase):

    name = "Geller"
    player = axelrod.Geller

    def test_will_cooperate_against_someone_who_is_about_to_cooperate(self):
        """
        Check that will cooperate against someone about to cooperate
        """
        P1 = self.player()
        P2 = axelrod.Cooperator()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_will_defect_against_someone_who_is_about_to_defect(self):
        """
        Check that will defect against someone about to defect
        """
        P1 = self.player()
        P2 = axelrod.Defector()
        self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        P1 = self.player()
        self.assertEqual(str(P1), self.name)

class TestGellerCooperator(TestGeller):

    name = "Geller Cooperator"
    player = axelrod.GellerCooperator

    def test_against_self(self):
        P1 = self.player()
        P2 = self.player()
        self.assertEqual(P1.strategy(P2), 'C')

class GellerDefector(TestGeller):

    name = "Geller Defector"
    player = axelrod.GellerDefector

    def test_against_self(self):
        P1 = self.player()
        P2 = self.player()
        self.assertEqual(P1.strategy(P2), 'D')
