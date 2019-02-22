from collections import Counter
import unittest

import axelrod
from axelrod import Action
from axelrod.history import History

C, D = Action.C, Action.D


class TestHistory(unittest.TestCase):
    def test_init(self):
        h1 = History([C, C, D])
        self.assertEqual(list(h1), [C, C, D])
        h1.extend([C, C])
        self.assertEqual(list(h1), [C, C, D, C, C])

    def test_str_list_repr(self):
        h = History()
        h.append(C, D)
        h.append(D, C)
        h.append(C, D)
        self.assertEqual(str(h), "CDC")
        self.assertEqual(list(h), [C, D, C])
        self.assertEqual(repr(h), "[C, D, C]")
        h2 = h.dual()
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

    def test_eq(self):
        h = History([C, D, C])
        with self.assertRaises(TypeError):
            h == 2

    def test_counts(self):
        h1 = History([C, C])
        self.assertEqual(h1.cooperations, 2)
        self.assertEqual(h1.defections, 0)
        h2 = History([D, D])
        self.assertEqual(h2.cooperations, 0)
        self.assertEqual(h2.defections, 2)
        self.assertNotEqual(h1, h2)
        h3 = History([C, C, D, D])
        self.assertEqual(h3.cooperations, 2)
        self.assertEqual(h3.defections, 2)

    def test_dual_history(self):
        player = axelrod.Alternator()
        opponent = axelrod.Cooperator()
        for _ in range(5):
            player.play(opponent)

        self.assertEqual(player.history, [C, D, C, D, C])
        self.assertEqual(player.cooperations, 3)
        self.assertEqual(player.defections, 2)

        new_distribution = Counter()
        for key, val in player.state_distribution.items():
            new_key = (key[0].flip(), key[1])
            new_distribution[new_key] = val

        player.history = player.history.dual()
        self.assertEqual(player.history, [D, C, D, C, D])
        self.assertEqual(player.cooperations, 2)
        self.assertEqual(player.defections, 3)
        self.assertEqual(player.state_distribution, new_distribution)

        # Dual operation is idempotent
        player.history = player.history.dual()
        self.assertEqual(player.history, [C, D, C, D, C])
        self.assertEqual(player.cooperations, 3)
        self.assertEqual(player.defections, 2)
