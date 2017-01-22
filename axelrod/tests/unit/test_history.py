import unittest

from axelrod import Actions
from axelrod.history import HistoryString, HistoryList

C, D = Actions.C, Actions.D


class TestHistoryList(unittest.TestCase):
    def test_init(self):
        h1 = HistoryList([C, C, D])
        h2 = HistoryList("CCD")
        h3 = HistoryList(C + C + D)
        self.assertEqual(h1, h2)
        self.assertEqual(h2, h3)
        self.assertEqual(h3, h1)

    def test_reset(self):
        h = HistoryList()
        h.append(C)
        self.assertEqual(len(h), 1)
        h.reset()
        self.assertEqual(len(h), 0)

    def test_compare(self):
        h = HistoryList([C, D, C])
        self.assertEqual(h, "CDC")
        self.assertEqual(h, C + D + C)
        self.assertEqual(h, [C, D, C])
        h2 = HistoryList([C, D, C])
        self.assertEqual(h, h2)
        h2.reset()
        self.assertNotEqual(h, h2)

    def test_add(self):
        h1 = HistoryList([C, C])
        h2 = HistoryList([D, D])
        h = h1 + h2
        h3 = HistoryList([C, C, D, D])
        self.assertEqual(h, h3)

    def test_counts(self):
        h1 = HistoryList([C, C])
        self.assertEqual(h1.cooperations, 2)
        self.assertEqual(h1.defections, 0)
        h2 = HistoryList([D, D])
        self.assertEqual(h2.cooperations, 0)
        self.assertEqual(h2.defections, 2)
        h3 = HistoryList([C, C, D, D])
        self.assertEqual(h3.cooperations, 2)
        self.assertEqual(h3.defections, 2)

    def test_pop(self):
        h1 = HistoryList([C, D])
        self.assertEqual(len(h1), 2)
        play = h1.pop(-1)
        self.assertEqual(play, D)
        self.assertEqual(len(h1), 1)


class TestHistoryString(unittest.TestCase):
    def test_init(self):
        h1 = HistoryString([C, C, D])
        h2 = HistoryString("CCD")
        h3 = HistoryString(C + C + D)
        self.assertEqual(h1, h2)
        self.assertEqual(h2, h3)
        self.assertEqual(h3, h1)

    def test_reset(self):
        h = HistoryString()
        h.append(C)
        self.assertEqual(len(h), 1)
        h.reset()
        self.assertEqual(len(h), 0)

    def test_compare(self):
        h = HistoryString([C, D, C])
        self.assertEqual(h, "CDC")
        self.assertEqual(h, C + D + C)
        self.assertEqual(h, [C, D, C])
        h2 = HistoryString([C, D, C])
        self.assertEqual(h, h2)
        h2.reset()
        self.assertNotEqual(h, h2)

    def test_add(self):
        h1 = HistoryString([C, C])
        h2 = HistoryString([D, D])
        h = h1 + h2
        h3 = HistoryString([C, C, D, D])
        self.assertEqual(h, h3)

    def test_counts(self):
        h1 = HistoryString([C, C])
        self.assertEqual(h1.cooperations, 2)
        self.assertEqual(h1.defections, 0)
        h2 = HistoryString([D, D])
        self.assertEqual(h2.cooperations, 0)
        self.assertEqual(h2.defections, 2)
        h3 = HistoryString([C, C, D, D])
        self.assertEqual(h3.cooperations, 2)
        self.assertEqual(h3.defections, 2)

    def test_pop(self):
        h1 = HistoryString([C, D])
        self.assertEqual(len(h1), 2)
        play = h1.pop(-1)
        self.assertEqual(play, D)
        self.assertEqual(len(h1), 1)

