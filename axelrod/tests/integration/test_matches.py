"""Tests for some expected match behaviours"""

import unittest

from hypothesis import given, settings
from hypothesis.strategies import integers

import axelrod as axl
from axelrod.tests.property import strategy_lists

C, D = axl.Action.C, axl.Action.D

deterministic_strategies = [
    s
    for s in axl.short_run_time_strategies
    if not axl.Classifiers["stochastic"](s())
]
stochastic_strategies = [
    s
    for s in axl.short_run_time_strategies
    if axl.Classifiers["stochastic"](s())
]


class TestMatchOutcomes(unittest.TestCase):
    @given(
        strategies=strategy_lists(
            strategies=deterministic_strategies, min_size=2, max_size=2
        ),
        turns=integers(min_value=1, max_value=20),
    )
    @settings(max_examples=5)
    def test_outcome_repeats(self, strategies, turns):
        """A test that if we repeat 3 matches with deterministic and well
        behaved strategies then we get the same result"""
        players = [s() for s in strategies]
        matches = [axl.Match(players, turns) for _ in range(3)]
        self.assertEqual(matches[0].play(), matches[1].play())
        self.assertEqual(matches[1].play(), matches[2].play())

    @given(
        strategies=strategy_lists(
            strategies=stochastic_strategies, min_size=2, max_size=2
        ),
        turns=integers(min_value=1, max_value=20),
        seed=integers(min_value=0, max_value=4294967295),
    )
    @settings(max_examples=5, deadline=None)
    def test_outcome_repeats_stochastic(self, strategies, turns, seed):
        """a test to check that if a seed is set stochastic strategies give the
        same result"""
        results = []
        for _ in range(3):
            players = [s() for s in strategies]
            results.append(axl.Match(players, turns=turns, seed=seed).play())

        self.assertEqual(results[0], results[1])
        self.assertEqual(results[1], results[2])

    def test_matches_with_det_player_for_stochastic_classes(self):
        """A test based on a bug found in the cache.

        See: https://github.com/Axelrod-Python/Axelrod/issues/779"""
        p1 = axl.MemoryOnePlayer(four_vector=(0, 0, 0, 0))
        p2 = axl.MemoryOnePlayer(four_vector=(1, 0, 1, 0))
        p3 = axl.MemoryOnePlayer(four_vector=(1, 1, 1, 0))

        m = axl.Match((p1, p2), turns=3)
        self.assertEqual(m.play(), [(C, C), (D, C), (D, D)])

        m = axl.Match((p2, p3), turns=3)
        self.assertEqual(m.play(), [(C, C), (C, C), (C, C)])

        m = axl.Match((p1, p3), turns=3)
        self.assertEqual(m.play(), [(C, C), (D, C), (D, C)])
