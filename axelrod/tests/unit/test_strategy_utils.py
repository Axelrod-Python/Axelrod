"""Tests for the strategy utils."""

import unittest

import axelrod as axl
from axelrod._strategy_utils import (
    detect_cycle,
    inspect_strategy,
    look_ahead,
    recursive_thue_morse,
    simulate_match,
    thue_morse_generator,
)

from hypothesis import given, settings
from hypothesis.strategies import integers, lists, sampled_from

C, D = axl.Action.C, axl.Action.D


class TestDetectCycle(unittest.TestCase):
    @given(
        cycle=lists(sampled_from([C, D]), min_size=2, max_size=10),
        period=integers(min_value=3, max_value=10),
    )
    @settings(max_examples=5)
    def test_finds_cycle(self, cycle, period):
        history = cycle * period
        detected = detect_cycle(history)
        self.assertIsNotNone(detected)
        self.assertIn("".join(map(str, detected)), "".join(map(str, (cycle))))

    def test_no_cycle(self):
        history = [C, D, C, C]
        self.assertIsNone(detect_cycle(history))

        history = [D, D, C, C, C]
        self.assertIsNone(detect_cycle(history))

    def test_regression_test_can_detect_cycle_that_is_repeated_exactly_once(self):
        self.assertEqual(detect_cycle([C, D, C, D]), (C, D))
        self.assertEqual(detect_cycle([C, D, C, D, C]), (C, D))

    def test_cycle_will_be_at_least_min_size(self):
        self.assertEqual(detect_cycle([C, C, C, C], min_size=1), (C,))
        self.assertEqual(detect_cycle([C, C, C, C], min_size=2), (C, C))

    def test_cycle_that_never_fully_repeats_returns_none(self):
        cycle = [C, D, D]
        to_test = cycle + cycle[:-1]
        self.assertIsNone(detect_cycle(to_test))

    def test_min_size_greater_than_two_times_history_tail_returns_none(self):
        self.assertIsNone(detect_cycle([C, C, C], min_size=2))

    def test_min_size_greater_than_two_times_max_size_has_no_effect(self):
        self.assertEqual(
            detect_cycle([C, C, C, C, C, C, C, C], min_size=2, max_size=3), (C, C)
        )

    def test_cycle_greater_than_max_size_returns_none(self):
        self.assertEqual(detect_cycle([C, C, D] * 2, min_size=1, max_size=3), (C, C, D))
        self.assertIsNone(detect_cycle([C, C, D] * 2, min_size=1, max_size=2))


class TestInspectStrategy(unittest.TestCase):
    def test_strategies_without_countermeasures_return_their_strategy(self):
        tft = axl.TitForTat()
        inspector = axl.Alternator()

        tft.play(inspector)
        self.assertEqual(tft.history, [C])
        self.assertEqual(inspect_strategy(inspector=inspector, opponent=tft), C)
        tft.play(inspector)
        self.assertEqual(tft.history, [C, C])
        self.assertEqual(inspect_strategy(inspector=inspector, opponent=tft), D)
        self.assertEqual(tft.strategy(inspector), D)

    def test_strategies_with_countermeasures_return_their_countermeasures(self):
        d_geller = axl.GellerDefector()
        inspector = axl.Cooperator()
        d_geller.play(inspector)

        self.assertEqual(inspect_strategy(inspector=inspector, opponent=d_geller), D)
        self.assertEqual(d_geller.strategy(inspector), C)


class TestSimulateMatch(unittest.TestCase):
    def test_tft_reacts_to_cooperation(self):
        tft = axl.TitForTat()
        inspector = axl.Alternator()

        simulate_match(inspector, tft, C, 5)
        self.assertEqual(inspector.history, [C, C, C, C, C])
        self.assertEqual(tft.history, [C, C, C, C, C])

    def test_tft_reacts_to_defection(self):
        tft = axl.TitForTat()
        inspector = axl.Alternator()

        simulate_match(inspector, tft, D, 5)
        self.assertEqual(inspector.history, [D, D, D, D, D])
        self.assertEqual(tft.history, [C, D, D, D, D])


class TestLookAhead(unittest.TestCase):
    def setUp(self):
        self.inspector = axl.Player()
        self.game = axl.Game()

    def test_cooperator(self):
        tft = axl.Cooperator()
        # It always makes sense to defect here.
        self.assertEqual(look_ahead(self.inspector, tft, self.game, 1), D)
        self.assertEqual(look_ahead(self.inspector, tft, self.game, 2), D)
        self.assertEqual(look_ahead(self.inspector, tft, self.game, 5), D)

    def test_tit_for_tat(self):
        tft = axl.TitForTat()
        # Cooperation should be chosen if we look ahead further than one move.
        self.assertEqual(look_ahead(self.inspector, tft, self.game, 1), D)
        self.assertEqual(look_ahead(self.inspector, tft, self.game, 2), C)
        self.assertEqual(look_ahead(self.inspector, tft, self.game, 5), C)


class TestRecursiveThueMorse(unittest.TestCase):
    def test_initial_values(self):
        self.assertEqual(recursive_thue_morse(0), 0)
        self.assertEqual(recursive_thue_morse(1), 1)
        self.assertEqual(recursive_thue_morse(2), 1)
        self.assertEqual(recursive_thue_morse(3), 0)
        self.assertEqual(recursive_thue_morse(4), 1)


class TestThueMorseGenerator(unittest.TestCase):
    def test_initial_values(self):
        generator = thue_morse_generator()
        values = [next(generator) for i in range(5)]
        self.assertEqual(values, [0, 1, 1, 0, 1])

    def test_with_offset(self):
        generator = thue_morse_generator(start=2)
        values = [next(generator) for i in range(5)]
        self.assertEqual(values, [1, 0, 1, 0, 0])
