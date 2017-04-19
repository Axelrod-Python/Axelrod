"""Tests for the GoByMajority strategies."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestHardGoByMajority(TestPlayer):

    name = "Hard Go By Majority"
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


class TestGoByMajority(TestPlayer):

    name = "Soft Go By Majority"
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

    def test_name(self):
        player = self.player(soft=True)
        self.assertEqual(player.name, "Soft Go By Majority")
        player = self.player(soft=False)
        self.assertEqual(player.name, "Hard Go By Majority")

    def test_repr(self):
        player = self.player(soft=True)
        name = str(player)
        self.assertEqual(name, "Soft Go By Majority")
        player = self.player(soft=False)
        name = str(player)
        self.assertEqual(name, "Hard Go By Majority")


def factory_TestGoByRecentMajority(memory_depth, soft=True):

    prefix = "Hard"
    prefix2 = "Hard"
    if soft:
        prefix = "Soft"
        prefix2 = ""

    class TestGoByRecentMajority(TestPlayer):

        name = "{} Go By Majority: {}".format(prefix, memory_depth)
        player = getattr(axelrod, "{}GoByMajority{}".format(prefix2,
                                                            memory_depth))

        expected_classifier = {
            'stochastic': False,
            'memory_depth': memory_depth,
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

            opponent_actions = [C] * memory_depth + [D] * memory_depth
            """
            with memory_depth=3 always switches after
            opponent_history=[C, C, C, D, D]
            with memory_depth=4 soft switches after
            op_history=[C, C, C, C, D, D, D]
            and hard switches after
            op_history=[C, C, C, C, D, D]
            """
            if memory_depth % 2 == 1 or soft:
                cooperation_len = int(memory_depth * 1.5) + 1
            else:
                cooperation_len = int(memory_depth * 1.5)
            defect_len = 2 * memory_depth - cooperation_len

            if soft:
                first_move = [C]
            else:
                first_move = [D]

            player_actions = (first_move + [C] * (cooperation_len - 1) +
                              [D] * defect_len)
            expected = list(zip(player_actions, opponent_actions))
            self.versus_test(axelrod.MockPlayer(actions=opponent_actions),
                             expected_actions=expected)

    return TestGoByRecentMajority


TestGoByMajority5 = factory_TestGoByRecentMajority(5)
TestGoByMajority10 = factory_TestGoByRecentMajority(10)
TestGoByMajority20 = factory_TestGoByRecentMajority(20)
TestGoByMajority40 = factory_TestGoByRecentMajority(40)
TestHardGoByMajority5 = factory_TestGoByRecentMajority(5, soft=False)
TestHardGoByMajority10 = factory_TestGoByRecentMajority(10, soft=False)
TestHardGoByMajority20 = factory_TestGoByRecentMajority(20, soft=False)
TestHardGoByMajority40 = factory_TestGoByRecentMajority(40, soft=False)
