import unittest
from axelrod import Actions

class TestAction(unittest.TestCase):

    def test_action_values(self):
        self.assertEqual(Actions.C, 'C')
        self.assertEqual(Actions.D, 'D')
        self.assertNotEqual(Actions.D, 'd')
        self.assertNotEqual(Actions.C, 'c')
        self.assertNotEqual(Actions.C, Actions.D)