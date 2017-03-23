"""Tests for Calculator strategy."""

import axelrod
from .test_player import TestPlayer
from axelrod.actions import flip_action

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestCalculator(TestPlayer):

    name = "Calculator"
    player = axelrod.Calculator
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)

        P1 = axelrod.Calculator()
        P1.history = [C] * 20
        P2 = axelrod.Player()
        P2.history = [C, D] * 10
        # Defects on cycle detection
        self.assertEqual(D, P1.strategy(P2))

        # Test non-cycle response
        history = [C, C, D, C, C, D, C, C, C, D, C, C, C, C, D, C, C, C, C, C]
        P2.history = history
        self.assertEqual(C, P1.strategy(P2))

    def test_twenty_rounds_joss_then_defects_for_cyclers(self):
        first_twenty = []
        for index in range(20):
            if index in [18, 19]:
                first_twenty.append((D, C))
            else:
                first_twenty.append((C, C))
        expected_actions = first_twenty + [(D, C), (D, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions, seed=1)

    def test_twenty_rounds_joss_then_tit_for_tat_for_non_cyclers(self):
        seed = 2
        twenty_round_non_cycle = [C, C, D, C, C, D, C, C, C, D, C, C, C, C, D, C, C, C, C, C]

        first_twenty = []
        for index, action in enumerate(twenty_round_non_cycle):
            previous_action = twenty_round_non_cycle[index - 1]
            if index == 0:
                first_twenty.append((C, action))
            elif index in [1, 2]:
                first_twenty.append((flip_action(previous_action), action))
            else:
                first_twenty.append((previous_action, action))

        self.versus_test(axelrod.MockPlayer(twenty_round_non_cycle), first_twenty, seed=seed)

        after_twenty_round_non_cycle = [D, C, D, C, D, C, D, C]
        after_first_twenty = [(C, D), (D, C), (C, D), (D, C), (C, D), (D, C), (C, D), (D, C)]
        opponent_actions = twenty_round_non_cycle + after_twenty_round_non_cycle
        test_actions = first_twenty + after_first_twenty
        self.versus_test(axelrod.MockPlayer(opponent_actions), test_actions, seed=seed)

    def attribute_equality_test(self, player, clone):
        """Overwrite the default test to check Joss instance"""
        self.assertIsInstance(player.joss_instance, axelrod.Joss)
        self.assertIsInstance(clone.joss_instance, axelrod.Joss)
