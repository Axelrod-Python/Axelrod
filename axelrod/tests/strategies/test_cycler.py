"""Tests for the Cycler strategies."""

import itertools
import axelrod
from axelrod.actions import Actions, str_to_actions
from .test_player import TestPlayer

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


def test_cycler_factory(cycle_str):

    class TestCycler(TestPlayer):

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

    return TestCycler


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
