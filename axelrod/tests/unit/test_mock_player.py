import unittest

from axelrod import Action, MockPlayer, Player

C, D = Action.C, Action.D


class TestMockPlayer(unittest.TestCase):
    def test_strategy(self):
        for action in [C, D]:
            m = MockPlayer(actions=[action])
            p2 = Player()
            self.assertEqual(action, m.strategy(p2))

        actions = [C, C, D, D, C, C]
        m = MockPlayer(actions=actions)
        p2 = Player()
        for action in actions:
            self.assertEqual(action, m.strategy(p2))

