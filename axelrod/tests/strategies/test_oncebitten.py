"""Tests for the once bitten strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestOnceBitten(TestPlayer):

    name = "Once Bitten"
    player = axl.OnceBitten
    expected_classifier = {
        "memory_depth": 12,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        """If opponent defects at any point then the player will defect
        forever."""
        # Become grudged if the opponent defects twice in a row
        opponent = axl.MockPlayer([C, C, C, D])
        actions = [(C, C), (C, C), (C, C), (C, D), (C, C)]
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            attrs={"grudged": False, "grudge_memory": 0},
        )

        opponent = axl.MockPlayer([C, C, C, D, D, D])
        actions = [
            (C, C),
            (C, C),
            (C, C),
            (C, D),
            (C, D),
            (D, D),
            (D, C),
            (D, C),
            (D, C),
            (D, D),
            (D, D),
        ]
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            attrs={"grudged": True, "grudge_memory": 5},
        )

        # After 10 rounds of being grudged: forgives
        opponent = axl.MockPlayer([C, D, D, C] + [C] * 10)
        actions = [(C, C), (C, D), (C, D), (D, C)] + [(D, C)] * 10 + [(C, C)]
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            attrs={"grudged": False, "grudge_memory": 0},
        )

    def test_reset(self):
        """Check that grudged gets reset properly"""
        p1 = self.player()
        p2 = axl.Defector()
        match = axl.Match((p1, p2), turns=3, seed=0)
        match.play()
        self.assertTrue(p1.grudged)
        p1.reset()
        self.assertFalse(p1.grudged)


class TestFoolMeOnce(TestPlayer):

    name = "Fool Me Once"
    player = axl.FoolMeOnce
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
        # If opponent defects more than once, defect forever
        actions = [(C, C)] * 10
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        opponent = axl.MockPlayer([D] + [C] * 9)
        actions = [(C, D)] + [(C, C)] * 9
        self.versus_test(opponent=opponent, expected_actions=actions)

        actions = [(C, D)] * 2 + [(D, D)] * 8
        self.versus_test(opponent=axl.Defector(), expected_actions=actions)

        opponent = axl.MockPlayer([D, D] + [C] * 9)
        actions = [(C, D)] * 2 + [(D, C)] * 8
        self.versus_test(opponent=opponent, expected_actions=actions)


class TestForgetfulFoolMeOnce(TestPlayer):

    name = "Forgetful Fool Me Once: 0.05"
    player = axl.ForgetfulFoolMeOnce
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Test that will forgive one D but will grudge after 2 Ds, randomly
        # forgets count.
        actions = [(C, C), (C, D), (C, C), (C, D), (D, C)]
        self.versus_test(
            opponent=axl.Alternator(),
            expected_actions=actions,
            seed=2,
            attrs={"D_count": 2},
        )

        # Sometime eventually forget count:
        actions = [(C, D), (C, D)] + [(D, D)] * 3 + [(C, D)]
        self.versus_test(
            opponent=axl.Defector(),
            expected_actions=actions,
            seed=4,
            attrs={"D_count": 0},
        )
