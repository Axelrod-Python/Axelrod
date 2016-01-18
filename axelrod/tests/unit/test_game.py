import unittest
from hypothesis import given
from hypothesis.strategies import integers, tuples

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

    @given(r=integers(), p=integers(), s=integers(), t=integers())
    def test_property_init(self, r, p, s, t):
        """Use the hypothesis library to test init"""
        expected_scores = {(C, D): (s, t), (D, C): (t, s),
                           (D, D): (p, p), (C, C): (r, r)}
        game = axelrod.Game(r, s, t, p)
        self.assertEqual(game.scores, expected_scores)

    @given(r=integers(), p=integers(), s=integers(), t=integers())
    def test_property_RPST(self, r, p, s, t):
        """Use the hypothesis library to test RPST"""
        game = axelrod.Game(r, s, t, p)
        self.assertEqual(game.RPST(), (r, p, s, t))

    @given(r=integers(), p=integers(), s=integers(), t=integers())
    def test_property_score(self, r, p, s, t):
        """Use the hypothesis library to test score"""
        game = axelrod.Game(r, s, t, p)
        self.assertEqual(game.score((C, C)), (r, r))
        self.assertEqual(game.score((D, D)), (p, p))
        self.assertEqual(game.score((C, D)), (s, t))
        self.assertEqual(game.score((D, C)), (t, s))
