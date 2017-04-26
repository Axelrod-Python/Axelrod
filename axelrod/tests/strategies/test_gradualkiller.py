"""Tests for the Gradual Killer strategy."""

import axelrod as axl
from .test_player import TestPlayer

C, D = axl.Actions.C, axl.Actions.D


class TestGradualKiller(TestPlayer):

    name = "Gradual Killer: ('D', 'D', 'D', 'D', 'D', 'C', 'C')"
    player = axl.GradualKiller
    expected_classifier = {
        'memory_depth': float('Inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    first_seven = [D, D, D, D, D, C, C]

    def test_strategy(self):
        # Starts by defecting.
        self.first_play_test(D)
        self.second_play_test(D, D, D, D)
        # First seven moves.
        vs_cooperator = list(zip(self.first_seven, [C] * 7))
        vs_defector = list(zip(self.first_seven, [D] * 7))
        vs_alternator = list(zip(self.first_seven, [C, D] * 3 + [C]))

        self.versus_test(axl.Cooperator(), expected_actions=vs_cooperator)
        self.versus_test(axl.Defector(), expected_actions=vs_defector)
        self.versus_test(axl.Alternator(), expected_actions=vs_alternator)

    def test_effect_of_strategy_with_history_CC(self):
        """Continues with C if opponent played CC on 6 and 7."""
        expected, opponent = self.get_actions_for_test(D, [C, C], C)
        self.versus_test(axl.MockPlayer(actions=opponent),
                         expected_actions=expected)

    def test_effect_of_strategy_with_history_CD(self):
        """Continues with C if opponent played CD on 6 and 7."""
        expected, opponent = self.get_actions_for_test(D, [C, D], C)
        self.versus_test(axl.MockPlayer(actions=opponent),
                         expected_actions=expected)

    def test_effect_of_strategy_with_history_DC(self):
        """Continues with C if opponent played DC on 6 and 7."""
        expected, opponent = self.get_actions_for_test(D, [D, C], C)
        self.versus_test(axl.MockPlayer(actions=opponent),
                         expected_actions=expected)

    def test_effect_of_strategy_with_history_DD(self):
        """Continues with D if opponent played DD on 6 and 7."""
        expected, opponent = self.get_actions_for_test(C, [D, D], D)
        self.versus_test(axl.MockPlayer(actions=opponent),
                         expected_actions=expected)

    def get_actions_for_test(self, opponent_start, action_six_and_seven,
                             gradual_killer_response):
        opponent = [opponent_start] * 5 + action_six_and_seven
        start = list(zip(self.first_seven, opponent))
        subsequent = list(zip([gradual_killer_response] * 7, opponent))
        expected = start + subsequent * 5
        return expected, opponent

    def test_get_actions_for_test(self):
        expected, opponent = self.get_actions_for_test(C, [D, C], D)
        self.assertEqual(opponent, [C, C, C, C, C, D, C])
        first_seven = expected[:7]
        self.assertEqual(first_seven, list(zip(self.first_seven, opponent)))

        subsequent = expected[7:]
        expected_subsequent = list(zip([D] * 7, opponent)) * 5
        self.assertEqual(subsequent, expected_subsequent)
