import unittest

from axelrod import Action
from axelrod.history import History

C, D = Action.C, Action.D


class TestHistory(unittest.TestCase):
    def test_init(self):
        h1 = History([C, C, D])
        self.assertEqual(list(h1), [C, C, D])
        h1.extend([C, C])
        self.assertEqual(list(h1), [C, C, D, C, C])

    def test_reset(self):
        h = History()
        h.append(C)
        self.assertEqual(len(h), 1)
        self.assertEqual(h.cooperations, 1)
        h.reset()
        self.assertEqual(len(h), 0)
        self.assertEqual(h.cooperations, 0)

    def test_compare(self):
        h = History([C, D, C])
        self.assertEqual(h, [C, D, C])
        h2 = History([C, D, C])
        self.assertEqual(h, h2)
        h2.reset()
        self.assertNotEqual(h, h2)

    def test_copy(self):
        h = History([C, D, C])
        h2 = h.copy()
        self.assertEqual(h, h2)

    def test_add(self):
        h1 = History([C, C])
        h2 = History([D, D])
        h = h1 + h2
        h3 = History([C, C, D, D])
        self.assertEqual(h, h3)

    def test_counts(self):
        h1 = History([C, C])
        self.assertEqual(h1.cooperations, 2)
        self.assertEqual(h1.defections, 0)
        h2 = History([D, D])
        self.assertEqual(h2.cooperations, 0)
        self.assertEqual(h2.defections, 2)
        h3 = History([C, C, D, D])
        self.assertEqual(h3.cooperations, 2)
        self.assertEqual(h3.defections, 2)

    def test_pop(self):
        h1 = History([C, D])
        self.assertEqual(len(h1), 2)
        play = h1.pop(-1)
        self.assertEqual(play, D)
        self.assertEqual(len(h1), 1)



