import unittest

import axelrod
from axelrod import MockPlayer, update_history
from axelrod.tests.strategies.test_player import TestOpponent

C, D = axelrod.Action.C, axelrod.Action.D


class TestMockPlayer(unittest.TestCase):
    def test_strategy(self):
        for action in [C, D]:
            m = MockPlayer(actions=[action])
            p2 = axelrod.Player()
            self.assertEqual(action, m.strategy(p2))

        actions = [C, C, D, D, C, C]
        m = MockPlayer(actions=actions)
        p2 = axelrod.Player()
        for action in actions:
            self.assertEqual(action, m.strategy(p2))


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
