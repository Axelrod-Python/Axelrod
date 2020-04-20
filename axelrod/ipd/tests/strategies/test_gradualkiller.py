"""Tests for the Gradual Killer strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestGradualKiller(TestPlayer):

    name = "Gradual Killer: (D, D, D, D, D, C, C)"
    player = axl.GradualKiller
    expected_classifier = {
        "memory_depth": float("Inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    first_seven = [D, D, D, D, D, C, C]

    def test_first_seven_moves_always_the_same(self):
        opponent = axl.Cooperator()
        actions = list(zip(self.first_seven, [C] * 7))
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.Defector()
        actions = list(zip(self.first_seven, [D] * 7))
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.Alternator()
        actions = list(zip(self.first_seven, [C, D] * 4))
        self.versus_test(opponent, expected_actions=actions)

    def test_effect_of_strategy_with_history_CC(self):
        """Continues with C if opponent played CC on 6 and 7."""
        opponent_actions = [D] * 5 + [C, C] + [D, C] * 20
        opponent = axl.MockPlayer(actions=opponent_actions)

        start = list(zip(self.first_seven, opponent_actions[:7]))
        actions = start + [(C, D), (C, C)] * 20

        self.versus_test(opponent, expected_actions=actions)

    def test_effect_of_strategy_with_history_CD(self):
        """Continues with C if opponent played CD on 6 and 7."""
        opponent_actions = [D] * 5 + [C, D] + [D, C] * 20
        opponent = axl.MockPlayer(actions=opponent_actions)

        start = list(zip(self.first_seven, opponent_actions[:7]))
        actions = start + [(C, D), (C, C)] * 20

        self.versus_test(opponent, expected_actions=actions)

    def test_effect_of_strategy_with_history_DC(self):
        """Continues with C if opponent played DC on 6 and 7."""
        opponent_actions = [D] * 5 + [D, C] + [D, C] * 20
        opponent = axl.MockPlayer(actions=opponent_actions)

        start = list(zip(self.first_seven, opponent_actions[:7]))
        actions = start + [(C, D), (C, C)] * 20

        self.versus_test(opponent, expected_actions=actions)

    def test_effect_of_strategy_with_history_DD(self):
        """Continues with D if opponent played DD on 6 and 7."""
        opponent_actions = [C] * 5 + [D, D] + [D, C] * 20
        opponent = axl.MockPlayer(actions=opponent_actions)

        start = list(zip(self.first_seven, opponent_actions[:7]))
        actions = start + [(D, D), (D, C)] * 20

        self.versus_test(opponent, expected_actions=actions)
