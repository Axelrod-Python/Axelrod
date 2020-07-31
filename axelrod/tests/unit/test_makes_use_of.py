"""Tests for makes_use_of."""

import unittest

import axelrod as axl
from axelrod.makes_use_of import makes_use_of


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
