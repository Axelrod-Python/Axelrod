import unittest
from axelrod import Actions, reverse_action

class TestAction(unittest.TestCase):

    def test_action_values(self):
        self.assertEqual(Actions.C, 'C')
        self.assertEqual(Actions.D, 'D')
        self.assertNotEqual(Actions.D, 'd')
        self.assertNotEqual(Actions.C, 'c')
        self.assertNotEqual(Actions.C, Actions.D)


    def test_reverse_action(self):
        self.assertEqual(reverse_action(Actions.D), Actions.C)
        self.assertEqual(reverse_action(Actions.C), Actions.D)

        with self.assertRaises(ValueError):
            reverse_action('R')