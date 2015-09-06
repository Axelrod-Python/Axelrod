"""Test for the Cycler strategies."""

import itertools
import axelrod
from .test_player import TestPlayer, test_four_vector

C, D = 'C', 'D'


class TestAntiCycler(TestPlayer):

    name = "AntiCycler"
    player = axelrod.AntiCycler
    behaviour = {
        'stochastic': False,
        'memory_depth': float('inf'),
        'inspects_opponent_source': False,
        'updates_opponent_source': False
    }

    def test_strategy(self):
        """Starts by cooperating"""
        responses = [C, D, C, C, D, C, C, C, D, C, C, C, C, D, C, C, C]
        self.responses_test([], [], responses)


def test_cycler_factory(cycle):

    class TestCycler(TestPlayer):

        name = "Cycler %s" % cycle
        player = getattr(axelrod, 'Cycler%s' % cycle)
        behaviour = {
            'stochastic': False,
            'memory_depth': 1,
            'inspects_opponent_source': False,
            'updates_opponent_source': False
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
