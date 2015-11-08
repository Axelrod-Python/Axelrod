import unittest
import axelrod

from axelrod import MockPlayer, simulate_play, update_history
from axelrod.tests.unit.test_player import TestOpponent

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestMockPlayer(unittest.TestCase):

    def test_strategy(self):
        for move in [C, D]:
            m = MockPlayer(axelrod.Player(), move)
            p2 = axelrod.Player()
            self.assertEqual(move, m.strategy(p2))

    def test_cloning(self):
        p1 = axelrod.Cooperator()
        p2 = axelrod.Defector()
        moves = 10
        for i in range(moves):
            p1.play(p2)
        m1 = MockPlayer(p1, C)
        m2 = MockPlayer(p2, D)
        self.assertEqual(m1.move, C)
        self.assertEqual(m1.history, p1.history)
        self.assertEqual(m1.cooperations, p1.cooperations)
        self.assertEqual(m1.defections, p1.defections)
        self.assertEqual(m2.move, D)
        self.assertEqual(m2.history, p2.history)
        self.assertEqual(m2.cooperations, p2.cooperations)
        self.assertEqual(m2.defections, p2.defections)


class TestUpdateHistories(unittest.TestCase):

    def test_various(self):
        p1 = TestOpponent()
        p2 = TestOpponent()
        update_history(p1, C)
        update_history(p2, C)
        self.assertEqual(p1.history, [C])
        self.assertEqual(p2.history, [C])
        self.assertEqual(p1.cooperations, 1)
        self.assertEqual(p2.cooperations, 1)
        self.assertEqual(p1.defections, 0)
        self.assertEqual(p2.defections, 0)

        update_history(p1, D)
        update_history(p2, D)
        self.assertEqual(p1.history, [C, D])
        self.assertEqual(p2.history, [C, D])
        self.assertEqual(p1.cooperations, 1)
        self.assertEqual(p2.cooperations, 1)
        self.assertEqual(p1.defections, 1)
        self.assertEqual(p2.defections, 1)


class TestSimulatePlay(unittest.TestCase):

    def test_various(self):
        p1 = TestOpponent()
        p2 = TestOpponent()
        self.assertEqual(simulate_play(p1, p2), (C, C))
        self.assertEqual(p1.cooperations, 1)
        self.assertEqual(p2.cooperations, 1)
        self.assertEqual(p1.defections, 0)
        self.assertEqual(p2.defections, 0)

        for h1 in [C, D]:
            for h2 in [C, D]:
                self.assertEqual(simulate_play(p1, p2, h1, h2), (h1, h2))
        self.assertEqual(p1.cooperations, 3)
        self.assertEqual(p2.cooperations, 3)
        self.assertEqual(p1.defections, 2)
        self.assertEqual(p2.defections, 2)

    def test_various2(self):
        p1 = axelrod.Cooperator()
        p2 = axelrod.Defector()
        self.assertEqual(simulate_play(p1, p2), (C, D))
        self.assertEqual(p1.cooperations, 1)
        self.assertEqual(p2.cooperations, 0)
        self.assertEqual(p1.defections, 0)
        self.assertEqual(p2.defections, 1)

        self.assertEqual(simulate_play(p1, p2), (C, D))
        self.assertEqual(p1.cooperations, 2)
        self.assertEqual(p2.cooperations, 0)
        self.assertEqual(p1.defections, 0)
        self.assertEqual(p2.defections, 2)

        self.assertEqual(p1.history, [C] * 2)
        self.assertEqual(p2.history, [D] * 2)
