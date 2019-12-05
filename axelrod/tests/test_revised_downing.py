from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D

class TestRevisedDowning(TestPlayer):

    name = "Revised Downing"
    player = axelrod.RevisedDowning
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
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D), (C, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[D, C, C])
        actions = [(C, D), (C, C), (C, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[D, D, C])
        actions = [(C, D), (C, D), (D, C), (D, D)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[C, C, D, D, C, C])
        actions = [(C, C), (C, C), (C, D), (C, D), (D, C), (D, C), (D, C)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[C, C, C, C, D, D])
        actions = [(C, C), (C, C), (C, C), (C, C), (C, D), (C, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions)
