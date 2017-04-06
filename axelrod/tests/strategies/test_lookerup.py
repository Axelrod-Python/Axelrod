"""Test for the Looker Up strategy."""
import unittest
import copy

import axelrod
from axelrod.strategies.lookerup import (get_last_n_plays, make_keys_into_action_keys, create_lookup_table_keys,
                                         create_lookup_table_from_tuple, create_lookup_table_from_string, ActionKeys)
from .test_player import TestPlayer, TestMatch

from axelrod.actions import str_to_actions

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestModuleLevelFunctions(unittest.TestCase):

    def test_action_keys_equals_tuple(self):
        self.assertEqual(ActionKeys(1, 2, 3), (1, 2, 3))

    def test_actions_keys_assign_values(self):
        self.assertEqual(ActionKeys(op_plays=2, self_plays=1, op_initial_plays=3), ActionKeys(1, 2, 3))

    def test_make_keys_into_action_keys(self):
        old = {((C, D), (C,), ()): 1,
               ((D, D), (D,), ()): 2}
        new = make_keys_into_action_keys(old)
        self.assertNotIsInstance(next(iter(old)), ActionKeys)
        self.assertIsInstance(next(iter(new)), ActionKeys)
        self.assertTrue(new.__eq__(old))
        self.assertTrue(old.__eq__(new))

    def test_make_keys_into_action_keys_always_returns_new_dict(self):
        old = {ActionKeys((C, D), (C,), ()): 1,
               ActionKeys((D, D), (D,), ()): 2}
        self.assertIsNot(old, make_keys_into_action_keys(old))

    def test_create_lookup_table_keys(self):
        expected = [
            ActionKeys((C, C), (C,), ()),
            ActionKeys((C, C), (D,), ()),
            ActionKeys((C, D), (C,), ()),
            ActionKeys((C, D), (D,), ()),
            ActionKeys((D, C), (C,), ()),
            ActionKeys((D, C), (D,), ()),
            ActionKeys((D, D), (C,), ()),
            ActionKeys((D, D), (D,), ())
        ]
        actual = create_lookup_table_keys(plays=2, op_plays=1, op_initial_plays=0)
        self.assertEqual(actual, expected)
        self.assertIsInstance(actual[0], ActionKeys)

    def test_create_lookup_table_from_tuple(self):
        expected = {
            ActionKeys((C,), (C,), (C,)): C,
            ActionKeys((C,), (C,), (D,)): C,
            ActionKeys((C,), (D,), (C,)): D,
            ActionKeys((C,), (D,), (D,)): C,
            ActionKeys((D,), (C,), (C,)): C,
            ActionKeys((D,), (C,), (D,)): D,
            ActionKeys((D,), (D,), (C,)): C,
            ActionKeys((D,), (D,), (D,)): C
        }
        actual = create_lookup_table_from_tuple(1, 1, 1, str_to_actions('CCDCCDCC'))
        self.assertEqual(actual, expected)
        self.assertIsInstance(next(iter(actual)), ActionKeys)

    def test_create_lookup_table_from_tuple_raises_error_when_keys_and_values_not_same_len(self):
        with self.assertRaises(ValueError):
            create_lookup_table_from_tuple(2, 2, 2, str_to_actions('CCC'))

    def test_create_lookup_table_from_string(self):
        expected = {
            ActionKeys((C,), (C,), (C,)): C,
            ActionKeys((C,), (C,), (D,)): C,
            ActionKeys((C,), (D,), (C,)): D,
            ActionKeys((C,), (D,), (D,)): C,
            ActionKeys((D,), (C,), (C,)): C,
            ActionKeys((D,), (C,), (D,)): D,
            ActionKeys((D,), (D,), (C,)): C,
            ActionKeys((D,), (D,), (D,)): C
        }
        actual = create_lookup_table_from_string(1, 1, 1, 'CCDCCDCC')
        self.assertEqual(actual, expected)
        self.assertIsInstance(next(iter(actual)), ActionKeys)

    def test_create_lookup_table_from_string_raises_error_when_keys_and_values_not_same_len(self):
        with self.assertRaises(ValueError):
            create_lookup_table_from_string(2, 2, 2, 'CCC')

    def test_get_last_n_plays(self):
        player = axelrod.Player()
        player.history = [C, D, C]
        self.assertEqual(get_last_n_plays(player, 0), ())
        self.assertEqual(get_last_n_plays(player, 2), (D, C))


class TestLookerUp(TestPlayer):

    name = "LookerUp"
    player = axelrod.LookerUp

    expected_classifier = {
        'memory_depth': 1,  # Default TFT
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    expected_class_classifier = copy.copy(expected_classifier)
    expected_class_classifier['memory_depth'] = float('inf')

    def test_default_init(self):
        player = self.player()
        expected = {((), (D, ), ()): D,
                    ((), (C, ), ()): C}
        self.assertEqual(player.lookup_table, expected)
        self.assertEqual(player.initial_actions, (C,))

    def test_init_with_empty_dict_makes_default(self):
        player = axelrod.LookerUp(lookup_table=dict())
        expected = {((), (D,), ()): D,
                    ((), (C,), ()): C}
        self.assertEqual(player.lookup_table, expected)
        self.assertEqual(player.initial_actions, (C,))

    def test_pattern_and_params_init(self):
        pattern = "CCCC"
        parameters = (1, 1, 0)
        player = axelrod.LookerUp(lookup_pattern=pattern, parameters=parameters)
        expected_lookup_table = {
            ((C,), (D,), ()): C,
            ((D,), (D,), ()): C,
            ((C,), (C,), ()): C,
            ((D,), (C,), ()): C
        }
        self.assertEqual(player.lookup_table, expected_lookup_table)

    def test_patter_and_params_init_only_happens_if_both_are_present(self):
        default = {((), (D,), ()): D,
                   ((), (C,), ()): C}
        pattern = "CC"
        parameters = (0, 1, 0)
        player1 = axelrod.LookerUp(lookup_pattern=pattern)
        player2 = axelrod.LookerUp(parameters=parameters)

        self.assertEqual(player1.lookup_table, default)
        self.assertEqual(player2.lookup_table, default)

    def test_lookup_table_init(self):
        lookup_table = {
            ((C,), (D,), ()): C,
            ((D,), (D,), ()): C,
            ((C,), (C,), ()): C,
            ((D,), (C,), ()): C
        }
        player = axelrod.LookerUp(lookup_table=lookup_table)
        self.assertEqual(player.lookup_table, lookup_table)
        self.assertIsInstance(next(iter(player.lookup_table)), ActionKeys)

    def test_lookup_table_init_supersedes_pattern_init(self):
        lookup_table = {
            ((C,), (D,), ()): D,
            ((D,), (D,), ()): D,
            ((C,), (C,), ()): D,
            ((D,), (C,), ()): D
        }
        pattern = "CCCCCCCC"
        parameters = (1, 1, 1)
        player = axelrod.LookerUp(lookup_table=lookup_table, lookup_pattern=pattern, parameters=parameters)

        self.assertEqual(player.lookup_table, lookup_table)

    def test_init_initial_actions_set_to_max_table_depth(self):
        initial_actions = (D, D, D)
        table_depth_one = axelrod.LookerUp(initial_actions=initial_actions)
        self.assertEqual(table_depth_one.initial_actions, (D,))

    def test_init_initial_actions_makes_up_missing_actions_with_c(self):
        initial_acitons = (D,)
        table_depth_three = axelrod.LookerUp(initial_actions=initial_acitons, lookup_pattern='CCCCCCCC',
                                             parameters=(3, 0, 0))
        self.assertEqual(table_depth_three.initial_actions, (D, C, C))

    def test_init_raises_error_for_bad_lookup_table_table_keys_do_not_match_each_other(self):
        table = {((C,), (C,), ()): C, ((D, D), (D, D), ()): C}
        with self.assertRaises(ValueError):
            axelrod.LookerUp(lookup_table=table)

    def test_init_raises_error_for_bad_lookup_table_table_keys_do_not_cover_all_combinations(self):
        table = {((C,), (C,), ()): C, ((D,), (D,), ()): C}
        with self.assertRaises(ValueError):
            axelrod.LookerUp(lookup_table=table)

    def test_strategy(self):
        self.first_play_test(C)
        self.second_play_test(C, D, C, D)  # TFT

        actions = [(C, C), (C, D), (D, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        lookup_table = {((), (), ()): C}
        actions = [(C, D)] * 5
        self.versus_test(axelrod.Defector(), expected_actions=actions, init_kwargs={'lookup_table': lookup_table})

    def test_defector_table(self):
        """
        Testing a lookup table that always defects IF there is enough history.
        """
        defector_table = {((C, ), (D, ), ()): D,
                          ((D, ), (D, ), ()): D,
                          ((C, ), (C, ), ()): D,
                          ((D, ), (C, ), ()): D}
        actions = [(C, C)] + [(D, D), (D, C)] * 4
        self.versus_test(axelrod.Alternator(), expected_actions=actions, init_kwargs={'lookup_table': defector_table})

    def test_zero_tables(self):
        """Test the corner case where n=0."""
        anti_tft_pattern = "DC"
        parameters = (0, 1, 0)

        tft_vs_alternator = [(C, C)] + [(D, D), (C, C)] * 5
        self.versus_test(axelrod.Alternator(), expected_actions=tft_vs_alternator,
                         init_kwargs={'parameters': parameters, 'lookup_pattern': anti_tft_pattern})

    def test_opponent_starting_moves_table(self):
        """A lookup table that always repeats the opponent's first move."""
        first_move_table = {((), (), (C,)): C,
                            ((), (), (D,)): D}

        vs_alternator = [(C, C), (C, D)] * 5
        self.versus_test(axelrod.Alternator(), expected_actions=vs_alternator,
                         init_kwargs={'lookup_table': first_move_table})

        vs_initial_defector = [(C, D)] + [(D, C), (D, D)] * 10
        opponent = axelrod.MockPlayer(actions=[D, C])
        self.versus_test(opponent, expected_actions=vs_initial_defector, init_kwargs={'lookup_table': first_move_table})


class TestEvolvedLookerUp1_1_1(TestPlayer):

    name = "EvolvedLookerUp1_1_1"
    player = axelrod.EvolvedLookerUp1_1_1

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_new_data(self):
        original_data = {
            ('C', 'C', 'C'): C,
            ('C', 'C', 'D'): D,
            ('C', 'D', 'C'): D,
            ('C', 'D', 'D'): D,
            ('D', 'C', 'C'): D,
            ('D', 'C', 'D'): D,
            ('D', 'D', 'C'): C,
            ('D', 'D', 'D'): D}
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_table, converted_original)

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_vs_initial_defector(self):
        opponent = [D, C, C, D, D, C]
        expected = [(C, D), (D, C), (C, C), (D, D), (D, D), (D, C)]
        self.versus_test(axelrod.MockPlayer(actions=opponent), expected_actions=expected)

    def test_vs_initial_cooperator(self):
        opponent = [C, D, D, C, C, D]
        expected = [(C, C), (C, D), (D, D), (D, C), (D, C), (D, D)]
        self.versus_test(axelrod.MockPlayer(actions=opponent), expected_actions=expected)


class TestEvolvedLookerUp2_2_2(TestPlayer):

    name = "EvolvedLookerUp2_2_2"
    player = axelrod.EvolvedLookerUp2_2_2

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_new_data(self):
        original_data = {
            ('CC', 'CC', 'CC'): C,
            ('CC', 'CC', 'CD'): D,
            ('CC', 'CC', 'DC'): C,
            ('CC', 'CC', 'DD'): C,
            ('CC', 'CD', 'CC'): D,
            ('CC', 'CD', 'CD'): C,
            ('CC', 'CD', 'DC'): C,
            ('CC', 'CD', 'DD'): C,
            ('CC', 'DC', 'CC'): D,
            ('CC', 'DC', 'CD'): C,
            ('CC', 'DC', 'DC'): D,
            ('CC', 'DC', 'DD'): D,
            ('CC', 'DD', 'CC'): D,
            ('CC', 'DD', 'CD'): C,
            ('CC', 'DD', 'DC'): C,
            ('CC', 'DD', 'DD'): C,
            ('CD', 'CC', 'CC'): D,
            ('CD', 'CC', 'CD'): C,
            ('CD', 'CC', 'DC'): D,
            ('CD', 'CC', 'DD'): D,
            ('CD', 'CD', 'CC'): D,
            ('CD', 'CD', 'CD'): D,
            ('CD', 'CD', 'DC'): D,
            ('CD', 'CD', 'DD'): D,
            ('CD', 'DC', 'CC'): D,
            ('CD', 'DC', 'CD'): C,
            ('CD', 'DC', 'DC'): D,
            ('CD', 'DC', 'DD'): D,
            ('CD', 'DD', 'CC'): D,
            ('CD', 'DD', 'CD'): C,
            ('CD', 'DD', 'DC'): D,
            ('CD', 'DD', 'DD'): C,
            ('DC', 'CC', 'CC'): D,
            ('DC', 'CC', 'CD'): D,
            ('DC', 'CC', 'DC'): D,
            ('DC', 'CC', 'DD'): D,
            ('DC', 'CD', 'CC'): C,
            ('DC', 'CD', 'CD'): C,
            ('DC', 'CD', 'DC'): D,
            ('DC', 'CD', 'DD'): C,
            ('DC', 'DC', 'CC'): C,
            ('DC', 'DC', 'CD'): C,
            ('DC', 'DC', 'DC'): C,
            ('DC', 'DC', 'DD'): D,
            ('DC', 'DD', 'CC'): D,
            ('DC', 'DD', 'CD'): D,
            ('DC', 'DD', 'DC'): D,
            ('DC', 'DD', 'DD'): C,
            ('DD', 'CC', 'CC'): C,
            ('DD', 'CC', 'CD'): D,
            ('DD', 'CC', 'DC'): D,
            ('DD', 'CC', 'DD'): D,
            ('DD', 'CD', 'CC'): D,
            ('DD', 'CD', 'CD'): C,
            ('DD', 'CD', 'DC'): C,
            ('DD', 'CD', 'DD'): D,
            ('DD', 'DC', 'CC'): C,
            ('DD', 'DC', 'CD'): D,
            ('DD', 'DC', 'DC'): D,
            ('DD', 'DC', 'DD'): D,
            ('DD', 'DD', 'CC'): D,
            ('DD', 'DD', 'CD'): D,
            ('DD', 'DD', 'DC'): D,
            ('DD', 'DD', 'DD'): D}
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_table, converted_original)

    def test_init(self):
        # Check for a few known keys

        known_pairs = {ActionKeys(self_plays=(C, C), op_plays=(C, D), op_initial_plays=(D, D)): D,
                       ActionKeys(self_plays=(C, D), op_plays=(C, D), op_initial_plays=(D, C)): C,
                       ActionKeys(self_plays=(C, D), op_plays=(C, D), op_initial_plays=(D, D)): C,
                       ActionKeys(self_plays=(D, C), op_plays=(D, C), op_initial_plays=(D, C)): C,
                       ActionKeys(self_plays=(D, D), op_plays=(C, C), op_initial_plays=(D, D)): D,
                       ActionKeys(self_plays=(C, C), op_plays=(D, C), op_initial_plays=(C, D)): D,
                       }
        player = self.player()
        for k, v in known_pairs.items():
            self.assertEqual(player.lookup_table[k], v)

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)
        self.second_play_test(C, C, C, C)

    def test_vs_initial_defector(self):
        opponent = [D, D] + [C, D] * 3
        expected = [(C, D), (C, D)] + [(D, C), (C, D)] * 3
        self.versus_test(axelrod.MockPlayer(actions=opponent), expected_actions=expected)

    def test_vs_initial_d_c(self):
        opponent = [D, C] + [C, D] * 3
        expected = [(C, D), (C, C)] + [(D, C), (C, D), (C, C), (D, D), (C, C), (C, D)]
        self.versus_test(axelrod.MockPlayer(actions=opponent), expected_actions=expected)


class TestWinner12(TestPlayer):
    name = "Winner12"
    player = axelrod.Winner12

    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    expected_class_classifier = copy.copy(expected_classifier)
    expected_class_classifier['memory_depth'] = float('inf')

    def test_new_data(self):
        original_data = {
            ('', 'C', 'CC'): C,
            ('', 'C', 'CD'): D,
            ('', 'C', 'DC'): C,
            ('', 'C', 'DD'): D,
            ('', 'D', 'CC'): D,
            ('', 'D', 'CD'): C,
            ('', 'D', 'DC'): D,
            ('', 'D', 'DD'): D}
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_table, converted_original)

    def test_strategy(self):
        """Starts by cooperating twice."""
        self.first_play_test(C)
        self.second_play_test(C, C, C, C)
        vs_alternator = [(C, C), (C, D), (D, C), (D, D)] * 5
        self.versus_test(axelrod.Alternator(), expected_actions=vs_alternator)

        self.versus_test(axelrod.Cooperator(), expected_actions=[(C, C)] * 10)

        self.versus_test(axelrod.Defector(), expected_actions=([(C, D), (C, D)] + [(D, D)] * 10))


class TestWinner21(TestPlayer):
    name = "Winner21"
    player = axelrod.Winner21

    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    expected_class_classifier = copy.copy(expected_classifier)
    expected_class_classifier['memory_depth'] = float('inf')

    def test_new_data(self):
        original_data = {
            ('', 'C', 'CC'): C,
            ('', 'C', 'CD'): D,
            ('', 'C', 'DC'): C,
            ('', 'C', 'DD'): D,
            ('', 'D', 'CC'): C,
            ('', 'D', 'CD'): D,
            ('', 'D', 'DC'): D,
            ('', 'D', 'DD'): D}
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_table, converted_original)

    def test_strategy(self):
        """Starts by cooperating twice."""
        self.first_play_test(D)
        self.second_play_test(C, C, C, C)

        vs_alternator = [(D, C), (C, D)] + [(D, C), (D, D)] * 5
        self.versus_test(axelrod.Alternator(), expected_actions=vs_alternator)

        self.versus_test(axelrod.Cooperator(), expected_actions=[(D, C)] + [(C, C)] * 10)

        self.versus_test(axelrod.Defector(), expected_actions=([(D, D), (C, D)] + [(D, D)] * 10))


class TestDictConversionFunctions(unittest.TestCase):

    def test_convert_key(self):
        opponent_starting_plays = ''
        player_last_plays = 'CC'
        opponent_last_plays = 'D'
        old_key = (opponent_starting_plays, player_last_plays, opponent_last_plays)

        new_key = ActionKeys(self_plays=(C, C), op_plays=(D,), op_initial_plays=())

        self.assertEqual(new_key, convert_key(old_key))

    def test_convert_original_to_current(self):
        expected = {
            ActionKeys(self_plays=(C, C), op_plays=(D,), op_initial_plays=()): C,
            ActionKeys(self_plays=(D, ), op_plays=(D, D), op_initial_plays=(C,)): D
        }
        original = {('', 'CC', 'D'): C, ('C', 'D', 'DD'): D}
        self.assertEqual(expected, convert_original_to_current(original))


def convert_original_to_current(original_data: dict) -> dict:
    return {convert_key(key): value for key, value in original_data.items()}


def convert_key(old_key: tuple) -> ActionKeys:
    opponent_start, player, opponent = old_key
    return ActionKeys(self_plays=str_to_actions(player),
                      op_plays=str_to_actions(opponent),
                      op_initial_plays=str_to_actions(opponent_start))
