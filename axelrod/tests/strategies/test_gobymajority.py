"""Tests for the GoByMajority strategies."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestHardGoByMajority(TestPlayer):

    name = "Hard Go By Majority: inf"
    player = axelrod.HardGoByMajority
    default_soft = False
    eq_play = D

    expected_classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by defecting.
        self.first_play_test(self.eq_play)
        # If opponent cooperates at least as often as they defect then the
        # player defects.
        self.responses_test([self.eq_play], [C, D, D, D], [D, D, C, C])
        # If opponent defects strictly more often than they defect then the
        # player defects.
        self.responses_test([D], [C, C, D, D, C], [D, D, C, C, D])
        # If opponent cooperates strictly more often than they defect then the
        # player cooperates.
        self.responses_test([C], [C, C, D, D, C], [D, C, C, C, D])

    def test_default_soft(self):
        player = self.player()
        self.assertEqual(player.soft, self.default_soft)


class TestGoByMajority(TestHardGoByMajority):

    name = "Go By Majority: inf, True"
    player = axelrod.GoByMajority
    default_soft = True
    eq_play = C

    def test_strategy(self):
        # In case of equality (including first play), cooperates.
        super().test_strategy()

        # Test tie break rule for soft=False
        player = self.player(soft=False)
        opponent = axelrod.Cooperator()
        self.assertEqual('D', player.strategy(opponent))

    def test_soft(self):
        player = self.player(soft=True)
        self.assertTrue(player.soft)
        player = self.player(soft=False)
        self.assertFalse(player.soft)


def factory_TestGoByRecentMajority(L, soft=True):

    prefix = "Hard"
    prefix2 = "Hard"
    if soft:
        prefix = "Soft"
        prefix2 = ""

    class TestGoByRecentMajority(TestPlayer):

        name = "{} Go By Majority {}".format(prefix, L)
        player = getattr(axelrod, "{}GoByMajority{}".format(prefix2, L))

        expected_classifier = {
            'stochastic': False,
            'memory_depth': L,
            'makes_use_of': set(),
            'long_run_time': False,
            'inspects_source': False,
            'manipulates_source': False,
            'manipulates_state': False
        }

        def test_strategy(self):
            # Test initial play.
            if soft:
                self.first_play_test(C)
            else:
                self.first_play_test(D)

            self.responses_test([C], [C] * L,
                                [C] * (L // 2 + 1) + [D] * (L // 2 - 1))
            self.responses_test([D], [C] * L,
                                [D] * (L // 2 + 1) + [C] * (L // 2 - 1))

            # Test 50:50 play difference with soft
            k = L
            if L % 2 == 1:
                k -= 1
            if soft:
                self.responses_test([C], [C] * k,
                                    [C] * (k // 2) + [D] * (k // 2))
            else:
                self.responses_test([D], [C] * k,
                                    [C] * (k // 2) + [D] * (k // 2))

    return TestGoByRecentMajority


TestGoByMajority5 = factory_TestGoByRecentMajority(5)
TestGoByMajority10 = factory_TestGoByRecentMajority(10)
TestGoByMajority20 = factory_TestGoByRecentMajority(20)
TestGoByMajority40 = factory_TestGoByRecentMajority(40)
TestHardGoByMajority5 = factory_TestGoByRecentMajority(5, soft=False)
TestHardGoByMajority10 = factory_TestGoByRecentMajority(10, soft=False)
TestHardGoByMajority20 = factory_TestGoByRecentMajority(20, soft=False)
TestHardGoByMajority40 = factory_TestGoByRecentMajority(40, soft=False)
