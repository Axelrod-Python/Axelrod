"""Tests for makes_use_of."""

import unittest

import axelrod as axl
from axelrod.makes_use_of import (
    class_makes_use_of,
    makes_use_of,
    makes_use_of_variant,
    method_makes_use_of,
)
from axelrod.strategy_transformers import final_sequence


class TestMakesUseOfLengthAndGamePlayer(axl.Player):
    """
    Should have some function that uses length
    """

    def first_function(self):  # pragma: no cover
        x = 1 + 2
        x * 5

    def second_function(self):  # pragma: no cover
        # We put this in the second function to make sure both are checked.
        x = 1 + self.match_attributes["length"]

        # Should only add once.
        y = 2 + self.match_attributes["length"]

        # Should also add game.
        self.match_attributes["game"]


class TestMakesUseOfNothingPlayer(axl.Player):
    """
    Doesn't use match_attributes
    """

    def only_function(self):  # pragma: no cover
        1 + 2 + 3
        print("=6")


class TestMakesUseOf(unittest.TestCase):
    def test_makes_use_of_length_and_game(self):
        self.assertEqual(
            makes_use_of(TestMakesUseOfLengthAndGamePlayer()),
            {"length", "game"},
        )

    def test_makes_use_of_empty(self):
        self.assertEqual(makes_use_of(TestMakesUseOfNothingPlayer()), set())

    def test_untransformed_class(self):
        for player in [axl.Cooperator(), axl.Random()]:
            self.assertEqual(class_makes_use_of(player), set())
            self.assertEqual(makes_use_of_variant(player), set())
            self.assertEqual(method_makes_use_of(player.strategy), set())

    def test_transformer_wrapper(self):
        # Test that the final transformer wrapper makes use of length
        self.assertEqual(method_makes_use_of(final_sequence), {"length"})

    def test_makes_use_of_transformed(self):
        # These players use match length via Final transformer
        for player in [axl.BackStabber(), axl.FirstBySteinAndRapoport()]:
            self.assertEqual(makes_use_of(player), {"length"})
            self.assertEqual(makes_use_of_variant(player), {"length"})
