"""Tests for the Cycler strategies."""

import itertools
import axelrod
from axelrod.actions import Actions, str_to_actions
from .test_player import TestPlayer
from axelrod import Cycler

C, D = Actions.C, Actions.D


class TestAntiCycler(TestPlayer):

    name = "AntiCycler"
    player = axelrod.AntiCycler
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by cooperating"""
        responses = [C, D, C, C, D, C, C, C, D, C, C, C, C, D, C, C, C]
        self.responses_test(responses)


class TestBasicCycler(TestPlayer):
    name = "Cycler CCD"
    player = Cycler
    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_repr(self):
        cycle_str = 'DDCCDDCDCDCDC'
        self.assertEqual(repr(Cycler(cycle_str)), 'Cycler {}'.format(cycle_str))

    def test_memory_depth_is_len_cycle_minus_one(self):
        len_ten = 'DCDCDDCDCD'
        len_five = 'DCDDC'
        depth_nine = Cycler(len_ten)
        depth_four = Cycler(len_five)
        self.assertEqual(depth_nine.classifier['memory_depth'], 9)
        self.assertEqual(depth_four.classifier['memory_depth'], 4)

    def test_cycler_works_as_expected(self):
        expected = [(C, D), (D, D), (D, D), (C, D)] * 2
        self.versus_test(axelrod.Defector(), expected, init_kwargs={'cycle': 'CDDC'})

    def test_cycle_raises_value_error_on_bad_cycle_str(self):
        self.assertRaises(ValueError, Cycler, 'CdDC')


def test_cycler_factory(cycle_str):

    class TestCyclerChild(TestPlayer):

        name = "Cycler %s" % cycle_str
        player = getattr(axelrod, 'Cycler%s' % cycle_str)
        expected_classifier = {
            'memory_depth': len(cycle_str) - 1,
            'stochastic': False,
            'makes_use_of': set(),
            'long_run_time': False,
            'inspects_source': False,
            'manipulates_source': False,
            'manipulates_state': False
        }

        def test_strategy(self):
            """Starts by cooperating"""
            match_len = 20
            actions_generator = _get_actions_cycle_against_cooperator(cycle_str)
            test_actions = [next(actions_generator) for _ in range(match_len)]
            self.versus_test(axelrod.Cooperator(), test_actions)

    return TestCyclerChild


def _get_actions_cycle_against_cooperator(cycle_string: str):
    """converts str like 'CCDC' to an itertools.cycle against Cooperator [(C, C), (C, C), (D, C), (C, C)]
    (Where C=Actions.C, D=Actions.D)"""
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
