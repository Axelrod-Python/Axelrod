# -*- coding: utf-8 -*-
import random
import unittest

import axelrod
from axelrod import MoranProcess
from axelrod.moran import fitness_proportionate_selection


class TestMoranProcess(unittest.TestCase):

    def test_fps(self):
        self.assertEqual(fitness_proportionate_selection([0, 0, 1]), 2)
        random.seed(1)
        self.assertEqual(fitness_proportionate_selection([1, 1, 1]), 0)
        self.assertEqual(fitness_proportionate_selection([1, 1, 1]), 2)

    def test_stochastic(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        mp = MoranProcess((p1, p2))
        self.assertFalse(mp._stochastic)
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        mp = MoranProcess((p1, p2), noise=0.05)
        self.assertTrue(mp._stochastic)
        p1, p2 = axelrod.Cooperator(), axelrod.Random()
        mp = MoranProcess((p1, p2))
        self.assertTrue(mp._stochastic)

    def test_exit_condition(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        mp = MoranProcess((p1, p2))
        mp.play()
        self.assertEqual(len(mp), 1)

    def test_two_players(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Defector()
        random.seed(5)
        mp = MoranProcess((p1, p2))
        mp.play()
        self.assertEqual(len(mp), 3)
        self.assertEqual(mp.winner, str(p2))

    def test_three_players(self):
        players = [axelrod.Cooperator(), axelrod.Cooperator(),
                   axelrod.Defector()]
        random.seed(5)
        mp = MoranProcess(players)
        mp.play()
        self.assertEqual(len(mp), 3)
        self.assertEqual(mp.winner, str(axelrod.Cooperator()))

    def test_four_players(self):
        players = [axelrod.Cooperator() for _ in range(3)]
        players.append(axelrod.Defector())
        random.seed(10)
        mp = MoranProcess(players)
        mp.play()
        self.assertEqual(len(mp), 4)
        self.assertEqual(mp.winner, str(axelrod.Cooperator()))

    def test_reset(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Defector()
        random.seed(5)
        mp = MoranProcess((p1, p2))
        mp.play()
        self.assertEqual(len(mp), 3)
        self.assertEqual(len(mp.score_history), 2)
        mp.reset()
        self.assertEqual(len(mp), 1)
        self.assertEqual(mp.winner, None)
        self.assertEqual(mp.score_history, [])
