import unittest
import axelrod
from axelrod import MockPlayer, update_history
from axelrod.tests.strategies.test_player import TestOpponent

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestMockPlayer(unittest.TestCase):

    def test_init(self):
        actions = [C, C, D]
        history = [C, C, C]
        state_dist = {(C, C): 2, (D, C): 1}
        m = MockPlayer(actions=actions, history=history, state_dist=state_dist)
        self.assertEqual(m.history, [C, C, C])
        self.assertEqual(m.state_distribution, state_dist)

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

    def test_history(self):
        t = TestOpponent()
        m1 = MockPlayer(actions=[C], history=[C] * 10)
        self.assertEqual(m1.actions.__next__(), C)
        self.assertEqual(m1.history, [C] * 10)
        self.assertEqual(m1.cooperations, 10)
        self.assertEqual(m1.defections, 0)
        self.assertEqual(m1.strategy(t), C)

        m2 = MockPlayer(actions=[D], history=[D] * 10)
        self.assertEqual(m2.actions.__next__(), D)
        self.assertEqual(m2.history, [D] * 10)
        self.assertEqual(m2.cooperations, 0)
        self.assertEqual(m2.defections, 10)
        self.assertEqual(m2.strategy(t), D)


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
