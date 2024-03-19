"""Tests for the GoByMajority strategies."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestHardGoByMajority(TestPlayer):

    name = "Hard Go By Majority"
    player = axl.HardGoByMajority
    default_soft = False

    expected_classifier = {
        "stochastic": False,
        "memory_depth": float("inf"),
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_memory_depth_infinite_soft_is_false(self):
        init_kwargs = {}
        if self.default_soft:
            init_kwargs["soft"] = False

        opponent_actions = [C] * 50 + [D] * 100 + [C] * 52
        actions = (
            [(D, C)]
            + [(C, C)] * 49
            + [(C, D)] * 50
            + [(D, D)] * 50
            + [(D, C)] * 51
            + [(C, C)]
        )
        opponent = axl.MockPlayer(actions=opponent_actions)
        self.versus_test(
            opponent, expected_actions=actions, init_kwargs=init_kwargs
        )

    def test_memory_depth_even_soft_is_false(self):
        memory_depth = 4
        init_kwargs = {"memory_depth": memory_depth}
        if self.default_soft:
            init_kwargs["soft"] = False

        opponent = axl.MockPlayer(
            actions=[C] * memory_depth + [D] * memory_depth
        )
        actions = (
            [(D, C)]
            + [(C, C)] * 3
            + [(C, D)] * 2
            + [(D, D)] * 2
            + [(D, C)] * 3
            + [(C, C)]
        )
        self.versus_test(
            opponent, expected_actions=actions, init_kwargs=init_kwargs
        )

    def test_memory_depth_odd(self):
        memory_depth = 5
        init_kwargs = {"memory_depth": memory_depth}
        if self.default_soft:
            first_action = [(C, C)]
        else:
            first_action = [(D, C)]
        opponent = axl.MockPlayer(
            actions=[C] * memory_depth + [D] * memory_depth
        )
        actions = (
            first_action
            + [(C, C)] * 4
            + [(C, D)] * 3
            + [(D, D)] * 2
            + [(D, C)] * 3
            + [(C, C)] * 2
        )
        self.versus_test(
            opponent, expected_actions=actions, init_kwargs=init_kwargs
        )

    def test_default_values(self):
        player = self.player()
        self.assertEqual(player.soft, self.default_soft)
        self.assertEqual(player.memory, 0)


class TestGoByMajority(TestHardGoByMajority):

    name = "Soft Go By Majority"
    player = axl.GoByMajority
    default_soft = True

    def test_memory_depth_infinite_soft_is_true(self):
        opponent_actions = [C] * 50 + [D] * 100 + [C] * 52
        actions = (
            [(C, C)] * 50
            + [(C, D)] * 51
            + [(D, D)] * 49
            + [(D, C)] * 50
            + [(C, C)] * 2
        )
        opponent = axl.MockPlayer(actions=opponent_actions)
        self.versus_test(opponent, expected_actions=actions)

    def test_memory_depth_even_soft_is_true(self):
        memory_depth = 4
        init_kwargs = {"memory_depth": memory_depth}

        opponent = axl.MockPlayer([C] * memory_depth + [D] * memory_depth)
        actions = (
            [(C, C)] * 4 + [(C, D)] * 3 + [(D, D)] + [(D, C)] * 2 + [(C, C)] * 2
        )
        self.versus_test(
            opponent, expected_actions=actions, init_kwargs=init_kwargs
        )

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
        player = getattr(axl, "{}GoByMajority{}".format(prefix2, memory_depth))

        expected_classifier = {
            "stochastic": False,
            "memory_depth": memory_depth,
            "makes_use_of": set(),
            "long_run_time": False,
            "inspects_source": False,
            "manipulates_source": False,
            "manipulates_state": False,
        }

        def test_strategy(self):
            # for example memory_depth=2 plays against [C, C, D, D]
            # soft actions = [(C, C), (C, C), (C, D), (C, D)]
            # hard actions = [(D, C), (C, C), (C, D), (D, D)]
            opponent_actions = [C] * memory_depth + [D] * memory_depth
            opponent = axl.MockPlayer(actions=opponent_actions)
            if soft:
                first_player_action = [C]
            else:
                first_player_action = [D]
            if memory_depth % 2 == 1 or soft:
                cooperations = int(memory_depth * 1.5)
            else:
                cooperations = int(memory_depth * 1.5) - 1
            defections = len(opponent_actions) - cooperations - 1
            player_actions = (
                first_player_action + [C] * cooperations + [D] * defections
            )

            actions = list(zip(player_actions, opponent_actions))
            self.versus_test(opponent, expected_actions=actions)

    return TestGoByRecentMajority


TestGoByMajority5 = factory_TestGoByRecentMajority(5)
TestGoByMajority10 = factory_TestGoByRecentMajority(10)
TestGoByMajority20 = factory_TestGoByRecentMajority(20)
TestGoByMajority40 = factory_TestGoByRecentMajority(40)
TestHardGoByMajority5 = factory_TestGoByRecentMajority(5, soft=False)
TestHardGoByMajority10 = factory_TestGoByRecentMajority(10, soft=False)
TestHardGoByMajority20 = factory_TestGoByRecentMajority(20, soft=False)
TestHardGoByMajority40 = factory_TestGoByRecentMajority(40, soft=False)
