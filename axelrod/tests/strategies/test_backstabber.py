"""Tests for BackStabber and DoubleCrosser."""
import axelrod
import unittest

from axelrod.strategies import backstabber
from axelrod.mock_player import Player, update_history
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestBackStabber(TestPlayer):

    name = "BackStabber: ('D', 'D')"
    player = axelrod.BackStabber
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': {'length'},
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_defects_after_four_defections(self):
        self.first_play_test(C)
        # Forgives three defections
        defector_actions = [(C, D), (C, D), (C, D), (C, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=defector_actions, match_attributes={"length": 200})
        alternator_actions = [(C, C), (C, D)] * 4 + [(D, C), (D, D)] * 2
        self.versus_test(axelrod.Alternator(), expected_actions=alternator_actions, match_attributes={"length": 200})

    def test_defects_on_last_two_rounds_by_match_len(self):
        actions = [(C, C)] * 198 + [(D, C), (D, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, match_attributes={"length": 200})

        actions = [(C, C)] * 10 + [(D, C), (D, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, match_attributes={"length": 12})

        # Test that exceeds tournament length
        actions = [(C, C)] * 198 + [(D, C), (D, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, match_attributes={"length": 200})
        # But only if the tournament is known
        actions = [(C, C)] * 202
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, match_attributes={"length": -1})


class TestDoubleCrosser(TestBackStabber):
    """
    Behaves like BackStabber except when its alternate strategy is triggered.
    The alternate strategy is triggered when opponent did not defect in the first 7 rounds, and
    8 <= the current round <= 180.
    """
    name = "DoubleCrosser: ('D', 'D')"
    player = axelrod.DoubleCrosser
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': {'length'},
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_when_alt_strategy_is_triggered(self):
        """
        The alternate strategy is if opponent's last two plays were defect, then defect. Otherwise, cooperate.
        """
        starting_cooperation = [C] * 7
        starting_rounds = [(C, C)] * 7

        opponent_actions = starting_cooperation + [D, D, C, D]
        expected_actions = starting_rounds + [(C, D), (C, D), (D, C), (C, D)]
        self.versus_test(axelrod.MockPlayer(actions=opponent_actions), expected_actions=expected_actions,
                         match_attributes={"length": 200})

        opponent_actions = starting_cooperation + [D, D, D, D, C, D]
        expected_actions = starting_rounds + [(C, D), (C, D), (D, D), (D, D), (D, C), (C, D)]
        self.versus_test(axelrod.MockPlayer(actions=opponent_actions), expected_actions=expected_actions,
                         match_attributes={"length": 200})

    def test_starting_defect_keeps_alt_strategy_from_triggering(self):
        opponent_actions_suffix = [C, D, C, D, D] + 3 * [C]
        expected_actions_suffix = [(C, C), (C, D), (C, C), (C, D), (C, D)] + 3 * [(D, C)]

        defects_on_first = [D] + [C] * 6
        defects_on_first_actions = [(C, D)] + [(C, C)] * 6
        self.versus_test(axelrod.MockPlayer(actions=defects_on_first + opponent_actions_suffix),
                         expected_actions=defects_on_first_actions + expected_actions_suffix,
                         match_attributes={"length": 200})

        defects_in_middle = [C, C, C, D, C, C, C]
        defects_in_middle_actions = [(C, C), (C, C), (C, C), (C, D), (C, C), (C, C), (C, C)]
        self.versus_test(axelrod.MockPlayer(actions=defects_in_middle + opponent_actions_suffix),
                         expected_actions=defects_in_middle_actions + expected_actions_suffix,
                         match_attributes={"length": 200})

        defects_on_last = [C] * 6 + [D]
        defects_on_last_actions = [(C, C)] * 6 + [(C, D)]
        self.versus_test(axelrod.MockPlayer(actions=defects_on_last + opponent_actions_suffix),
                         expected_actions=defects_on_last_actions + expected_actions_suffix,
                         match_attributes={"length": 200})

    def test_alt_strategy_stops_after_round_180(self):
        one_eighty_opponent_actions = [C] * 8 + [C, D] * 86
        one_eighty_expected_actions = [(C, C)] * 8 + [(C, C), (C, D)] * 86
        opponent_actions = one_eighty_opponent_actions + [C] * 6
        expected_actions = one_eighty_expected_actions + [(D, C)] * 6
        self.versus_test(axelrod.MockPlayer(actions=opponent_actions), expected_actions=expected_actions,
                         match_attributes={"length": 200})


class TestModuleMethods(unittest.TestCase):

    def setUp(self):
        self.player = Player()

    def update_history(self, history_list):
        for move in history_list:
            update_history(self.player, move)

    def test_update_history(self):
        self.assertEqual(self.player.history, [])
        self.assertEqual(self.player.defections, 0)

        self.update_history([D, D, C])

        self.assertEqual(self.player.history, [D, D, C])
        self.assertEqual(self.player.defections, 2)

        self.player.reset()
        self.update_history([D])
        self.assertEqual(self.player.history, [D])
        self.assertEqual(self.player.defections, 1)

    def test_backstabber_strategy_no_history(self):
        self.assertEqual(C, backstabber._backstabber_strategy(self.player))

    def test_backstabber_strategy_three_defections(self):
        self.update_history([D, D, D])
        self.assertEqual(C, backstabber._backstabber_strategy(self.player))

    def test_backstabber_strategy_four_defections(self):
        self.update_history([D, D, D, D])
        self.assertEqual(D, backstabber._backstabber_strategy(self.player))

    def test_alt_strategy_no_history_one_history_returns_C(self):
        self.assertEqual(C, backstabber._alt_strategy(self.player))

        self.update_history([D])
        self.assertEqual(C, backstabber._alt_strategy(self.player))

    def test_alt_strategy_returns_D(self):
        self.update_history([C, C, D, D])
        self.assertEqual(D, backstabber._alt_strategy(self.player))

        self.player.reset()
        self.update_history([D, D, D])
        self.assertEqual(D, backstabber._alt_strategy(self.player))

    def test_alt_strategy_returns_C(self):
        self.update_history([D, D, D, C])
        self.assertEqual(C, backstabber._alt_strategy(self.player))

    def test_opponent_defected_in_first_n_rounds(self):
        self.update_history([C, C, C, C, D, C])
        self.assertTrue(backstabber._opponent_defected_in_first_n_rounds(self.player, 10))
        self.assertTrue(backstabber._opponent_defected_in_first_n_rounds(self.player, 6))
        self.assertTrue(backstabber._opponent_defected_in_first_n_rounds(self.player, 5))

        self.assertFalse(backstabber._opponent_defected_in_first_n_rounds(self.player, 4))

    def test_opponent_triggers_alt_strategy_false_by_defected_in_first_n_rounds(self):
        last_of_first_n_rounds = 7
        history = [C if rnd != last_of_first_n_rounds else D for rnd in range(1, 20)]
        self.update_history(history)
        self.assertFalse(backstabber._opponent_triggers_alt_strategy(self.player))

    def test_opponent_triggers_alt_strategy_false_by_before_round_eight(self):
        current_round = 7
        history = [C] * (current_round - 1)
        self.update_history(history)
        self.assertFalse(backstabber._opponent_triggers_alt_strategy(self.player))

    def test_opponent_triggers_alt_strategy_false_by_after_round_one_eighty(self):
        current_round = 181
        history = [C] * (current_round - 1)
        self.update_history(history)
        self.assertFalse(backstabber._opponent_triggers_alt_strategy(self.player))

    def test_opponent_triggers_alt_strategy_true_edge_case_high(self):
        current_round = 180
        history = [C] * (current_round - 1)
        self.update_history(history)
        self.assertTrue(backstabber._opponent_triggers_alt_strategy(self.player))

    def test_opponent_triggers_alt_strategy_true_edge_case_low(self):
        current_round = 8
        history = [C] * (current_round - 1)
        self.update_history(history)
        self.assertTrue(backstabber._opponent_triggers_alt_strategy(self.player))
