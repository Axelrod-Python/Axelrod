"""Test for the Cycler strategies."""

import itertools
import axelrod
from .test_player import TestPlayer, test_four_vector

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestAntiCycler(TestPlayer):

    name = "AntiCycler"
    player = axelrod.AntiCycler
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by cooperating"""
        responses = [C, D, C, C, D, C, C, C, D, C, C, C, C, D, C, C, C]
        self.responses_test([], [], responses)


def test_cycler_factory(cycle):

    class TestCycler(TestPlayer):

        name = "Cycler %s" % cycle
        player = getattr(axelrod, 'Cycler%s' % cycle)
        expected_classifier = {
            'memory_depth': len(cycle) - 1,
            'stochastic': False,
            'makes_use_of': set(),
            'inspects_source': False,
            'manipulates_source': False,
            'manipulates_state': False
        }

        def test_strategy(self):
            """Starts by cooperating"""
            for i in range(20):
                responses = itertools.islice(itertools.cycle(cycle), i)
            self.responses_test([], [], responses)

    return TestCycler

TestCyclerCCD = test_cycler_factory("CCD")
TestCyclerCCCD = test_cycler_factory("CCCD")
TestCyclerCCCCCD = test_cycler_factory("CCCCCD")
