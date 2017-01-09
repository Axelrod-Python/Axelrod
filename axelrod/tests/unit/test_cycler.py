"""Test for the Cycler strategies."""

import itertools
import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


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
        responses = C + D + C + C + D + C * 3 + D + C * 4 + D + C * 3
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
            for i in range(20):
                responses = itertools.islice(itertools.cycle(cycle), i)
            self.responses_test(responses)

    return TestCycler


TestCyclerDC = test_cycler_factory("DC")
TestCyclerCCD = test_cycler_factory("CCD")
TestCyclerDDC = test_cycler_factory("DDC")
TestCyclerCCCD = test_cycler_factory("CCCD")
TestCyclerCCCCCD = test_cycler_factory("CCCCCD")
TestCyclerCCCDCD = test_cycler_factory("CCCDCD")
