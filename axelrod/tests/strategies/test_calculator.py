"""Tests for Calculator strategy."""

import axelrod
from .test_player import TestPlayer
from axelrod.actions import flip_action
from axelrod._strategy_utils import detect_cycle
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

    def test_first_play(self):
        self.first_play_test(C)

    def test_twenty_rounds_joss_then_defects_for_cyclers(self):
        """uses axelrod.strategies.axelrod_first.Joss strategy for first 20 rounds"""
        seed = 2
        flip_indices = [1, 3]
        twenty_alternator_actions = [C, D] * 10
        twenty_test_actions = get_joss_strategy_actions(twenty_alternator_actions, flip_indices)

        expected_actions = twenty_test_actions + [(D, C), (D, D), (D, C), (D, D)]
        self.versus_test(axelrod.Alternator(), twenty_test_actions, seed=seed)
        self.versus_test(axelrod.Alternator(), expected_actions, seed=seed)

    def test_twenty_rounds_joss_then_tit_for_tat_for_non_cyclers(self):
        """uses axelrod.strategies.axelrod_first.Joss strategy for first 20 rounds"""
        seed = 2
        flip_indices = [1, 2]

        twenty_non_cyclical_actions = [C, C, D, C, C, D, C, C, C, D, C, C, C, C, D, C, C, C, C, C]
        twenty_test_actions = get_joss_strategy_actions(twenty_non_cyclical_actions, flip_indices)

        subsequent_opponent_actions = [D, C, D, C, D, C, D, C]
        subsequent_test_actions = [(C, D), (D, C), (C, D), (D, C), (C, D), (D, C), (C, D), (D, C)]

        opponent_actions = twenty_non_cyclical_actions + subsequent_opponent_actions
        test_actions = twenty_test_actions + subsequent_test_actions
        self.versus_test(axelrod.MockPlayer(twenty_non_cyclical_actions), twenty_test_actions, seed=seed)
        self.versus_test(axelrod.MockPlayer(opponent_actions), test_actions, seed=seed)

    def test_edge_case_calculator_sees_cycles_of_size_ten(self):
        seed = 3
        ten_length_cycle = [C, D, C, C, D, C, C, C, D, C]
        self.assertEqual(detect_cycle((ten_length_cycle * 2)), tuple(ten_length_cycle))

        ten_cycle_twenty_rounds = get_joss_strategy_actions(ten_length_cycle * 2, indices_to_flip=[16])
        opponent_actions = ten_length_cycle * 2 + [C, D, C]
        expected = ten_cycle_twenty_rounds + [(D, C), (D, D), (D, C)]
        self.versus_test(axelrod.MockPlayer(opponent_actions), expected, seed=seed)

    def test_edge_case_calculator_ignores_cycles_gt_len_ten(self):
        seed = 3
        eleven_length_cycle = [D, D, C, C, D, C, C, C, D, C, D]
        twenty_rounds_of_eleven_len_cycle = eleven_length_cycle + eleven_length_cycle[:9]
        twenty_rounds = get_joss_strategy_actions(twenty_rounds_of_eleven_len_cycle, indices_to_flip=[19])

        opponent_actions = twenty_rounds_of_eleven_len_cycle[: -1] + [D] + [C, D]
        self.assertEqual(detect_cycle(opponent_actions), tuple(eleven_length_cycle))

        uses_tit_for_tat_after_twenty_rounds = twenty_rounds + [(D, C), (C, D)]
        self.versus_test(axelrod.MockPlayer(opponent_actions), uses_tit_for_tat_after_twenty_rounds, seed=seed)

    def attribute_equality_test(self, player, clone):
        """Overwrite the default test to check Joss instance"""
        self.assertIsInstance(player.joss_instance, axelrod.Joss)
        self.assertIsInstance(clone.joss_instance, axelrod.Joss)

    def test_get_joss_strategy_actions(self):
        opponent = [C, D, D, C, C]

        flip_never_occurs_at_index_zero = [0]
        flip_indices = [1, 2]

        without_flip = [(C, C), (C, D), (D, D), (D, C), (C, C)]
        with_flip = [(C, C), (D, D), (C, D), (D, C), (C, C)]

        self.assertEqual(get_joss_strategy_actions(opponent, []), without_flip)
        self.assertEqual(get_joss_strategy_actions(opponent, flip_never_occurs_at_index_zero), without_flip)
        self.assertEqual(get_joss_strategy_actions(opponent, flip_indices), with_flip)


def get_joss_strategy_actions(opponent_moves: list, indices_to_flip: list) -> list:
    """
    take a list of opponent moves and returns a tuple list of [(Joss moves, opponent moves)]
    indices_to_flip are the indices where Joss differs from it's expected TitForTat.
    Joss is from axelrod.strategies.axelrod_first.
    """
    out = []
    for index, action in enumerate(opponent_moves):
        previous_action = opponent_moves[index - 1]
        if index == 0:
            out.append((C, action))
        elif index in indices_to_flip:
            out.append((flip_action(previous_action), action))
        else:
            out.append((previous_action, action))
    return out
