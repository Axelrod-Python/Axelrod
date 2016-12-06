"""Tests for some expected match behaviours"""
import unittest
import axelrod

from hypothesis import given
from hypothesis.strategies import integers
from axelrod.tests.property import strategy_lists

C, D = axelrod.Actions.C, axelrod.Actions.D

deterministic_strategies = [s for s in axelrod.strategies
                            if not s().classifier['stochastic']]
stochastic_strategies = [s for s in axelrod.strategies
                         if s().classifier['stochastic']]


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

    @given(strategies=strategy_lists(strategies=stochastic_strategies,
                                     min_size=2, max_size=2),
           turns=integers(min_value=1, max_value=20),
           seed=integers(min_value=0, max_value=4294967295))
    def test_outcome_repeats_stochastic(self, strategies, turns, seed):
        """a test to check that if a seed is set stochastic strategies give the
        same result"""
        results = []
        for _ in range(3):
            axelrod.seed(seed)
            players = [s() for s in strategies]
            results.append(axelrod.Match(players, turns).play())

        self.assertEqual(results[0], results[1])
        self.assertEqual(results[1], results[2])

    def test_matches_with_det_player_for_stochastic_classes(self):
        """A test based on a bug found in the cache.

        See: https://github.com/Axelrod-Python/Axelrod/issues/779"""
        p1 = axelrod.MemoryOnePlayer((0, 0, 0, 0))
        p2 = axelrod.MemoryOnePlayer((1, 0, 1, 0))
        p3 = axelrod.MemoryOnePlayer((1, 1, 1, 0))

        m = axelrod.Match((p1, p2), turns=3)
        self.assertEqual(m.play(), [('C', 'C'), ('D', 'C'), ('D', 'D')])

        m = axelrod.Match((p2, p3), turns=3)
        self.assertEqual(m.play(), [('C', 'C'), ('C', 'C'), ('C', 'C')])

        m = axelrod.Match((p1, p3), turns=3)
        self.assertEqual(m.play(), [('C', 'C'), ('D', 'C'), ('D', 'C')])
