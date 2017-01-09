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


    def test_sums(self):
        self.assertEqual("CC", C + C)
        self.assertEqual("CD", C + D)
        self.assertEqual("DC", D + C)
        self.assertEqual("DD", D + D)
        self.assertEqual("CDCD", (C + D) * 2)

    def test_flip_action(self):
        self.assertEqual(flip_action(D), C)
        self.assertEqual(flip_action(C), D)

        with self.assertRaises(ValueError):
            flip_action('R')
