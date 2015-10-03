"""Tests for mind controllers and other wizards."""

import axelrod

from .test_player import TestPlayer

C, D = 'C', 'D'


class TestMindController(TestPlayer):

    name = 'Mind Controller'
    player = axelrod.MindController
    expected_classifier = {
        'memory_depth': -10,
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': True,  # Finds out what opponent will do
        'manipulates_state': False
    }

    def test_strategy(self):
        """ Will always make opponent cooperate """

        P1 = axelrod.MindController()
        P2 = axelrod.Cooperator()
        self.assertEqual(P1.strategy(P2), D)
        self.assertEqual(P2.strategy(P1), C)

    def test_vs_defect(self):
        """ Will force even defector to cooperate """

        P1 = axelrod.MindController()
        P2 = axelrod.Defector()
        self.assertEqual(P1.strategy(P2), D)
        self.assertEqual(P2.strategy(P1), C)

    def test_vs_grudger(self):
        """ Will force even Grudger to forget its grudges"""

        P1 = axelrod.MindController()
        P2 = axelrod.Grudger()
        P1.history = [D, D, D, D]
        self.assertEqual(P1.strategy(P2), D)
        self.assertEqual(P2.strategy(P1), C)


class TestMindWarper(TestMindController):

    name = "Mind Warper"
    player = axelrod.MindWarper
    expected_classifier = {
        'memory_depth': -10,
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': True,  # Finds out what opponent will do
        'manipulates_state': False
    }

class TestMindBender(TestMindController):

    name = "Mind Bender"
    player = axelrod.MindBender
    expected_classifier = {
        'memory_depth': -10,
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': True,  # Finds out what opponent will do
        'manipulates_state': False
    }
