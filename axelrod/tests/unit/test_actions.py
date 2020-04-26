import unittest

import axelrod as axl
from axelrod.action import UnknownActionError, actions_to_str, str_to_actions

C, D = axl.Action.C, axl.Action.D


class TestAction(unittest.TestCase):
    def test_lt(self):
        self.assertLess(C, D)

    def test_repr(self):
        self.assertEqual(repr(C), "C")
        self.assertEqual(repr(D), "D")

    def test_str(self):
        self.assertEqual(str(C), "C")
        self.assertEqual(str(D), "D")

    def test__eq__(self):
        self.assertTrue(C == C)
        self.assertTrue(D == D)
        self.assertFalse(C == D)
        self.assertFalse(D == C)

    def test_total_order(self):
        actions = [C, D, D, C, C, C, D]
        actions.sort()
        self.assertEqual(actions, [C, C, C, C, D, D, D])

    def test_flip(self):
        self.assertEqual(C.flip(), D)
        self.assertEqual(D.flip(), C)

    def test_from_char(self):
        self.assertEqual(axl.Action.from_char("C"), C)
        self.assertEqual(axl.Action.from_char("D"), D)

    def test_from_char_error(self):
        self.assertRaises(UnknownActionError, axl.Action.from_char, "")
        self.assertRaises(UnknownActionError, axl.Action.from_char, "c")
        self.assertRaises(UnknownActionError, axl.Action.from_char, "d")
        self.assertRaises(UnknownActionError, axl.Action.from_char, "A")
        self.assertRaises(UnknownActionError, axl.Action.from_char, "CC")

    def test_str_to_actions(self):
        self.assertEqual(str_to_actions(""), ())
        self.assertEqual(str_to_actions("C"), (C,))
        self.assertEqual(str_to_actions("CDDC"), (C, D, D, C))

    def test_str_to_actions_fails_fast_and_raises_value_error(self):
        self.assertRaises(UnknownActionError, str_to_actions, "Cc")

    def test_actions_to_str(self):
        self.assertEqual(actions_to_str([]), "")
        self.assertEqual(actions_to_str([C]), "C")
        self.assertEqual(actions_to_str([C, D, C]), "CDC")
        self.assertEqual(actions_to_str((C, C, D)), "CCD")

    def test_actions_to_str_with_iterable(self):
        self.assertEqual(actions_to_str(iter([C, D, C])), "CDC")
        generator = (action for action in [C, D, C])
        self.assertEqual(actions_to_str(generator), "CDC")
