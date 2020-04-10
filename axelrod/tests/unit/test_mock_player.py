import unittest

import axelrod as axl

C, D = axl.Action.C, axl.Action.D


class TestMockPlayer(unittest.TestCase):
    def test_strategy(self):
        for action in [C, D]:
            m = axl.MockPlayer(actions=[action])
            p2 = axl.Player()
            self.assertEqual(action, m.strategy(p2))

        actions = [C, C, D, D, C, C]
        m = axl.MockPlayer(actions=actions)
        p2 = axl.Player()
        for action in actions:
            self.assertEqual(action, m.strategy(p2))
