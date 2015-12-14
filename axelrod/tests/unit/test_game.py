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

    @given(tuples(integers(), integers(), integers(), integers()))
    def test_property_RPST(self, rpst):
        """Use the hypothesis library to test properties using the hypothesis
        library"""
        r, s, t, p = rpst
        game = axelrod.Game(r, s, t, p)
        self.assertEqual(game.RPST(), (r, p, s, t))

    @given(tuples(integers(), integers(), integers(), integers()))
    def test_property_score(self, rpst):
        """Use the hypothesis library to test properties using the hypothesis
        library"""
        r, s, t, p = rpst
        game = axelrod.Game(r, s, t, p)
        self.assertEqual(game.score((C, C)), (r, r))
        self.assertEqual(game.score((D, D)), (p, p))
        self.assertEqual(game.score((C, D)), (s, t))
        self.assertEqual(game.score((D, C)), (t, s))
