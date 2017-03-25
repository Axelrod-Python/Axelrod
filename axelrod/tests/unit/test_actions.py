import unittest
from axelrod import Actions, flip_action
from axelrod.actions import str_to_actions
from types import GeneratorType

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

    def test_str_to_actions_is_generator(self):
        to_test = str_to_actions('c')
        self.assertIsInstance(to_test, GeneratorType)

    def test_str_to_actions_upper_and_lower(self):
        to_test = str_to_actions('cDdC')
        self.assertEqual(next(to_test), Actions.C)
        self.assertEqual(next(to_test), Actions.D)
        self.assertEqual(next(to_test), Actions.D)
        self.assertEqual(next(to_test), Actions.C)
        self.assertRaises(StopIteration, next, to_test)

    def test_str_to_actions_only_raises_value_error_once_offending_letter_is_reached(self):
        to_test = str_to_actions('cAc')
        self.assertEqual(next(to_test), Actions.C)
        self.assertRaises(ValueError, next, to_test)
