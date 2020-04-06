import unittest

import axelrod as axl
from axelrod.tests.property import games

from hypothesis import given, settings
from hypothesis.strategies import integers

C, D = axl.Action.C, axl.Action.D


class TestGame(unittest.TestCase):
    def test_default_scores(self):
        expected_scores = {
            (C, D): (0, 5),
            (D, C): (5, 0),
            (D, D): (1, 1),
            (C, C): (3, 3),
        }
        self.assertEqual(axl.Game().scores, expected_scores)

    def test_default_RPST(self):
        expected_values = (3, 1, 0, 5)
        self.assertEqual(axl.Game().RPST(), expected_values)

    def test_default_score(self):
        game = axl.Game()
        self.assertEqual(game.score((C, C)), (3, 3))
        self.assertEqual(game.score((D, D)), (1, 1))
        self.assertEqual(game.score((C, D)), (0, 5))
        self.assertEqual(game.score((D, C)), (5, 0))

    def test_default_equality(self):
        self.assertEqual(axl.Game(), axl.Game())

    def test_not_default_equality(self):
        self.assertEqual(axl.Game(1, 2, 3, 4), axl.Game(1, 2, 3, 4))
        self.assertNotEqual(axl.Game(1, 2, 3, 4), axl.Game(1, 2, 3, 5))
        self.assertNotEqual(axl.Game(1, 2, 3, 4), axl.Game())

    def test_wrong_class_equality(self):
        self.assertNotEqual(axl.Game(), "wrong class")

    @given(r=integers(), p=integers(), s=integers(), t=integers())
    @settings(max_examples=5)
    def test_random_init(self, r, p, s, t):
        """Test init with random scores using the hypothesis library."""
        expected_scores = {
            (C, D): (s, t),
            (D, C): (t, s),
            (D, D): (p, p),
            (C, C): (r, r),
        }
        game = axl.Game(r, s, t, p)
        self.assertEqual(game.scores, expected_scores)

    @given(r=integers(), p=integers(), s=integers(), t=integers())
    @settings(max_examples=5)
    def test_random_RPST(self, r, p, s, t):
        """Test RPST method with random scores using the hypothesis library."""
        game = axl.Game(r, s, t, p)
        self.assertEqual(game.RPST(), (r, p, s, t))

    @given(r=integers(), p=integers(), s=integers(), t=integers())
    @settings(max_examples=5)
    def test_random_score(self, r, p, s, t):
        """Test score method with random scores using the hypothesis library."""
        game = axl.Game(r, s, t, p)
        self.assertEqual(game.score((C, C)), (r, r))
        self.assertEqual(game.score((D, D)), (p, p))
        self.assertEqual(game.score((C, D)), (s, t))
        self.assertEqual(game.score((D, C)), (t, s))

    @given(game=games())
    @settings(max_examples=5)
    def test_random_repr(self, game):
        """Test repr with random scores using the hypothesis library."""
        expected_repr = "Axelrod game: (R,P,S,T) = {}".format(game.RPST())
        self.assertEqual(expected_repr, game.__repr__())
        self.assertEqual(expected_repr, str(game))
