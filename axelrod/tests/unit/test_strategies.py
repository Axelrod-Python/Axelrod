"""Test for the random strategy."""

import unittest

import axelrod


class TestStrategies(unittest.TestCase):

    def test_strategy_list(self):
        self.assertTrue(hasattr(axelrod, "strategies"))
        self.assertTrue(hasattr(axelrod, "basic_strategies"))
        self.assertTrue(hasattr(axelrod, "ordinary_strategies"))
        self.assertTrue(hasattr(axelrod, "cheating_strategies"))

    def test_lists_not_empty(self):
        self.assertTrue(len(axelrod.strategies) > 0)
        self.assertTrue(len(axelrod.basic_strategies) > 0)
        self.assertTrue(len(axelrod.ordinary_strategies) > 0)
        self.assertTrue(len(axelrod.cheating_strategies) > 0)

    def test_meta_inclusion(self):
        self.assertTrue(axelrod.MetaMajority in axelrod.strategies)


class TestFilters(unittest.TestCase):

    def test_is_basic(self):
        self.assertTrue(axelrod.is_basic(axelrod.Cooperator))
        self.assertTrue(axelrod.is_basic(axelrod.TitForTat))
        self.assertFalse(axelrod.is_basic(axelrod.MindWarper))


    def test_is_cheater(self):
        self.assertFalse(axelrod.is_cheater(axelrod.Cooperator))
        self.assertFalse(axelrod.is_cheater(axelrod.TitForTat))
        self.assertTrue(axelrod.is_cheater(axelrod.MindWarper))
