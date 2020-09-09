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

    def test_strategy_versus_cooperator(self):
        actions = [(C, C)] * 7
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            attrs={"opponent_class": "Cooperative"},
        )

    def test_strategy_versus_mock_player(self):
        """Tests that one defection after does not affect opponent_class determination."""
        opponent = axl.MockPlayer(actions=[C] * 6 + [D])
        actions = [(C, C)] * 6 + [(C, D), (D, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={"opponent_class": "Cooperative"},
        )

    def test_strategy_versus_defector(self):
        """Tests that defector is recognized correctly."""
        actions = [(C, D)] + [(D, D)] * 6
        self.versus_test(
            axl.Defector(),
            expected_actions=actions,
            attrs={"opponent_class": "ALLD"},
        )

    def test_strategy_stft(self):
        """Tests that STFT can be identified by DCDCDC and the subsequent response."""
        opponent = axl.CyclerDC()
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

    def test_strategy_PavlovD(self):
        """Tests that PavolvD is identified by DDCDDC."""
        opponent = axl.Cycler(cycle="DDC")
        actions = [(C, D), (D, D), (D, C), (C, D), (D, D), (D, C), (D, D)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={"opponent_class": "PavlovD"},
        )

    def test_strategy_PavlovD2(self):
        """Tests that PavolvD is identified by DDCDDC and that the response
        is D then C"""
        opponent = axl.MockPlayer(actions=[D, D, C, D, D, C, D])
        actions = [
            (C, D),
            (D, D),
            (D, C),
            (C, D),
            (D, D),
            (D, C),
            (D, D),
            (C, D),
        ]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={"opponent_class": "PavlovD"},
        )

    def test_strategy_random(self):
        opponent = axl.MockPlayer(actions=[C, C, C, D, D, D])
        actions = [(C, C), (C, C), (C, C), (C, D), (D, D), (D, D), (D, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={"opponent_class": "Random"},
        )

    def test_strategy_random2(self):
        opponent = axl.MockPlayer(actions=[D, D, D, C, C, C])
        actions = [(C, D), (D, D), (D, D), (D, C), (C, C), (C, C), (D, D)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={"opponent_class": "Random"},
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

    def test_strategy_cooperator(self):
        actions = [(C, C)] * 8
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            attrs={"opponent_class": "Cooperative"},
        )

    def test_strategy_defector(self):
        actions = [(C, D)] + [(D, D)] * 9
        self.versus_test(
            axl.Defector(),
            expected_actions=actions,
            attrs={"opponent_class": "ALLD"},
        )

    def test_strategy_defector2(self):
        opponent = axl.MockPlayer(actions=[C, D, D, D, D, D, D])
        actions = [(C, C), (C, D)] + [(D, D)] * 5 + [(D, C)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "ALLD"}
        )

    def test_strategy_defector3(self):
        opponent = axl.MockPlayer(actions=[C, C, D, D, D, D, D])
        actions = [(C, C), (C, C), (C, D)] + [(D, D)] * 4 + [(D, C)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "ALLD"}
        )

    def test_strategy_defector4(self):
        opponent = axl.MockPlayer(actions=[C, D, D, C, D, D, D])
        actions = [
            (C, C),
            (C, D),
            (D, D),
            (D, C),
            (C, D),
            (D, D),
            (D, D),
            (D, C),
        ]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "ALLD"}
        )

    def test_strategy_stft(self):
        opponent = axl.MockPlayer(actions=[C, D, D, C, C, D, D])
        actions = [
            (C, C),
            (C, D),
            (D, D),
            (D, C),
            (C, C),
            (C, D),
            (C, D),
            (D, C),
        ]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "STFT"}
        )

    def test_strategy_stft2(self):
        opponent = axl.MockPlayer(actions=[C, D, C, D, C, D, D])
        actions = [
            (C, C),
            (C, D),
            (D, C),
            (C, D),
            (D, C),
            (C, D),
            (C, D),
            (D, C),
        ]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "STFT"}
        )

    def test_strategy_stft3(self):
        opponent = axl.MockPlayer(actions=[D, D, D, C, C, C, C])
        actions = [
            (C, D),
            (D, D),
            (D, D),
            (D, C),
            (C, C),
            (C, C),
            (C, C),
            (C, D),
        ]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_class": "STFT"}
        )

    def test_strategy_random(self):
        opponent = axl.MockPlayer(actions=[C, C, C, C, D, D])
        actions = [
            (C, C),
            (C, C),
            (C, C),
            (C, C),
            (C, D),
            (D, D),
            (D, C),
            (D, C),
        ]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={"opponent_class": "Random"},
        )

    def test_strategy_random2(self):
        opponent = axl.MockPlayer(actions=[D, D, C, C, C, C])
        actions = [
            (C, D),
            (D, D),
            (D, C),
            (C, C),
            (C, C),
            (C, C),
            (D, D),
            (D, D),
        ]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={"opponent_class": "Random"},
        )
