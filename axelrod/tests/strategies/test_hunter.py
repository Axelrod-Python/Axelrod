"""Tests for the Hunter strategy."""

import unittest

import axelrod as axl
from axelrod import Match
from axelrod.strategies.hunter import detect_cycle

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


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
    player = axl.DefectorHunter
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, D)] * 4 + [(D, D)] * 10
        self.versus_test(opponent=axl.Defector(), expected_actions=actions)

        actions = [(C, C)] * 14
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)


class TestCooperatorHunter(TestPlayer):

    name = "Cooperator Hunter"
    player = axl.CooperatorHunter
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C)] * 4 + [(D, C)] * 10
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        actions = [(C, D)] * 14
        self.versus_test(opponent=axl.Defector(), expected_actions=actions)


class TestAlternatorHunter(TestPlayer):

    name = "Alternator Hunter"
    player = axl.AlternatorHunter
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "inspects_source": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, D)] * 3 + [(D, C), (D, D)] * 5
        self.versus_test(
            opponent=axl.Alternator(),
            expected_actions=actions,
            attrs={"is_alt": True},
        )

        actions = [(C, D)] * 14
        self.versus_test(
            opponent=axl.Defector(),
            expected_actions=actions,
            attrs={"is_alt": False},
        )

    def test_reset_attr(self):
        p = self.player()
        p.is_alt = True
        p.reset()
        self.assertFalse(p.is_alt)


class TestCycleHunter(TestPlayer):

    name = "Cycle Hunter"
    player = axl.CycleHunter
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        player = self.player()
        # Test against cyclers
        for opponent in [
            axl.CyclerCCD(),
            axl.CyclerCCCD(),
            axl.CyclerCCCCCD(),
            axl.Alternator(),
        ]:
            player.reset()
            match = Match((player, opponent), turns=30)
            match.play()
            self.assertEqual(player.history[-1], D)
        # Test against non-cyclers
        for opponent in [
            axl.Random(),
            axl.AntiCycler(),
            axl.Cooperator(),
            axl.Defector(),
        ]:
            player.reset()
            match = Match((player, opponent), turns=30, seed=40)
            match.play()
            self.assertEqual(player.history[-1], C)

    def test_reset_attr(self):
        p = self.player()
        p.cycle = "CCDDCD"
        p.reset()
        self.assertEqual(p.cycle, None)


class TestEventualCycleHunter(TestPlayer):

    name = "Eventual Cycle Hunter"
    player = axl.EventualCycleHunter
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        player = self.player()
        # Test against cyclers
        for opponent in [
            axl.CyclerCCD(),
            axl.CyclerCCCD(),
            axl.CyclerCCCCCD(),
            axl.Alternator(),
        ]:
            player.reset()
            match = Match((player, opponent), turns=50)
            match.play()
            self.assertEqual(player.history[-1], D)
        # Test against non-cyclers and cooperators
        for opponent in [
            axl.Random(),
            axl.AntiCycler(),
            axl.DoubleCrosser(),
            axl.Cooperator(),
        ]:
            player.reset()
            match = Match((player, opponent), turns=50, seed=43)
            match.play()
            self.assertEqual(player.history[-1], C)

    def test_reset_attr(self):
        p = self.player()
        p.cycle = "CCDDCD"
        p.reset()
        self.assertEqual(p.cycle, None)


class TestMathConstantHunter(TestPlayer):

    name = "Math Constant Hunter"
    player = axl.MathConstantHunter
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        opponent = axl.MockPlayer([C] * 7 + [D] * 3)
        actions = [(C, C)] * 7 + [(C, D)]
        self.versus_test(opponent=opponent, expected_actions=actions)


class TestRandomHunter(TestPlayer):

    name = "Random Hunter"
    player = axl.RandomHunter
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):

        # We should catch the alternator here.
        actions = [(C, C), (C, D)] * 5 + [(C, C), (D, D), (D, C)]
        self.versus_test(
            opponent=axl.Alternator(),
            expected_actions=actions,
            attrs={"countCC": 5, "countDD": 0},
        )

        actions = [(C, D)] * 14
        self.versus_test(
            opponent=axl.Defector(),
            expected_actions=actions,
            attrs={"countCC": 0, "countDD": 0},
        )

    def test_reset(self):
        player = self.player()
        opponent = axl.Cooperator()
        match = Match((player, opponent), turns=100)
        match.play()
        self.assertFalse(player.countCC == 0)
        player.reset()
        self.assertTrue(player.countCC == 0)
