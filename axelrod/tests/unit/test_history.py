import unittest

from axelrod import Actions, History

C, D = Actions.C, Actions.D


class TestHistory(unittest.TestCase):
    def test_init(self):
        h1 = History([C, C, D])
        h2 = History("CCD")
        h3 = History(C + C + D)
        self.assertEqual(h1, h2)
        self.assertEqual(h2, h3)
        self.assertEqual(h3, h1)

    def test_reset(self):
        h = History()
        h.append(C)
        self.assertEqual(len(h), 1)
        h.reset()
        self.assertEqual(len(h), 0)

    def test_compare(self):
        h = History([C, D, C])
        self.assertEqual(h, "CDC")
        self.assertEqual(h, C + D + C)
        self.assertEqual(h, [C, D, C])
        h2 = History([C, D, C])
        self.assertEqual(h, h2)
        h2.reset()
        self.assertNotEqual(h, h2)

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
