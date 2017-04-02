import unittest
from axelrod import Actions, flip_action
from axelrod.actions import str_to_actions

C, D = Actions.C, Actions.D


class TestAction(unittest.TestCase):

    def test_action_values(self):
        self.assertEqual(C, 'C')
        self.assertEqual(D, 'D')
        self.assertNotEqual(D, 'd')
        self.assertNotEqual(C, 'c')
        self.assertNotEqual(D, 0)
        self.assertNotEqual(C, 1)
        self.assertNotEqual(C, D)

    def test_flip_action(self):
        self.assertEqual(flip_action(D), C)
        self.assertEqual(flip_action(C), D)

    def test_error(self):
        self.assertRaises(ValueError, flip_action, 'R')

    def test_str_to_actions(self):
        self.assertEqual(str_to_actions('C'), (C, ))
        self.assertEqual(str_to_actions('CDDC'), (C, D, D, C))

    def test_str_to_actions_fails_fast_and_raises_value_error(self):
        self.assertRaises(ValueError, str_to_actions, 'Cc')
