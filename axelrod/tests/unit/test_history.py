import unittest
from collections import Counter

import axelrod as axl
from axelrod.history import History, LimitedHistory

C, D = axl.Action.C, axl.Action.D


class TestHistory(unittest.TestCase):
    def test_init(self):
        h1 = History([C, C, D], [C, C, C])
        self.assertEqual(list(h1), [C, C, D])
        h1.extend([C, C], [D, D])
        self.assertEqual(list(h1), [C, C, D, C, C])

    def test_str_list_repr(self):
        h = History()
        h.append(C, D)
        h.append(D, C)
        h.append(C, D)
        self.assertEqual(str(h), "CDC")
        self.assertEqual(list(h), [C, D, C])
        self.assertEqual(repr(h), "[C, D, C]")
        h2 = h.flip_plays()
        self.assertEqual(str(h2), "DCD")

    def test_reset(self):
        h = History()
        h.append(C, D)
        self.assertEqual(len(h), 1)
        self.assertEqual(h.cooperations, 1)
        h.reset()
        self.assertEqual(len(h), 0)
        self.assertEqual(h.cooperations, 0)

    def test_compare(self):
        h = History([C, D, C], [C, C, C])
        self.assertEqual(h, [C, D, C])
        h2 = History([C, D, C], [C, C, C])
        self.assertEqual(h, h2)
        h2.reset()
        self.assertNotEqual(h, h2)

    def test_copy(self):
        h = History([C, D, C], [C, C, C])
        h2 = h.copy()
        self.assertEqual(h, h2)

    def test_eq(self):
        h = History([C, D, C], [C, C, C])
        with self.assertRaises(TypeError):
            h == 2

    def test_counts(self):
        h1 = History([C, C], [C, C])
        self.assertEqual(h1.cooperations, 2)
        self.assertEqual(h1.defections, 0)
        h2 = History([D, D], [C, C])
        self.assertEqual(h2.cooperations, 0)
        self.assertEqual(h2.defections, 2)
        self.assertNotEqual(h1, h2)
        h3 = History([C, C, D, D], [C, C, C, C])
        self.assertEqual(h3.cooperations, 2)
        self.assertEqual(h3.defections, 2)

    def test_flip_plays(self):
        player = axl.Alternator()
        opponent = axl.Cooperator()
        match = axl.Match((player, opponent), turns=5)
        match.play()

        self.assertEqual(player.history, [C, D, C, D, C])
        self.assertEqual(player.cooperations, 3)
        self.assertEqual(player.defections, 2)

        new_distribution = Counter()
        for key, val in player.state_distribution.items():
            new_key = (key[0].flip(), key[1])
            new_distribution[new_key] = val

        flipped_history = player.history.flip_plays()
        self.assertEqual(flipped_history, [D, C, D, C, D])
        self.assertEqual(flipped_history.cooperations, 2)
        self.assertEqual(flipped_history.defections, 3)
        self.assertEqual(flipped_history.state_distribution, new_distribution)

        # Flip operation is idempotent
        flipped_flipped_history = flipped_history.flip_plays()
        self.assertEqual(flipped_flipped_history, [C, D, C, D, C])
        self.assertEqual(flipped_flipped_history.cooperations, 3)
        self.assertEqual(flipped_flipped_history.defections, 2)


def test_coplays():
    plays = (C, C, D)
    coplays = (C, C, C)
    history = History(plays=plays, coplays=coplays)
    assert history.coplays == list(coplays)


class TestLimitedHistory(unittest.TestCase):
    def test_memory_depth(self):
        h = LimitedHistory(memory_depth=3)
        h.append(C, C)
        self.assertEqual(len(h), 1)
        h.append(D, D)
        self.assertEqual(len(h), 2)
        h.append(C, D)
        self.assertEqual(len(h), 3)
        self.assertEqual(h.cooperations, 2)
        self.assertEqual(h.defections, 1)
        self.assertEqual(
            h.state_distribution, Counter({(C, C): 1, (D, D): 1, (C, D): 1})
        )
        h.append(D, C)
        self.assertEqual(len(h), 3)
        self.assertEqual(h._plays, [D, C, D])
        self.assertEqual(h._coplays, [D, D, C])
        self.assertEqual(h.cooperations, 1)
        self.assertEqual(h.defections, 2)
        self.assertEqual(
            h.state_distribution,
            Counter({(D, D): 1, (C, D): 1, (D, C): 1, (C, C): 0}),
        )
