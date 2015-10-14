import unittest

import axelrod

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGame(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()

    def test_init(self):
        expected_scores = {(C, D): (0, 5), (D, C): (5, 0),
                           (D, D): (1, 1), (C, C): (3, 3)}
        self.assertEqual(self.game.scores, expected_scores)

    def test_RPST(self):
        expected_values = (3, 1, 0, 5)
        self.assertEqual(self.game.RPST(), expected_values)

    def test_score(self):
        self.assertEqual(self.game.score((C, C)), (3, 3))
        self.assertEqual(self.game.score((D, D)), (1, 1))
        self.assertEqual(self.game.score((C, D)), (0, 5))
        self.assertEqual(self.game.score((D, C)), (5, 0))
