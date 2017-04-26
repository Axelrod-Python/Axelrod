"""Tests for the GoByMajority strategies."""

import axelrod
from .test_player import TestPlayer
from axelrod import MockPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestHardGoByMajority(TestPlayer):

    name = "Hard Go By Majority"
    player = axelrod.HardGoByMajority
    eq_play = D
    soft = False

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
        self.first_play_test(self.eq_play)

        expected, opponent_actions = self.get_infinite_memory_depth_actions()
        self.versus_test(MockPlayer(actions=opponent_actions),
                         expected_actions=expected)

    def get_infinite_memory_depth_actions(self):
        opponent_actions = [C, D, D]
        first_three = [(self.eq_play, C), (C, D), (self.eq_play, D)]
        second_three = [(D, C), (self.eq_play, D), (D, D)]
        subsequent = [(D, C), (D, D), (D, D)]
        expected = first_three + second_three + subsequent * 10
        return expected, opponent_actions

    def test_memory_depth(self):
        memory_depth = 4
        opponent_actions = [C, C, C, D, D, D]
        first_six = [(self.eq_play, C), (C, C), (C, C),
                     (C, D), (C, D), (self.eq_play, D)]
        subsequent = [(D, C), (D, C), (self.eq_play, C),
                      (C, D), (C, D), (self.eq_play, D)]

        expected = first_six + subsequent * 10
        self.versus_test(MockPlayer(actions=opponent_actions),
                         expected_actions=expected,
                         init_kwargs={'memory_depth': memory_depth})

    def test_soft_value(self):
        player = self.player()
        self.assertFalse(player.soft)


class TestGoByMajority(TestHardGoByMajority):

    name = "Soft Go By Majority"
    player = axelrod.GoByMajority
    eq_play = C
    soft = True

    def test_set_soft_to_false(self):
        self.eq_play = D
        expected, opponent_actions = self.get_infinite_memory_depth_actions()
        self.versus_test(MockPlayer(actions=opponent_actions),
                         expected_actions=expected, init_kwargs={'soft': False})
        self.eq_play = C

    def test_soft_value(self):
        default = self.player()
        self.assertTrue(default.soft)
        player = self.player(soft=True)
        self.assertTrue(player.soft)
        player = self.player(soft=False)
        self.assertFalse(player.soft)

    def test_name(self):
        player = self.player(soft=True)
        self.assertEqual(player.name, "Soft Go By Majority")
        player = self.player(soft=False)
        self.assertEqual(player.name, "Hard Go By Majority")
        player = self.player(memory_depth=5)
        self.assertEqual(player.name, "Soft Go By Majority: 5")

    def test_str(self):
        player = self.player(soft=True)
        name = str(player)
        self.assertEqual(name, "Soft Go By Majority")
        player = self.player(soft=False)
        name = str(player)
        self.assertEqual(name, "Hard Go By Majority")
        player = self.player(memory_depth=5)
        name = str(player)
        self.assertEqual(name, "Soft Go By Majority: 5")


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
            """
            with memory_depth=3 always switches after
            opponent_history=[C, C, C, D, D] (int(3*1.5) + 1 = 5)
            with memory_depth=4 soft switches after
            op_history=[C, C, C, C, D, D, D] (int(4*1.5) + 1 = 7)
            and hard switches after
            op_history=[C, C, C, C, D, D] (int(4 * 1.5) = 6)
            """

            if soft:
                self.first_play_test(C)
            else:
                self.first_play_test(D)

            opponent_actions = [C] * memory_depth + [D] * memory_depth

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
            self.versus_test(MockPlayer(actions=opponent_actions),
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
