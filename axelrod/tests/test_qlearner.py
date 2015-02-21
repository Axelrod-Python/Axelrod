"""
Test for the qlearner strategy
"""
import unittest
import axelrod
import random

class TestRiskyQLearner(unittest.TestCase):

    def test_qs_update(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.RiskyQLearner()
        p2 = axelrod.Cooperator()
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Qs, {'': {'C': 0, 'D': -0.9}, '0.0': {'C': 0, 'D': 0}})
        self.assertEqual(p1.Vs, {'': 0, '0.0': 0})

        play_1,play_2 = p1.strategy(p2),p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Qs,{'': {'C': 0, 'D': -0.9}, '0.0': {'C': 0.9, 'D': 0}, 'C1.0': {'C': 0, 'D': 0}})
        self.assertEqual(p1.Vs,{'': 0, '0.0': 0.9, 'C1.0': 0})

    def test_choose_best_strategy(self):
        """
        Tests that it chooses the best strategy
        """
        random.seed(5)
        p1 = axelrod.RiskyQLearner()
        p1.state = 'CCDC'
        p1.Qs = {'': {'C': 0, 'D': 0}, 'CCDC': {'C': 2, 'D': 6}}
        p2 = axelrod.Cooperator()
        self.assertEqual(p1.strategy(p2), 'C')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
