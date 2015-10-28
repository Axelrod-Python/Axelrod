import unittest
from axelrod import Actions, flip_action

class TestAction(unittest.TestCase):

    def test_action_values(self):
        self.assertEqual(Actions.C, 'C')
        self.assertEqual(Actions.D, 'D')
        self.assertNotEqual(Actions.D, 'd')
        self.assertNotEqual(Actions.C, 'c')
        self.assertNotEqual(Actions.C, Actions.D)


    def test_flip_action(self):
        self.assertEqual(flip_action(Actions.D), Actions.C)
        self.assertEqual(flip_action(Actions.C), Actions.D)

        with self.assertRaises(ValueError):
            flip_action('R')