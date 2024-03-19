"""Tests for the Grumpy strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestGrumpy(TestPlayer):

    name = "Grumpy: Nice, 10, -10"
    player = axl.Grumpy
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_default_strategy(self):

        opponent = axl.Cooperator()
        actions = [(C, C)] * 30
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.Alternator()
        actions = [(C, C), (C, D)] * 30
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.Defector()
        actions = [(C, D)] * 11 + [(D, D)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent_actions = [D] * 11 + [C] * 22 + [D] * 11
        opponent = axl.MockPlayer(actions=opponent_actions)
        actions = ([(C, D)] * 11 + [(D, C)] * 22 + [(C, D)] * 11) * 3
        self.versus_test(opponent, expected_actions=actions)

    def test_starting_state(self):
        opponent_actions = [D] * 11 + [C] * 22 + [D] * 11
        opponent = axl.MockPlayer(actions=opponent_actions)

        actions = ([(C, D)] * 11 + [(D, C)] * 22 + [(C, D)] * 11) * 3
        init_kwargs = {"starting_state": "Nice"}
        self.versus_test(
            opponent, expected_actions=actions, init_kwargs=init_kwargs
        )

        opponent = axl.MockPlayer(actions=opponent_actions)
        grumpy_starting = [(D, D)] * 11 + [(D, C)] * 22 + [(C, D)] * 11
        actions = grumpy_starting + actions
        init_kwargs = {"starting_state": "Grumpy"}
        self.versus_test(
            opponent, expected_actions=actions, init_kwargs=init_kwargs
        )

    def test_thresholds(self):
        init_kwargs = {"grumpy_threshold": 3, "nice_threshold": -2}
        opponent_actions = [D] * 4 + [C] * 7 + [D] * 3
        opponent = axl.MockPlayer(actions=opponent_actions)
        actions = ([(C, D)] * 4 + [(D, C)] * 7 + [(C, D)] * 3) * 3
        self.versus_test(
            opponent, expected_actions=actions, init_kwargs=init_kwargs
        )

        init_kwargs = {"grumpy_threshold": 0, "nice_threshold": -2}
        opponent_actions = [D] * 1 + [C] * 4 + [D] * 3
        opponent = axl.MockPlayer(actions=opponent_actions)
        actions = ([(C, D)] * 1 + [(D, C)] * 4 + [(C, D)] * 3) * 3
        self.versus_test(
            opponent, expected_actions=actions, init_kwargs=init_kwargs
        )

        init_kwargs = {"grumpy_threshold": 3, "nice_threshold": 0}
        opponent_actions = [D] * 4 + [C] * 5 + [D] * 1
        opponent = axl.MockPlayer(actions=opponent_actions)
        actions = ([(C, D)] * 4 + [(D, C)] * 5 + [(C, D)] * 1) * 3
        self.versus_test(
            opponent, expected_actions=actions, init_kwargs=init_kwargs
        )

    def test_reset_state_with_non_default_init(self):
        player = axl.Grumpy(starting_state="Grumpy")
        player.state = "Nice"
        player.reset()
        self.assertEqual(player.state, "Grumpy")
