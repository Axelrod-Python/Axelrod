import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestRevisedDowning(TestPlayer):

    name = "Revised Downing"
    player = axl.RevisedDowning
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
        actions = [(C, C), (C, C), (C, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        actions = [(C, D), (C, D), (D, D)]
        self.versus_test(axl.Defector(), expected_actions=actions)

        opponent = axl.MockPlayer(actions=[D, C, C])
        actions = [(C, D), (C, C), (C, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.MockPlayer(actions=[D, D, C])
        actions = [(C, D), (C, D), (D, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.MockPlayer(actions=[C, C, D, D, C, C])
        actions = [(C, C), (C, C), (C, D), (C, D), (D, C), (C, C), (D, C)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.MockPlayer(actions=[C, C, C, C, D, D])
        actions = [(C, C), (C, C), (C, C), (C, C), (C, D), (C, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions)
