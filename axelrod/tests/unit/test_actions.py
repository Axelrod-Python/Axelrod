import unittest
from axelrod import Actions, flip_action


C, D = Actions.C, Actions.D


class TestAction(unittest.TestCase):

    def test_action_values(self):
        self.assertEqual(C, 'C')
        self.assertEqual(D, 'D')
        self.assertNotEqual(D, 'd')
        self.assertNotEqual(C, 'c')
        self.assertNotEqual(C, D)

    def test_flip_action(self):
        self.assertEqual(flip_action(D), C)
        self.assertEqual(flip_action(C), D)

        with self.assertRaises(ValueError):
            flip_action('R')
