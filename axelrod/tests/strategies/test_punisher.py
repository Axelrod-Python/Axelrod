"""Tests for the Punisher strategies."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D


class TestPunisher(TestPlayer):

    name = "Punisher"
    player = axelrod.Punisher
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_init(self):
        """Tests for the __init__ method."""
        player = axelrod.Punisher()
        self.assertEqual(player.mem_length, 1)
        self.assertFalse(player.grudged)
        self.assertEqual(player.grudge_memory, 1)

    def test_strategy(self):
        opponent = axelrod.Alternator()
        actions = [(C, C), (C, D), (D, C)]
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            attrs={"grudged": True, "grudge_memory": 0},
        )

        opponent = axelrod.MockPlayer([C, D] + [C] * 10)
        actions = [(C, C), (C, D)] + [(D, C)] * 11
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            attrs={"grudged": True, "grudge_memory": 10},
        )

        # Eventually the grudge is dropped
        opponent = axelrod.MockPlayer([C, D] + [C] * 10)
        actions = [(C, C), (C, D)] + [(D, C)] * 11 + [(C, D)]
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            attrs={"grudged": False, "grudge_memory": 0, "mem_length": 10},
        )

        # Grudged again on opponent's D
        opponent = axelrod.MockPlayer([C, D] + [C] * 11)
        actions = [(C, C), (C, D)] + [(D, C)] * 11 + [(C, C), (C, D), (D, C)]
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            attrs={"grudged": True, "grudge_memory": 0, "mem_length": 2},
        )


class TestInversePunisher(TestPlayer):

    name = "Inverse Punisher"
    player = axelrod.InversePunisher
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_init(self):
        """Tests for the __init__ method."""
        player = axelrod.InversePunisher()
        self.assertEqual(player.mem_length, 1)
        self.assertFalse(player.grudged)
        self.assertEqual(player.grudge_memory, 1)

    def test_strategy(self):
        opponent = axelrod.Alternator()
        actions = [(C, C), (C, D), (D, C)]
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            attrs={"grudged": True, "grudge_memory": 0},
        )

        opponent = axelrod.MockPlayer([C, D] + [C] * 10)
        actions = [(C, C), (C, D)] + [(D, C)] * 11
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            attrs={"grudged": True, "grudge_memory": 10},
        )

        # Eventually the grudge is dropped
        opponent = axelrod.MockPlayer([C, D] + [C] * 10)
        actions = [(C, C), (C, D)] + [(D, C)] * 11 + [(C, D)]
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            attrs={"grudged": False, "grudge_memory": 0, "mem_length": 10},
        )

        # Grudged again on opponent's D
        opponent = axelrod.MockPlayer([C, D] + [C] * 11)
        actions = [(C, C), (C, D)] + [(D, C)] * 11 + [(C, C), (C, D), (D, C)]
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            attrs={"grudged": True, "grudge_memory": 0, "mem_length": 17},
        )


class TestLevelPunisher(TestPlayer):

    name = "Level Punisher"
    player = axelrod.LevelPunisher
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Cooperates if the turns played are less than 10.
        actions = [(C, C)] * 9
        self.versus_test(opponent=axelrod.Cooperator(), expected_actions=actions)

        # After 10 rounds
        # Check if number of defections by opponent is greater than 20%
        opponent = axelrod.MockPlayer([C] * 4 + [D] * 2 + [C] * 3 + [D])
        actions = [(C, C)] * 4 + [(C, D)] * 2 + [(C, C)] * 3 + [(C, D), (D, C)]
        self.versus_test(opponent=opponent, expected_actions=actions)

        # Check if number of defections by opponent is less than 20%
        opponent = axelrod.MockPlayer([C] * 4 + [D] + [C] * 4 + [D])
        actions = [(C, C)] * 4 + [(C, D)] + [(C, C)] * 4 + [(C, D), (C, C)]
        self.versus_test(opponent=opponent, expected_actions=actions)


class TestTrickyLevelPunisher(TestPlayer):

    name = "Level Punisher"
    player = axelrod.LevelPunisher
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Cooperates if the turns played are less than 10.
        actions = [(C, C)] * 9
        self.versus_test(opponent=axelrod.Cooperator(), expected_actions=actions)

        # After 10 rounds
        # Check if number of defections by opponent is greater than 20%
        opponent = axelrod.MockPlayer([C] * 4 + [D] * 2 + [C] * 3 + [D])
        actions = [(C, C)] * 4 + [(C, D)] * 2 + [(C, C)] * 3 + [(C, D), (D, C)]
        self.versus_test(opponent=opponent, expected_actions=actions)

        # Check if number of defections by opponent is greater than 10%
        opponent = axelrod.MockPlayer([C] * 4 + [D] + [C] * 4 + [D])
        actions = [(C, C)] * 4 + [(C, D)] + [(C, C)] * 4 + [(C, D), (C, C)]
        self.versus_test(opponent=opponent, expected_actions=actions)

        # After 10 rounds
        # Check if number of defections by opponent is greater than 5%
        opponent = axelrod.MockPlayer([C] * 4 + [D] + [C] * 5)
        actions = [(C, C)] * 4 + [(C, D)] + [(C, C)] * 5
        self.versus_test(opponent=opponent, expected_actions=actions)

        # Check if number of defections by opponent is less than 5%
        opponent = axelrod.MockPlayer([C] * 10)
        actions = [(C, C)] * 5
        self.versus_test(opponent=opponent, expected_actions=actions)
