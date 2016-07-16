"""Tests for some expected match behaviours"""
import unittest
import axelrod

from hypothesis import given
from hypothesis.strategies import integers
from axelrod.tests.property import strategy_lists

C, D = axelrod.Actions.C, axelrod.Actions.D

deterministic_strategies = [s for s in axelrod.ordinary_strategies
                            if not s().classifier['stochastic']]  # Well behaved strategies

class TestMatchOutcomes(unittest.TestCase):

    @given(strategies=strategy_lists(strategies=deterministic_strategies,
                                     min_size=2, max_size=2),
           turns=integers(min_value=1, max_value=20))
    def test_outcome_repeats(self, strategies, turns):
        """A test that if we repeat 3 matches with deterministic and well
        behaved strategies then we get the same result"""
        players = [s() for s in strategies]
        matches = [axelrod.Match(players, turns) for _ in range(3)]
        self.assertEqual(matches[0].play(), matches[1].play())
        self.assertEqual(matches[1].play(), matches[2].play())
