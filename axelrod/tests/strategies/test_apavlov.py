"""Tests APavlov strategies."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestAPavlov2006(TestPlayer):
    name = "Adaptive Pavlov 2006"
    player = axl.APavlov2006

    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C)] * 7
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            attrs={"opponent_class": "Cooperative"},
        )

        opponent = axl.MockPlayer(actions=[C] * 6 + [D])
        actions = [(C, C)] * 6 + [(C, D), (D, C)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "Cooperative"}
        )

        actions = [(C, D)] + [(D, D)] * 6
        self.versus_test(
            axl.Defector(),
            expected_actions=actions,
            attrs={"opponent_class": "ALLD"},
        )

        opponent = axl.MockPlayer(actions=[D, C, D, C, D, C])
        actions = [
            (C, D),
            (D, C),
            (C, D),
            (D, C),
            (C, D),
            (D, C),
            (C, D),
            (C, C),
            (C, D),
            (D, C),
        ]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "STFT"}
        )

        opponent = axl.MockPlayer(actions=[D, D, C, D, D, C])
        actions = [(C, D), (D, D), (D, C), (C, D), (D, D), (D, C), (D, D)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "PavlovD"}
        )

        opponent = axl.MockPlayer(actions=[D, D, C, D, D, C, D])
        actions = [(C, D), (D, D), (D, C), (C, D), (D, D), (D, C), (D, D), (C, D)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "PavlovD"}
        )

        opponent = axl.MockPlayer(actions=[C, C, C, D, D, D])
        actions = [(C, C), (C, C), (C, C), (C, D), (D, D), (D, D), (D, C)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "Random"}
        )

        opponent = axl.MockPlayer(actions=[D, D, D, C, C, C])
        actions = [(C, D), (D, D), (D, D), (D, C), (C, C), (C, C), (D, D)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "Random"}
        )


class TestAPavlov2011(TestPlayer):
    name = "Adaptive Pavlov 2011"
    player = axl.APavlov2011

    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):

        actions = [(C, C)] * 8
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            attrs={"opponent_class": "Cooperative"},
        )

        actions = [(C, D)] + [(D, D)] * 9
        self.versus_test(
            axl.Defector(),
            expected_actions=actions,
            attrs={"opponent_class": "ALLD"},
        )

        opponent = axl.MockPlayer(actions=[C, D, D, D, D, D, D])
        actions = [(C, C), (C, D)] + [(D, D)] * 5 + [(D, C)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "ALLD"}
        )

        opponent = axl.MockPlayer(actions=[C, C, D, D, D, D, D])
        actions = [(C, C), (C, C), (C, D)] + [(D, D)] * 4 + [(D, C)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "ALLD"}
        )

        opponent = axl.MockPlayer(actions=[C, D, D, C, D, D, D])
        actions = [(C, C), (C, D), (D, D), (D, C), (C, D), (D, D), (D, D), (D, C)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "ALLD"}
        )

        opponent = axl.MockPlayer(actions=[C, D, D, C, C, D, D])
        actions = [(C, C), (C, D), (D, D), (D, C), (C, C), (C, D), (C, D), (D, C)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "STFT"}
        )

        opponent = axl.MockPlayer(actions=[C, D, C, D, C, D, D])
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D), (C, D), (D, C)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "STFT"}
        )

        opponent = axl.MockPlayer(actions=[D, D, D, C, C, C, C])
        actions = [(C, D), (D, D), (D, D), (D, C), (C, C), (C, C), (C, C), (C, D)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "STFT"}
        )

        opponent = axl.MockPlayer(actions=[C, C, C, C, D, D])
        actions = [(C, C), (C, C), (C, C), (C, C), (C, D), (D, D), (D, C), (D, C)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "Random"}
        )

        opponent = axl.MockPlayer(actions=[D, D, C, C, C, C])
        actions = [(C, D), (D, D), (D, C), (C, C), (C, C), (C, C), (D, D), (D, D)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "Random"}
        )
