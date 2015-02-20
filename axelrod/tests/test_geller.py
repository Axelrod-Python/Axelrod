"""
Test for the geller strategy
"""
import unittest
import axelrod

class TestGrudger(unittest.TestCase):

    def test_will_cooperate_against_someone_who_is_about_to_cooperate(self):
        """
        Check that will cooperate against someone about to cooperate
        """
        P1 = axelrod.Geller()
        P2 = axelrod.Cooperator()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_will_defect_against_someone_who_is_about_to_defect(self):
        """
        Check that will defect against someone about to defect
        """
        P1 = axelrod.Geller()
        P2 = axelrod.Defector()
        self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        P1 = axelrod.Geller()
        self.assertEqual(str(P1), 'Geller')
