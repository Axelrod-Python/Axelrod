"""
Test for the average_copier strategy
"""
import unittest
import axelrod
import random

class TestAverageCopier(unittest.TestCase):

    def test_qs_update(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.QLearner()
        p2 = axelrod.Cooperator()
        play_1,play_2 = p1.strategy(p2),p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Qs,{'': {'C': 0, 'D': 5.4}})
        self.assertEqual(p1.Vs,{'': 5.4})

        play_1,play_2 = p1.strategy(p2),p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Qs,{'': {'C': 0, 'D': 9.54}, 'C': {'C': 0, 'D': 0}})
        self.assertEqual(p1.Vs,{'': 9.54, 'C': 0})

    def test_choose_best_strategy(self):
        """
        Tests that it chooses the best strategy
        """
        random.seed(5)
        p1 = axelrod.QLearner()
        p1.state = 'CCDC'
        p1.Qs = {'CCDC':{'C':2, 'D':6}}
        p2 = axelrod.Cooperator()
        self.assertEqual(p1.strategy(p2),'D')
        self.assertEqual(p1.strategy(p2),'D')
        self.assertEqual(p1.strategy(p2),'D')
        self.assertEqual(p1.strategy(p2),'D')
        self.assertEqual(p1.strategy(p2),'D')
        self.assertEqual(p1.strategy(p2),'D')
