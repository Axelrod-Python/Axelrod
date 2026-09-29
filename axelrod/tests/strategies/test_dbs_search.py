"""Differential tests against the unchanged recursive DBS search."""

import itertools
import math
import random
import struct
import unittest
from unittest.mock import patch

import axelrod as axl
from axelrod.strategies import dbs

C, D = axl.Action.C, axl.Action.D
OUTCOMES = ((C, C), (C, D), (D, C), (D, D))


def recursive_values(outcome, policy, depth):
    return dbs.minimax_tree_search(
        dbs.DeterministicNode(outcome[0], outcome[1], 0), policy, depth
    )


def recursive_move(outcome, policy, depth_search_tree=5):
    values = recursive_values(outcome, policy, depth_search_tree)
    return (C, D)[values.index(max(values))]


class TestDBSSearchEquivalence(unittest.TestCase):
    def test_exact_values_and_actions(self):
        rng = random.Random(73041)
        policies = list(itertools.product((0, 1), repeat=4))
        policies += [tuple(rng.random() for _ in range(4)) for _ in range(32)]
        policies += [
            (0.5,) * 4,
            (0.1, 0.7, 0.3, 0.9),
            (math.nextafter(0.5, 0), math.nextafter(0.5, 1), 0.0, 1.0),
            (math.nextafter(0.0, 1), math.nextafter(1.0, 0), -0.0, 0.5),
        ]
        for probabilities in policies:
            policy = dict(zip(OUTCOMES, probabilities))
            for depth in (1, 2, 3, 5, 6):
                for outcome in OUTCOMES:
                    with self.subTest(
                        policy=policy, depth=depth, outcome=outcome
                    ):
                        expected = recursive_values(outcome, policy, depth)
                        actual = dbs._root_values(outcome, policy, depth)
                        self.assertEqual(actual, expected)
                        for value, reference in zip(actual, expected):
                            self.assertIs(type(value), type(reference))
                            self.assertEqual(
                                struct.pack(">d", value),
                                struct.pack(">d", reference),
                            )
                        self.assertEqual(
                            dbs.move_gen(outcome, policy, depth),
                            recursive_move(outcome, policy, depth),
                        )

    def test_ties_keep_cooperation(self):
        found_tie = False
        for probabilities in itertools.product((0, 0.5, 1), repeat=4):
            policy = dict(zip(OUTCOMES, probabilities))
            values = recursive_values((C, C), policy, 3)
            if values[0] == values[1]:
                found_tie = True
                self.assertEqual(dbs.move_gen((C, C), policy, 3), C)
        self.assertTrue(found_tie)

    def test_depth_one_only_needs_the_current_policy_entry(self):
        policy = {(C, C): 0.5}
        self.assertEqual(dbs.move_gen([C, C], policy, 1), D)

    def test_other_depths_keep_original_behavior(self):
        policy = dbs.create_policy(1, 1, 0, 0)
        for depth in (0, -1, 1.5, None, "5"):
            with self.subTest(depth=depth):
                try:
                    recursive_move((C, C), policy, depth)
                except Exception as error:
                    with self.assertRaises(type(error)):
                        dbs.move_gen((C, C), policy, depth)
                else:
                    self.fail(
                        "Expected the original search to reject this depth"
                    )
        for depth in (1.0, 3.0, True):
            self.assertEqual(
                dbs.move_gen((C, C), policy, depth),
                recursive_move((C, C), policy, depth),
            )

    def test_observations_and_learning_states_match(self):
        rng = random.Random(43817)
        observations = [
            (rng.choice((C, D)), rng.choice((C, D))) for _ in range(320)
        ]
        configurations = (
            (0.75, 3, 4, 3, 5),
            (0.75, 1, 1, 0, 5),
            (0.1, 2, 2, 1, 3),
            (0.99, 5, 3, 0, 3),
            (1.0, 3, 4, 3, 2),
        )
        for configuration in configurations:
            reference, optimized = axl.DBS(*configuration), axl.DBS(
                *configuration
            )
            opponent = axl.Cooperator()
            for own, other in observations:
                with patch.object(dbs, "move_gen", recursive_move):
                    expected = reference.strategy(opponent)
                self.assertEqual(optimized.strategy(opponent), expected)
                for name in (
                    "Rd",
                    "Rc",
                    "Pi",
                    "violation_counts",
                    "v",
                    "history_by_cond",
                ):
                    self.assertEqual(
                        getattr(optimized, name), getattr(reference, name)
                    )
                reference.update_history(own, other)
                optimized.update_history(own, other)
                opponent.update_history(other, own)

    def test_adaptive_and_noisy_matches(self):
        for opponent in (axl.Alternator, axl.TitForTat, axl.Random, axl.DBS):
            for noise in (0, 0.1):
                for seed in (7, 42):
                    with self.subTest(
                        opponent=opponent, noise=noise, seed=seed
                    ):

                        def play():
                            return axl.Match(
                                [axl.DBS(), opponent()],
                                turns=100,
                                noise=noise,
                                seed=seed,
                            ).play()

                        with patch.object(dbs, "move_gen", recursive_move):
                            expected = play()
                        self.assertEqual(play(), expected)
