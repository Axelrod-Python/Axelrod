"""Tests for the Cycler strategies."""
import random
import itertools

import axelrod
from axelrod import AntiCycler, Cycler
from axelrod._strategy_utils import detect_cycle
from axelrod.action import Action, str_to_actions

from .test_player import TestPlayer
from .test_evolvable_player import TestEvolvablePlayer

C, D = Action.C, Action.D


class TestAntiCycler(TestPlayer):

    name = "AntiCycler"
    player = axelrod.AntiCycler
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_has_no_cycles(self):
        test_range = 100
        player = AntiCycler()
        for _ in range(test_range):
            player.play(axelrod.Cooperator())

        contains_no_cycles = player.history
        for slice_at in range(1, len(contains_no_cycles) + 1):
            self.assertIsNone(detect_cycle(contains_no_cycles[:slice_at]))

    def test_strategy(self):
        """Rounds are CDD  CD  CCD CCCD CCCCD ..."""
        anticycler_rounds = [
            C,
            D,
            D,
            C,
            D,
            C,
            C,
            D,
            C,
            C,
            C,
            D,
            C,
            C,
            C,
            C,
            D,
            C,
            C,
            C,
            C,
            C,
            D,
        ]
        num_elements = len(anticycler_rounds)
        against_defector = list(zip(anticycler_rounds, [D] * num_elements))
        against_cooperator = list(zip(anticycler_rounds, [C] * num_elements))

        self.versus_test(axelrod.Defector(), expected_actions=against_defector)
        self.versus_test(axelrod.Cooperator(), expected_actions=against_cooperator)


class TestBasicCycler(TestPlayer):
    name = "Cycler: CCD"
    player = Cycler
    expected_classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_memory_depth_is_len_cycle_minus_one(self):
        len_ten = "DCDCDDCDCD"
        len_five = "DCDDC"
        depth_nine = Cycler(cycle=len_ten)
        depth_four = Cycler(cycle=len_five)
        self.assertEqual(depth_nine.classifier["memory_depth"], 9)
        self.assertEqual(depth_four.classifier["memory_depth"], 4)

    def test_cycler_works_as_expected(self):
        expected = [(C, D), (D, D), (D, D), (C, D)] * 2
        self.versus_test(
            axelrod.Defector(), expected_actions=expected, init_kwargs={"cycle": "CDDC"}
        )

    def test_cycle_raises_value_error_on_bad_cycle_str(self):
        self.assertRaises(ValueError, Cycler, cycle="CdDC")


class TestEvolvableCycler(TestEvolvablePlayer):
    name = "EvolvableCycler"
    player_class = axelrod.EvolvableCycler
    init_parameters = {"cycle_length": 100}


class TestEvolvableCycler(TestEvolvablePlayer):
    name = "EvolvableCycler"
    player_class = axelrod.EvolvableCycler
    randomized = False
    init_parameters = {"cycle": "".join(random.choice(("C", "D")) for _ in range(50))}


def test_cycler_factory(cycle_str):
    class TestCyclerChild(TestPlayer):

        name = "Cycler %s" % cycle_str
        player = getattr(axelrod, "Cycler%s" % cycle_str)
        expected_classifier = {
            "memory_depth": len(cycle_str) - 1,
            "stochastic": False,
            "makes_use_of": set(),
            "long_run_time": False,
            "inspects_source": False,
            "manipulates_source": False,
            "manipulates_state": False,
        }

        def test_strategy(self):
            """Starts by cooperating"""
            match_len = 20
            actions_generator = _get_actions_cycle_against_cooperator(cycle_str)
            test_actions = [next(actions_generator) for _ in range(match_len)]
            self.versus_test(axelrod.Cooperator(), expected_actions=test_actions)

    return TestCyclerChild


def _get_actions_cycle_against_cooperator(cycle_string: str):
    """Converts str like 'CCDC' to an itertools.cycle against Cooperator. The
    above example returns: itertools.cycle([(C, C), (C, C), (D, C), (C, C)])"""
    cooperator_opponent_action = C
    action_iterator = str_to_actions(cycle_string)
    out = [(action, cooperator_opponent_action) for action in action_iterator]
    return itertools.cycle(out)


TestCyclerDC = test_cycler_factory("DC")
TestCyclerCCD = test_cycler_factory("CCD")
TestCyclerDDC = test_cycler_factory("DDC")
TestCyclerCCCD = test_cycler_factory("CCCD")
TestCyclerCCCCCD = test_cycler_factory("CCCCCD")
TestCyclerCCCDCD = test_cycler_factory("CCCDCD")
