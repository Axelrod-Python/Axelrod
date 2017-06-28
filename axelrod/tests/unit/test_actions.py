import unittest
from axelrod import Actions, flip_action
from axelrod.actions import str_to_actions, UnknownAction,  actions_to_str

C, D = Actions.C, Actions.D


class TestAction(unittest.TestCase):

    def test_repr(self):
        self.assertEqual(repr(C), 'C')
        self.assertEqual(repr(D), 'D')

    def test_str(self):
        self.assertEqual(str(C), 'C')
        self.assertEqual(str(D), 'D')

    def test_bool(self):
        self.assertTrue(C)
        self.assertFalse(D)

    def test__eq__(self):
        self.assertTrue(C == C)
        self.assertTrue(D == D)
        self.assertFalse(C == D)
        self.assertFalse(D == C)

    def test_flip(self):
        self.assertEqual(C.flip(), D)
        self.assertEqual(D.flip(), C)

    def test_from_char(self):
        self.assertEqual(Actions.from_char('C'), C)
        self.assertEqual(Actions.from_char('D'), D)

    def test_from_char_error(self):
        self.assertRaises(UnknownAction, Actions.from_char, '')
        self.assertRaises(UnknownAction, Actions.from_char, 'c')
        self.assertRaises(UnknownAction, Actions.from_char, 'd')
        self.assertRaises(UnknownAction, Actions.from_char, 'A')

    def test_flip_action(self):
        self.assertEqual(flip_action(D), C)
        self.assertEqual(flip_action(C), D)

    def test_flip_action_error(self):
        self.assertRaises(UnknownAction, flip_action, 'R')

    def test_str_to_actions(self):
        self.assertEqual(str_to_actions(''), ())
        self.assertEqual(str_to_actions('C'), (C, ))
        self.assertEqual(str_to_actions('CDDC'), (C, D, D, C))

    def test_str_to_actions_fails_fast_and_raises_value_error(self):
        self.assertRaises(UnknownAction, str_to_actions, 'Cc')

    def test_actions_to_str(self):
        self.assertEqual(actions_to_str([]), "")
        self.assertEqual(actions_to_str([C, D, C]), "CDC")
        self.assertEqual(actions_to_str((C, C, D)), "CCD")

    def test_actions_to_str_with_iterable(self):
        self.assertEqual(actions_to_str(iter([C, D, C])), "CDC")
        generator = (action for action in [C, D, C])
        self.assertEqual(actions_to_str(generator), "CDC")
