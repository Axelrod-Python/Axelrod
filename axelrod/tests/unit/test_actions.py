import unittest
from axelrod import Actions, flip_action
from axelrod.actions import str_to_actions, UnknownAction

C, D = Actions.C, Actions.D


class TestAction(unittest.TestCase):

    def test_repr(self):
        self.assertEqual(repr(C), 'C')
        self.assertEqual(repr(D), 'D')

    def test_bool(self):
        self.assertTrue(C)
        self.assertFalse(D)

    def test_flip_action(self):
        self.assertEqual(flip_action(D), C)
        self.assertEqual(flip_action(C), D)

    def test__eq__(self):
        self.assertTrue(C == C)
        self.assertTrue(D == D)
        self.assertFalse(C == D)
        self.assertFalse(D == C)

    def test_error(self):
        self.assertRaises(UnknownAction, flip_action, 'R')

    def test_str_to_actions(self):
        self.assertEqual(str_to_actions(''), ())
        self.assertEqual(str_to_actions('C'), (C, ))
        self.assertEqual(str_to_actions('CDDC'), (C, D, D, C))

    def test_str_to_actions_fails_fast_and_raises_value_error(self):
        self.assertRaises(UnknownAction, str_to_actions, 'Cc')
