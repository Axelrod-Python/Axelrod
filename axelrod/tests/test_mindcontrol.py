"""
Test for the mindcontrol strategy
"""
import unittest
import axelrod

class TestMindControl(unittest.TestCase):

    def test_vs_cooperator(self):
        """ Will always make opponent cooperate """

        P1 = axelrod.MindControl()
        P2 = axelrod.Cooperator()
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P2.strategy(P1), 'C')

    def test_vs_defect(self):
        """ Will force even defector to cooperate """

        P1 = axelrod.MindControl()
        P2 = axelrod.Defector()
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P2.strategy(P1), 'C')

    def test_vs_grudger(self):
        """ Will force even Grudger to forget its grudges"""

        P1 = axelrod.MindControl()
        P2 = axelrod.Grudger()
        P1.history = ['D','D','D','D',]
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P2.strategy(P1), 'C')
        
    def test_string(self):
        """Tests that the string is correctly displayed"""

        P1 = axelrod.MindControl()
        self.assertEqual(str(P1), 'Mind Control')
