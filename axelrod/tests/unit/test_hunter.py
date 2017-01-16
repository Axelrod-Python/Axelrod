"""Tests for the Hunter strategy."""

import random
import unittest

import axelrod

from .test_player import TestPlayer
from axelrod.strategies.hunter import detect_cycle

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestCycleDetection(unittest.TestCase):
    def test_cycles(self):
        history = [C] * 10
        self.assertEqual(detect_cycle(history), (C,))
        self.assertEqual(detect_cycle(history, min_size=2), (C, C))
        history = [C, D] * 10
        self.assertEqual(detect_cycle(history, min_size=2), (C, D))
        self.assertEqual(detect_cycle(history, min_size=3), (C, D, C, D))
        history = [C, D, C] * 10
        self.assertTrue(detect_cycle(history), (C, D, C))
        history = [C, C, D] * 10
        self.assertTrue(detect_cycle(history), (C, C, D))

    def test_noncycles(self):
        history = [C, D, C, C, D, C, C, C, D]
        self.assertEqual(detect_cycle(history), None)
        history = [C, C, D, C, C, D, C, C, C, D, C, C, C, C, D, C, C, C, C, C]
        self.assertEqual(detect_cycle(history), None)


class TestDefectorHunter(TestPlayer):

    name = "Defector Hunter"
    player = axelrod.DefectorHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        for i in range(3):
            self.responses_test([C], [C] * i, [D] * i)
        self.responses_test([D], [C] * 4, [D] * 4)


class TestCooperatorHunter(TestPlayer):

    name = "Cooperator Hunter"
    player = axelrod.CooperatorHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        for i in range(3):
            self.responses_test([C], [C] * i, [C] * i)
        self.responses_test([D], [C] * 4, [C] * 4)


class TestAlternatorHunter(TestPlayer):

    name = "Alternator Hunter"
    player = axelrod.AlternatorHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        self.responses_test([C], [C] * 2, [C, D], attrs={'is_alt': False})
        self.responses_test([C], [C] * 3, [C, D, C], attrs={'is_alt': False})
        self.responses_test([C], [C] * 4, [C, D] * 2, attrs={'is_alt': False})
        self.responses_test([C], [C] * 5, [C, D] * 2 + [C],
                            attrs={'is_alt': False})
        self.responses_test([D], [C] * 6, [C, D] * 3, attrs={'is_alt': True})
        self.responses_test([D], [C] * 7, [C, D] * 3 + [C],
                            attrs={'is_alt': True})

    def test_reset_attr(self):
        p = self.player()
        p.is_alt = True
        p.reset()
        self.assertFalse(p.is_alt)


class TestCycleHunter(TestPlayer):

    name = "Cycle Hunter"
    player = axelrod.CycleHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        player = self.player()
        # Test against cyclers
        for opponent in [axelrod.CyclerCCD(), axelrod.CyclerCCCD(),
                         axelrod.CyclerCCCCCD(), axelrod.Alternator()]:
            player.reset()
            for i in range(30):
                player.play(opponent)
            self.assertEqual(player.history[-1], D)
        # Test against non-cyclers
        axelrod.seed(40)
        for opponent in [axelrod.Random(), axelrod.AntiCycler(),
                         axelrod.Cooperator(), axelrod.Defector()]:
            player.reset()
            for i in range(30):
                player.play(opponent)
            self.assertEqual(player.history[-1], C)

    def test_reset_attr(self):
        p = self.player()
        p.cycle = "CCDDCD"
        p.reset()
        self.assertEqual(p.cycle, None)


class TestEventualCycleHunter(TestPlayer):

    name = "Eventual Cycle Hunter"
    player = axelrod.EventualCycleHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        player = self.player()
        # Test against cyclers
        for opponent in [axelrod.CyclerCCD(), axelrod.CyclerCCCD(),
                         axelrod.CyclerCCCCCD(), axelrod.Alternator()]:
            player.reset()
            for i in range(50):
                player.play(opponent)
            self.assertEqual(player.history[-1], D)
        # Test against non-cyclers and cooperators
        axelrod.seed(43)
        for opponent in [axelrod.Random(), axelrod.AntiCycler(),
                         axelrod.DoubleCrosser(), axelrod.Cooperator()]:
            player.reset()
            for i in range(50):
                player.play(opponent)
            self.assertEqual(player.history[-1], C)

    def test_reset_attr(self):
        p = self.player()
        p.cycle = "CCDDCD"
        p.reset()
        self.assertEqual(p.cycle, None)


class TestMathConstantHunter(TestPlayer):

    name = "Math Constant Hunter"
    player = axelrod.MathConstantHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.responses_test([D], [C] * 8, [C] * 7 + [D])


class TestRandomHunter(TestPlayer):

    name = "Random Hunter"
    player = axelrod.RandomHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):

        # We should catch the alternator here.
        self.responses_test([D], [C] * 12, [C, D] * 6)

        # It is still possible for this test to fail, but very unlikely.
        history1 = [C] * 100
        history2 = [random.choice([C, D]) for i in range(100)]
        self.responses_test(D, history1, history2)

        history1 = [D] * 100
        history2 = [random.choice([C, D]) for i in range(100)]
        self.responses_test(D, history1, history2)

    def test_reset(self):
        player = self.player()
        opponent = axelrod.Cooperator()
        for _ in range(100): player.play(opponent)
        self.assertFalse(player.countCC == 0)
        player.reset()
        self.assertTrue(player.countCC == 0)
