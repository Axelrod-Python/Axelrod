"""Test for the Looker Up strategy."""
import copy
import unittest

import axelrod
from axelrod.action import str_to_actions
from axelrod.strategies.lookerup import (
    LookupTable,
    Plays,
    create_lookup_table_keys,
    make_keys_into_plays,
)

from .test_player import TestPlayer
from .test_evolvable_player import TestEvolvablePlayer

C, D = axelrod.Action.C, axelrod.Action.D


class TestEvolvableLookerUp(TestEvolvablePlayer):
    name = "EvolvableLookerUp"
    player_class = axelrod.EvolvableLookerUp
    init_parameters = {"parameters": (1, 1, 1)}


class TestEvolvableLookerUp2(TestEvolvablePlayer):
    name = "EvolvableLookerUp"
    player_class = axelrod.EvolvableLookerUp
    init_parameters = {"parameters": (2, 1, 3)}


class TestEvolvableLookerUp3(TestEvolvablePlayer):
    name = "EvolvableLookerUp"
    player_class = axelrod.EvolvableLookerUp
    init_parameters = {
        "initial_actions": (C, C,),
        "lookup_dict":  {
            ((C, C), (C,), ()): C,
            ((C, C), (D,), ()): D,
            ((C, D), (C,), ()): D,
            ((C, D), (D,), ()): C,
            ((D, C), (C,), ()): C,
            ((D, C), (D,), ()): D,
            ((D, D), (C,), ()): D,
            ((D, D), (D,), ()): C,
        }
    }


class TestLookupTable(unittest.TestCase):
    lookup_dict = {
        ((C, C), (C,), ()): C,
        ((C, C), (D,), ()): D,
        ((C, D), (C,), ()): D,
        ((C, D), (D,), ()): C,
        ((D, C), (C,), ()): C,
        ((D, C), (D,), ()): D,
        ((D, D), (C,), ()): D,
        ((D, D), (D,), ()): C,
    }

    def test_init(self):

        table = LookupTable(self.lookup_dict)

        self.assertEqual(table.table_depth, 2)
        self.assertEqual(table.player_depth, 2)
        self.assertEqual(table.op_depth, 1)
        self.assertEqual(table.op_openings_depth, 0)
        self.assertEqual(
            table.dictionary,
            {
                Plays(self_plays=(C, C), op_plays=(C,), op_openings=()): C,
                Plays(self_plays=(C, C), op_plays=(D,), op_openings=()): D,
                Plays(self_plays=(C, D), op_plays=(C,), op_openings=()): D,
                Plays(self_plays=(C, D), op_plays=(D,), op_openings=()): C,
                Plays(self_plays=(D, C), op_plays=(C,), op_openings=()): C,
                Plays(self_plays=(D, C), op_plays=(D,), op_openings=()): D,
                Plays(self_plays=(D, D), op_plays=(C,), op_openings=()): D,
                Plays(self_plays=(D, D), op_plays=(D,), op_openings=()): C,
            },
        )
        self.assertIsInstance(next(iter(table.dictionary)), Plays)

    def test_init_raises_error_when_keys_for_lookup_dict_do_not_match(self):
        lookup_dict = {((C,), (C,), ()): C, ((D, D), (D, D), ()): C}
        with self.assertRaises(ValueError):
            LookupTable(lookup_dict=lookup_dict)

    def test_init_raises_error_keys_do_not_cover_all_combinations(self):
        lookup_dict = {((C,), (C,), ()): C, ((D,), (D,), ()): C}
        with self.assertRaises(ValueError):
            LookupTable(lookup_dict=lookup_dict)

    def test_from_pattern(self):
        pattern = (C, D, D, C, C, D, D, C)
        table = LookupTable.from_pattern(
            pattern, player_depth=2, op_depth=1, op_openings_depth=0
        )
        self.assertEqual(table.dictionary, make_keys_into_plays(self.lookup_dict))

    def test_from_pattern_raises_error_pattern_len_ne_dict_size(self):
        too_big = (C,) * 17
        too_small = (C,) * 15
        just_right = (C,) * 16
        with self.assertRaises(ValueError):
            LookupTable.from_pattern(too_big, 2, 2, 0)
        with self.assertRaises(ValueError):
            LookupTable.from_pattern(too_small, 2, 2, 0)
        self.assertIsInstance(
            LookupTable.from_pattern(just_right, 2, 2, 0), LookupTable
        )

    def test_dictionary_property_returns_new_dict_object(self):
        table = LookupTable(lookup_dict=self.lookup_dict)
        self.assertIsNot(table.dictionary, table.dictionary)

    def test_display_default(self):
        table = LookupTable.from_pattern(
            (C,) * 8, player_depth=2, op_depth=0, op_openings_depth=1
        )
        self.assertEqual(
            table.display(),
            (
                "op_openings|self_plays | op_plays  \n"
                + "     C     ,   C, C    ,           : C,\n"
                + "     C     ,   C, D    ,           : C,\n"
                + "     C     ,   D, C    ,           : C,\n"
                + "     C     ,   D, D    ,           : C,\n"
                + "     D     ,   C, C    ,           : C,\n"
                + "     D     ,   C, D    ,           : C,\n"
                + "     D     ,   D, C    ,           : C,\n"
                + "     D     ,   D, D    ,           : C,\n"
            ),
        )

    def test_display_assign_order(self):
        table = LookupTable.from_pattern(
            (C,) * 8, player_depth=0, op_depth=3, op_openings_depth=0
        )
        self.assertEqual(
            table.display(sort_by=("op_openings", "op_plays", "self_plays")),
            (
                "op_openings| op_plays  |self_plays \n"
                + "           ,  C, C, C  ,           : C,\n"
                + "           ,  C, C, D  ,           : C,\n"
                + "           ,  C, D, C  ,           : C,\n"
                + "           ,  C, D, D  ,           : C,\n"
                + "           ,  D, C, C  ,           : C,\n"
                + "           ,  D, C, D  ,           : C,\n"
                + "           ,  D, D, C  ,           : C,\n"
                + "           ,  D, D, D  ,           : C,\n"
            ),
        )

    def test_equality_true(self):
        table_a = LookupTable(self.lookup_dict)
        table_b = LookupTable(self.lookup_dict)
        self.assertTrue(table_a.__eq__(table_b))

    def test_equality_false(self):
        table_a = LookupTable.from_pattern((C, D), 1, 0, 0)
        table_b = LookupTable.from_pattern((D, C), 1, 0, 0)
        table_c = LookupTable.from_pattern((C, D), 0, 1, 0)
        self.assertFalse(table_a.__eq__(table_b))
        self.assertFalse(table_a.__eq__(table_c))
        self.assertFalse(table_a.__eq__(table_a.dictionary))

    def test_not_equal(self):
        table_a = LookupTable(self.lookup_dict)
        table_b = LookupTable(self.lookup_dict)
        not_equal = LookupTable.from_pattern((C, C), 1, 0, 0)
        self.assertFalse(table_a.__ne__(table_b))
        self.assertTrue(table_a.__ne__(not_equal))


class TestLookupTableHelperFunctions(unittest.TestCase):
    def test_plays_equals_tuple(self):
        self.assertEqual(Plays(1, 2, 3), (1, 2, 3))

    def test_plays_assign_values(self):
        self.assertEqual(Plays(op_plays=2, self_plays=1, op_openings=3), Plays(1, 2, 3))

    def test_make_keys_into_plays(self):
        old = {((C, D), (C,), ()): 1, ((D, D), (D,), ()): 2}
        new = make_keys_into_plays(old)
        self.assertNotIsInstance(next(iter(old)), Plays)
        self.assertIsInstance(next(iter(new)), Plays)
        self.assertTrue(new.__eq__(old))
        self.assertTrue(old.__eq__(new))

    def test_make_keys_into_plays_always_returns_new_dict(self):
        old = {Plays((C, D), (C,), ()): 1, Plays((D, D), (D,), ()): 2}
        self.assertIsNot(old, make_keys_into_plays(old))

    def test_create_lookup_table_keys(self):
        expected = [
            Plays((C, C), (C,), ()),
            Plays((C, C), (D,), ()),
            Plays((C, D), (C,), ()),
            Plays((C, D), (D,), ()),
            Plays((D, C), (C,), ()),
            Plays((D, C), (D,), ()),
            Plays((D, D), (C,), ()),
            Plays((D, D), (D,), ()),
        ]
        actual = create_lookup_table_keys(
            player_depth=2, op_depth=1, op_openings_depth=0
        )
        self.assertEqual(actual, expected)
        self.assertIsInstance(actual[0], Plays)


class TestLookerUp(TestPlayer):

    name = "LookerUp"
    player = axelrod.LookerUp

    expected_classifier = {
        "memory_depth": 1,  # Default TFT
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    expected_class_classifier = copy.copy(expected_classifier)
    expected_class_classifier["memory_depth"] = float("inf")

    def test_default_init(self):
        player = self.player()
        expected = {Plays((), (D,), ()): D, Plays((), (C,), ()): C}
        self.assertEqual(player.lookup_dict, expected)
        self.assertEqual(player.initial_actions, (C,))

    def test_pattern_and_params_init_pattern_is_string(self):
        pattern = "CCCC"
        parameters = Plays(1, 1, 0)
        player = axelrod.LookerUp(pattern=pattern, parameters=parameters)
        expected_lookup_table = {
            Plays((C,), (D,), ()): C,
            Plays((D,), (D,), ()): C,
            Plays((C,), (C,), ()): C,
            Plays((D,), (C,), ()): C,
        }
        self.assertEqual(player.lookup_dict, expected_lookup_table)

    def test_pattern_and_params_init_pattern_is_tuple(self):
        pattern = (C, C, C, C)
        parameters = Plays(1, 1, 0)
        player = axelrod.LookerUp(pattern=pattern, parameters=parameters)
        expected_lookup_table = {
            Plays((C,), (D,), ()): C,
            Plays((D,), (D,), ()): C,
            Plays((C,), (C,), ()): C,
            Plays((D,), (C,), ()): C,
        }
        self.assertEqual(player.lookup_dict, expected_lookup_table)

    def test_pattern_and_params_init_can_still_use_regular_tuple(self):
        pattern = (C, C)
        parameters = (1, 0, 0)
        player = axelrod.LookerUp(pattern=pattern, parameters=parameters)
        expected_lookup_table = {Plays((C,), (), ()): C, Plays((D,), (), ()): C}
        self.assertEqual(player.lookup_dict, expected_lookup_table)

    def test_pattern_and_params_init_only_happens_if_both_are_present(self):
        default = {Plays((), (D,), ()): D, Plays((), (C,), ()): C}
        pattern = "CC"
        parameters = Plays(self_plays=0, op_plays=1, op_openings=0)
        player1 = axelrod.LookerUp(pattern=pattern)
        player2 = axelrod.LookerUp(parameters=parameters)

        self.assertEqual(player1.lookup_dict, default)
        self.assertEqual(player2.lookup_dict, default)

    def test_lookup_table_init(self):
        lookup_table = {
            ((C,), (D,), ()): C,
            ((D,), (D,), ()): C,
            ((C,), (C,), ()): C,
            ((D,), (C,), ()): C,
        }
        player = axelrod.LookerUp(lookup_dict=lookup_table)
        self.assertEqual(player.lookup_dict, lookup_table)
        self.assertIsInstance(next(iter(player.lookup_dict)), Plays)

    def test_lookup_table_init_supersedes_pattern_init(self):
        lookup_table = {
            ((C,), (D,), ()): D,
            ((D,), (D,), ()): D,
            ((C,), (C,), ()): D,
            ((D,), (C,), ()): D,
        }
        pattern = "CCCCCCCC"
        parameters = Plays(self_plays=1, op_plays=1, op_openings=1)
        player = axelrod.LookerUp(
            lookup_dict=lookup_table, pattern=pattern, parameters=parameters
        )

        self.assertEqual(player.lookup_dict, lookup_table)

    def test_init_raises_errors(self):
        mismatch_dict = {((C,), (C,), ()): C, ((D, D), (D, D), ()): C}
        with self.assertRaises(ValueError):
            axelrod.LookerUp(lookup_dict=mismatch_dict)

        incomplete_lookup_dict = {((C,), (C,), ()): C, ((D,), (D,), ()): C}
        with self.assertRaises(ValueError):
            axelrod.LookerUp(lookup_dict=incomplete_lookup_dict)

        too_short_pattern = "CC"
        with self.assertRaises(ValueError):
            axelrod.LookerUp(pattern=too_short_pattern, parameters=(3, 3, 3))

    def test_initial_actions_set_to_max_table_depth(self):
        initial_actions = (D, D, D)
        table_depth_one = axelrod.LookerUp(initial_actions=initial_actions)
        self.assertEqual(table_depth_one.initial_actions, (D,))

    def test_initial_actions_makes_up_missing_actions_with_c(self):
        initial_actions = (D,)
        table_depth_three = axelrod.LookerUp(
            initial_actions=initial_actions,
            pattern="CCCCCCCC",
            parameters=Plays(3, 0, 0),
        )
        self.assertEqual(table_depth_three.initial_actions, (D, C, C))

    def test_set_memory_depth(self):
        mem_depth_1 = axelrod.LookerUp(pattern="CC", parameters=Plays(1, 0, 0))
        self.assertEqual(mem_depth_1.classifier["memory_depth"], 1)

        mem_depth_3 = axelrod.LookerUp(pattern="C" * 16, parameters=Plays(1, 3, 0))
        self.assertEqual(mem_depth_3.classifier["memory_depth"], 3)

        mem_depth_inf = axelrod.LookerUp(pattern="CC", parameters=Plays(0, 0, 1))
        self.assertEqual(mem_depth_inf.classifier["memory_depth"], float("inf"))

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        actions = [(C, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)

    def test_cooperator_table(self):
        lookup_table = {((), (), ()): C}
        actions = [(C, D)] * 5
        self.versus_test(
            axelrod.Defector(),
            expected_actions=actions,
            init_kwargs={"lookup_dict": lookup_table},
        )

    def test_defector_table_with_initial_cooperate(self):
        """
        Testing a lookup table that always defects IF there is enough history.
        """
        defector_table = {
            ((C,), (D,), ()): D,
            ((D,), (D,), ()): D,
            ((C,), (C,), ()): D,
            ((D,), (C,), ()): D,
        }
        actions = [(C, C)] + [(D, D), (D, C)] * 4
        self.versus_test(
            axelrod.Alternator(),
            expected_actions=actions,
            init_kwargs={"lookup_dict": defector_table},
        )

    def test_zero_tables(self):
        """Test the corner case where n=0."""
        anti_tft_pattern = "DC"
        parameters = Plays(self_plays=0, op_plays=1, op_openings=0)

        tft_vs_alternator = [(C, C)] + [(D, D), (C, C)] * 5
        self.versus_test(
            axelrod.Alternator(),
            expected_actions=tft_vs_alternator,
            init_kwargs={"parameters": parameters, "pattern": anti_tft_pattern},
        )

    def test_opponent_starting_moves_table(self):
        """A lookup table that always repeats the opponent's first move."""
        first_move_table = {((), (), (C,)): C, ((), (), (D,)): D}

        vs_alternator = [(C, C), (C, D)] * 5
        self.versus_test(
            axelrod.Alternator(),
            expected_actions=vs_alternator,
            init_kwargs={"lookup_dict": first_move_table},
        )

        vs_initial_defector = [(C, D)] + [(D, C), (D, D)] * 10
        opponent = axelrod.MockPlayer(actions=[D, C])
        self.versus_test(
            opponent,
            expected_actions=vs_initial_defector,
            init_kwargs={"lookup_dict": first_move_table},
        )

    def test_lookup_table_display(self):
        player = axelrod.LookerUp(
            pattern="CCCC", parameters=Plays(self_plays=2, op_plays=0, op_openings=0)
        )
        self.assertEqual(
            player.lookup_table_display(("self_plays", "op_plays", "op_openings")),
            (
                "self_plays | op_plays  |op_openings\n"
                + "   C, C    ,           ,           : C,\n"
                + "   C, D    ,           ,           : C,\n"
                + "   D, C    ,           ,           : C,\n"
                + "   D, D    ,           ,           : C,\n"
            ),
        )


class TestEvolvedLookerUp1_1_1(TestPlayer):

    name = "EvolvedLookerUp1_1_1"
    player = axelrod.EvolvedLookerUp1_1_1

    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_new_data(self):
        original_data = {
            ("C", "C", "C"): C,
            ("C", "C", "D"): D,
            ("C", "D", "C"): D,
            ("C", "D", "D"): D,
            ("D", "C", "C"): D,
            ("D", "C", "D"): D,
            ("D", "D", "C"): C,
            ("D", "D", "D"): D,
        }
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_dict, converted_original)

    def test_vs_initial_defector(self):
        opponent = [D, C, C, D, D, C]
        expected = [(C, D), (D, C), (C, C), (D, D), (D, D), (D, C)]
        self.versus_test(
            axelrod.MockPlayer(actions=opponent), expected_actions=expected
        )

    def test_vs_initial_cooperator(self):
        opponent = [C, D, D, C, C, D]
        expected = [(C, C), (C, D), (D, D), (D, C), (D, C), (D, D)]
        self.versus_test(
            axelrod.MockPlayer(actions=opponent), expected_actions=expected
        )


class TestEvolvedLookerUp2_2_2(TestPlayer):

    name = "EvolvedLookerUp2_2_2"
    player = axelrod.EvolvedLookerUp2_2_2

    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_new_data(self):
        original_data = {
            ("CC", "CC", "CC"): C,
            ("CC", "CC", "CD"): D,
            ("CC", "CC", "DC"): C,
            ("CC", "CC", "DD"): C,
            ("CC", "CD", "CC"): D,
            ("CC", "CD", "CD"): C,
            ("CC", "CD", "DC"): C,
            ("CC", "CD", "DD"): C,
            ("CC", "DC", "CC"): D,
            ("CC", "DC", "CD"): C,
            ("CC", "DC", "DC"): D,
            ("CC", "DC", "DD"): D,
            ("CC", "DD", "CC"): D,
            ("CC", "DD", "CD"): C,
            ("CC", "DD", "DC"): C,
            ("CC", "DD", "DD"): C,
            ("CD", "CC", "CC"): D,
            ("CD", "CC", "CD"): C,
            ("CD", "CC", "DC"): D,
            ("CD", "CC", "DD"): D,
            ("CD", "CD", "CC"): D,
            ("CD", "CD", "CD"): D,
            ("CD", "CD", "DC"): D,
            ("CD", "CD", "DD"): D,
            ("CD", "DC", "CC"): D,
            ("CD", "DC", "CD"): C,
            ("CD", "DC", "DC"): D,
            ("CD", "DC", "DD"): D,
            ("CD", "DD", "CC"): D,
            ("CD", "DD", "CD"): C,
            ("CD", "DD", "DC"): D,
            ("CD", "DD", "DD"): C,
            ("DC", "CC", "CC"): D,
            ("DC", "CC", "CD"): D,
            ("DC", "CC", "DC"): D,
            ("DC", "CC", "DD"): D,
            ("DC", "CD", "CC"): C,
            ("DC", "CD", "CD"): C,
            ("DC", "CD", "DC"): D,
            ("DC", "CD", "DD"): C,
            ("DC", "DC", "CC"): C,
            ("DC", "DC", "CD"): C,
            ("DC", "DC", "DC"): C,
            ("DC", "DC", "DD"): D,
            ("DC", "DD", "CC"): D,
            ("DC", "DD", "CD"): D,
            ("DC", "DD", "DC"): D,
            ("DC", "DD", "DD"): C,
            ("DD", "CC", "CC"): C,
            ("DD", "CC", "CD"): D,
            ("DD", "CC", "DC"): D,
            ("DD", "CC", "DD"): D,
            ("DD", "CD", "CC"): D,
            ("DD", "CD", "CD"): C,
            ("DD", "CD", "DC"): C,
            ("DD", "CD", "DD"): D,
            ("DD", "DC", "CC"): C,
            ("DD", "DC", "CD"): D,
            ("DD", "DC", "DC"): D,
            ("DD", "DC", "DD"): D,
            ("DD", "DD", "CC"): D,
            ("DD", "DD", "CD"): D,
            ("DD", "DD", "DC"): D,
            ("DD", "DD", "DD"): D,
        }
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_dict, converted_original)

    def test_vs_initial_defector(self):
        opponent_actions = [D, D] + [C, D] * 3
        expected = [(C, D), (C, D)] + [(D, C), (C, D)] * 3
        self.versus_test(
            axelrod.MockPlayer(actions=opponent_actions), expected_actions=expected
        )

    def test_vs_initial_d_c(self):
        opponent_actions = [D, C] + [C, D] * 3
        expected = [(C, D), (C, C)] + [(D, C), (C, D), (C, C), (D, D), (C, C), (C, D)]
        self.versus_test(
            axelrod.MockPlayer(actions=opponent_actions), expected_actions=expected
        )


class TestWinner12(TestPlayer):
    name = "Winner12"
    player = axelrod.Winner12

    expected_classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    expected_class_classifier = copy.copy(expected_classifier)
    expected_class_classifier["memory_depth"] = float("inf")

    def test_new_data(self):
        original_data = {
            ("", "C", "CC"): C,
            ("", "C", "CD"): D,
            ("", "C", "DC"): C,
            ("", "C", "DD"): D,
            ("", "D", "CC"): D,
            ("", "D", "CD"): C,
            ("", "D", "DC"): D,
            ("", "D", "DD"): D,
        }
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_dict, converted_original)

    def test_strategy(self):
        """Starts by cooperating twice."""
        vs_alternator = [(C, C), (C, D), (D, C), (D, D)] * 5
        self.versus_test(axelrod.Alternator(), expected_actions=vs_alternator)

        self.versus_test(axelrod.Cooperator(), expected_actions=[(C, C)] * 10)

        self.versus_test(
            axelrod.Defector(), expected_actions=([(C, D), (C, D)] + [(D, D)] * 10)
        )


class TestWinner21(TestPlayer):
    name = "Winner21"
    player = axelrod.Winner21

    expected_classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    expected_class_classifier = copy.copy(expected_classifier)
    expected_class_classifier["memory_depth"] = float("inf")

    def test_new_data(self):
        original_data = {
            ("", "C", "CC"): C,
            ("", "C", "CD"): D,
            ("", "C", "DC"): C,
            ("", "C", "DD"): D,
            ("", "D", "CC"): C,
            ("", "D", "CD"): D,
            ("", "D", "DC"): D,
            ("", "D", "DD"): D,
        }
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_dict, converted_original)

    def test_strategy(self):
        """Starts by cooperating twice."""
        vs_alternator = [(D, C), (C, D)] + [(D, C), (D, D)] * 5
        self.versus_test(axelrod.Alternator(), expected_actions=vs_alternator)

        self.versus_test(
            axelrod.Cooperator(), expected_actions=[(D, C)] + [(C, C)] * 10
        )

        self.versus_test(
            axelrod.Defector(), expected_actions=([(D, D), (C, D)] + [(D, D)] * 10)
        )


class TestDictConversionFunctions(unittest.TestCase):
    def test_convert_key(self):
        opponent_starting_plays = ""
        player_last_plays = "CC"
        opponent_last_plays = "D"
        old_key = (opponent_starting_plays, player_last_plays, opponent_last_plays)

        new_key = Plays(self_plays=(C, C), op_plays=(D,), op_openings=())

        self.assertEqual(new_key, convert_key(old_key))

    def test_convert_original_to_current(self):
        expected = {
            Plays(self_plays=(C, C), op_plays=(D,), op_openings=()): C,
            Plays(self_plays=(D,), op_plays=(D, D), op_openings=(C,)): D,
        }
        original = {("", "CC", "D"): C, ("C", "D", "DD"): D}
        self.assertEqual(expected, convert_original_to_current(original))


def convert_original_to_current(original_data: dict) -> dict:
    return {convert_key(key): value for key, value in original_data.items()}


def convert_key(old_key: tuple) -> Plays:
    opponent_start, player, opponent = old_key
    return Plays(
        self_plays=str_to_actions(player),
        op_plays=str_to_actions(opponent),
        op_openings=str_to_actions(opponent_start),
    )
