"""Tests for mind controllers and other wizards."""

import axelrod

from test_player import TestPlayer


class TestMindController(TestPlayer):

    name = 'Mind Controller'
    player = axelrod.MindController
    stochastic = False

    def test_strategy(self):
        """ Will always make opponent cooperate """

        P1 = axelrod.MindController()
        P2 = axelrod.Cooperator()
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P2.strategy(P1), 'C')

    def test_vs_defect(self):
        """ Will force even defector to cooperate """

        P1 = axelrod.MindController()
        P2 = axelrod.Defector()
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P2.strategy(P1), 'C')

    def test_vs_grudger(self):
        """ Will force even Grudger to forget its grudges"""

        P1 = axelrod.MindController()
        P2 = axelrod.Grudger()
        P1.history = ['D','D','D','D',]
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P2.strategy(P1), 'C')

    def test_init(self):
        """Test to make sure parameters are initialised correctly """

        P1 = axelrod.MindController()
        self.assertEqual(P1.history, [])

    def test_reset(self):
        """ test for the reset method """
        P1 = axelrod.MindController()
        P1.history = ['C', 'D', 'D', 'D']
        P1.reset()
        self.assertEqual(P1.history, [])

class TestMindWarper(TestMindController):

    name = "Mind Warper"
    player = axelrod.MindWarper

class TestMindBender(TestMindController):

    name = "Mind Bender"
    player = axelrod.MindBender