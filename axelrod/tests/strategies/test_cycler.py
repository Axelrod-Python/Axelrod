"""Tests for the Cycler strategies."""

import itertools
import axelrod
from axelrod import Actions
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


def test_cycler_factory(cycle):

    class TestCycler(TestPlayer):

        name = "Cycler %s" % cycle
        player = getattr(axelrod, 'Cycler%s' % cycle)
        expected_classifier = {
            'memory_depth': len(cycle) - 1,
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
            actions_cycle = _get_actions_cycle_against_cooperator(cycle)
            test_actions = list(itertools.islice(itertools.cycle(actions_cycle), match_len))
            self.versus_test(axelrod.Cooperator(), test_actions)

    return TestCycler


def _get_actions_cycle_against_cooperator(cycle_string: str) -> [(Actions, Actions)]:
    """converts str like 'CCDC' to set of actions against Cooperator [(C, C), (C, C), (D, C), (C, C)]
    (Where C=Actions.C, D=Actions.D)"""
    cooperator_opponent_action = C
    out = []
    for action_str in cycle_string:
        action = _get_action(action_str)
        out.append((action, cooperator_opponent_action))
    return out


def _get_action(action_str: str) -> Actions:
    """takes a string and returns appropriate Actions class."""
    actions = {'C': C, 'D': D}
    return actions[action_str]


TestCyclerDC = test_cycler_factory("DC")
TestCyclerCCD = test_cycler_factory("CCD")
TestCyclerDDC = test_cycler_factory("DDC")
TestCyclerCCCD = test_cycler_factory("CCCD")
TestCyclerCCCCCD = test_cycler_factory("CCCCCD")
TestCyclerCCCDCD = test_cycler_factory("CCCDCD")
