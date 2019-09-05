"""Test for the Gambler strategy. Most tests come from the LookerUp test suite.
"""

import copy
import random
import unittest
import axelrod
from axelrod.load_data_ import load_pso_tables
from axelrod.strategies.lookerup import create_lookup_table_keys
from .test_lookerup import convert_original_to_current
from .test_player import TestPlayer
from .test_evolvable_player import PartialClass, TestEvolvablePlayer


tables = load_pso_tables("pso_gambler.csv", directory="data")
C, D = axelrod.Action.C, axelrod.Action.D


class TestGambler(TestPlayer):

    name = "Gambler"
    player = axelrod.Gambler

    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    expected_class_classifier = copy.copy(expected_classifier)
    expected_class_classifier["memory_depth"] = float("inf")

    def test_strategy(self):
        tft_table = {((), (D,), ()): 0, ((), (C,), ()): 1}
        self.versus_test(
            axelrod.Alternator(),
            expected_actions=[(C, C)] + [(C, D), (D, C)] * 5,
            init_kwargs={"lookup_dict": tft_table},
        )

    def test_stochastic_values(self):
        stochastic_lookup = {((), (), ()): 0.3}
        expected_actions = [(C, C), (D, C), (D, C), (C, C), (D, C)]
        self.versus_test(
            axelrod.Cooperator(),
            expected_actions=expected_actions,
            init_kwargs={"lookup_dict": stochastic_lookup},
            seed=1,
        )


class TestPSOGamblerMem1(TestPlayer):

    name = "PSO Gambler Mem1"
    player = axelrod.PSOGamblerMem1

    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
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
            ("", "C", "C"): 1.0,
            ("", "C", "D"): 0.52173487,
            ("", "D", "C"): 0.0,
            ("", "D", "D"): 0.12050939,
        }
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_dict, converted_original)

    def test_strategy(self):
        vs_cooperator = [(C, C)] * 5
        self.versus_test(axelrod.Cooperator(), expected_actions=vs_cooperator)

    def test_defects_forever_with_correct_conditions(self):
        seed = 1
        opponent_actions = [D, D] + [C] * 10
        expected = [(C, D), (C, D), (D, C)] + [(D, C)] * 9
        self.versus_test(
            axelrod.MockPlayer(actions=opponent_actions),
            expected_actions=expected,
            seed=seed,
        )


class TestPSOGambler1_1_1(TestPlayer):

    name = "PSO Gambler 1_1_1"
    player = axelrod.PSOGambler1_1_1

    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_new_data(self):
        original_data = {
            ("C", "C", "C"): 1.0,
            ("C", "C", "D"): 0.12304797,
            ("C", "D", "C"): 0.0,
            ("C", "D", "D"): 0.13581423,
            ("D", "C", "C"): 1.0,
            ("D", "C", "D"): 0.57740178,
            ("D", "D", "C"): 0.0,
            ("D", "D", "D"): 0.11886807,
        }
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_dict, converted_original)

    def test_cooperate_forever(self):
        seed = 2
        opponent = [D] * 3 + [C] * 10
        expected = [(C, D), (D, D), (D, D)] + [(C, C)] * 10
        self.versus_test(
            axelrod.MockPlayer(opponent), expected_actions=expected, seed=seed
        )

    def test_defect_forever(self):
        seed = 2
        opponent_actions = [C] + [D] + [C] * 10
        expected = [(C, C), (C, D)] + [(D, C)] * 10
        self.versus_test(
            axelrod.MockPlayer(opponent_actions), expected_actions=expected, seed=seed
        )

        opponent_actions = [D] + [C] * 10
        expected = [(C, D)] + [(D, C)] * 10
        self.versus_test(
            axelrod.MockPlayer(opponent_actions), expected_actions=expected, seed=seed
        )


class TestPSOGambler2_2_2(TestPlayer):

    name = "PSO Gambler 2_2_2"
    player = axelrod.PSOGambler2_2_2

    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_new_data(self):
        original_data = {
            ("CC", "CC", "CC"): 1.0,
            ("CC", "CC", "CD"): 1.0,
            ("CC", "CC", "DC"): 0.0,
            ("CC", "CC", "DD"): 0.02126434,
            ("CC", "CD", "CC"): 0.0,
            ("CC", "CD", "CD"): 1.0,
            ("CC", "CD", "DC"): 1.0,
            ("CC", "CD", "DD"): 0.0,
            ("CC", "DC", "CC"): 0.0,
            ("CC", "DC", "CD"): 0.0,
            ("CC", "DC", "DC"): 0.0,
            ("CC", "DC", "DD"): 0.0,
            ("CC", "DD", "CC"): 0.0,
            ("CC", "DD", "CD"): 0.0,
            ("CC", "DD", "DC"): 0.0,
            ("CC", "DD", "DD"): 1.0,
            ("CD", "CC", "CC"): 1.0,
            ("CD", "CC", "CD"): 0.95280465,
            ("CD", "CC", "DC"): 0.80897541,
            ("CD", "CC", "DD"): 0.0,
            ("CD", "CD", "CC"): 0.0,
            ("CD", "CD", "CD"): 0.0,
            ("CD", "CD", "DC"): 0.0,
            ("CD", "CD", "DD"): 0.65147565,
            ("CD", "DC", "CC"): 0.15412392,
            ("CD", "DC", "CD"): 0.24922166,
            ("CD", "DC", "DC"): 0.0,
            ("CD", "DC", "DD"): 0.0,
            ("CD", "DD", "CC"): 0.0,
            ("CD", "DD", "CD"): 0.0,
            ("CD", "DD", "DC"): 0.0,
            ("CD", "DD", "DD"): 0.24523149,
            ("DC", "CC", "CC"): 1.0,
            ("DC", "CC", "CD"): 0.0,
            ("DC", "CC", "DC"): 0.0,
            ("DC", "CC", "DD"): 0.43278586,
            ("DC", "CD", "CC"): 1.0,
            ("DC", "CD", "CD"): 0.0,
            ("DC", "CD", "DC"): 0.23563137,
            ("DC", "CD", "DD"): 1.0,
            ("DC", "DC", "CC"): 1.0,
            ("DC", "DC", "CD"): 1.0,
            ("DC", "DC", "DC"): 0.00227615,
            ("DC", "DC", "DD"): 0.0,
            ("DC", "DD", "CC"): 0.0,
            ("DC", "DD", "CD"): 0.0,
            ("DC", "DD", "DC"): 0.0,
            ("DC", "DD", "DD"): 1.0,
            ("DD", "CC", "CC"): 0.0,
            ("DD", "CC", "CD"): 0.0,
            ("DD", "CC", "DC"): 0.0,
            ("DD", "CC", "DD"): 0.0,
            ("DD", "CD", "CC"): 0.15140743,
            ("DD", "CD", "CD"): 0.0,
            ("DD", "CD", "DC"): 0.0,
            ("DD", "CD", "DD"): 0.0,
            ("DD", "DC", "CC"): 0.0,
            ("DD", "DC", "CD"): 0.0,
            ("DD", "DC", "DC"): 0.0,
            ("DD", "DC", "DD"): 1.0,
            ("DD", "DD", "CC"): 0.0,
            ("DD", "DD", "CD"): 1.0,
            ("DD", "DD", "DC"): 0.77344942,
            ("DD", "DD", "DD"): 0.0,
        }
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_dict, converted_original)

    def test_vs_defector(self):
        expected = [(C, D), (C, D)] + [(D, D)] * 10
        self.versus_test(axelrod.Defector(), expected_actions=expected)

    def test_vs_cooperator(self):
        expected = [(C, C)] * 10
        self.versus_test(axelrod.Cooperator(), expected_actions=expected)

    def test_vs_alternator(self):
        seed = 1
        expected = [(C, C), (C, D), (C, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=expected, seed=seed)

    def test_vs_DCDDC(self):
        seed = 2
        opponent_actions = [D, C, D, D, C]
        expected = [
            (C, D),
            (C, C),
            (D, D),
            (D, D),
            (C, C),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (C, C),
        ]
        self.versus_test(
            axelrod.MockPlayer(actions=opponent_actions),
            expected_actions=expected,
            seed=seed,
        )

        new_seed = 139  # First seed with different result.
        expected[5] = (C, D)
        self.versus_test(
            axelrod.MockPlayer(actions=opponent_actions),
            expected_actions=expected,
            seed=new_seed,
        )


class TestPSOGambler2_2_2_Noise05(TestPlayer):
    name = "PSO Gambler 2_2_2 Noise 05"
    player = axelrod.PSOGambler2_2_2_Noise05

    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_new_data(self):
        original_data = {
            ("CC", "CC", "CC"): 1.0,
            ("CC", "CC", "CD"): 0.0,
            ("CC", "CC", "DC"): 1.0,
            ("CC", "CC", "DD"): 0.63548102,
            ("CC", "CD", "CC"): 1.0,
            ("CC", "CD", "CD"): 1.0,
            ("CC", "CD", "DC"): 1.0,
            ("CC", "CD", "DD"): 0.0,
            ("CC", "DC", "CC"): 0.0,
            ("CC", "DC", "CD"): 1.0,
            ("CC", "DC", "DC"): 0.0,
            ("CC", "DC", "DD"): 0.0,
            ("CC", "DD", "CC"): 1.0,
            ("CC", "DD", "CD"): 0.0,
            ("CC", "DD", "DC"): 0.0,
            ("CC", "DD", "DD"): 0.0,
            ("CD", "CC", "CC"): 1.0,
            ("CD", "CC", "CD"): 1.0,
            ("CD", "CC", "DC"): 0.0,
            ("CD", "CC", "DD"): 0.0,
            ("CD", "CD", "CC"): 0.0,
            ("CD", "CD", "CD"): 0.13863175,
            ("CD", "CD", "DC"): 1.0,
            ("CD", "CD", "DD"): 0.7724137,
            ("CD", "DC", "CC"): 0.0,
            ("CD", "DC", "CD"): 1.0,
            ("CD", "DC", "DC"): 0.0,
            ("CD", "DC", "DD"): 0.07127653,
            ("CD", "DD", "CC"): 0.0,
            ("CD", "DD", "CD"): 1.0,
            ("CD", "DD", "DC"): 0.28124022,
            ("CD", "DD", "DD"): 0.0,
            ("DC", "CC", "CC"): 0.0,
            ("DC", "CC", "CD"): 0.98603825,
            ("DC", "CC", "DC"): 0.0,
            ("DC", "CC", "DD"): 0.0,
            ("DC", "CD", "CC"): 1.0,
            ("DC", "CD", "CD"): 0.06434619,
            ("DC", "CD", "DC"): 1.0,
            ("DC", "CD", "DD"): 1.0,
            ("DC", "DC", "CC"): 1.0,
            ("DC", "DC", "CD"): 0.50999729,
            ("DC", "DC", "DC"): 0.00524508,
            ("DC", "DC", "DD"): 1.0,
            ("DC", "DD", "CC"): 1.0,
            ("DC", "DD", "CD"): 1.0,
            ("DC", "DD", "DC"): 1.0,
            ("DC", "DD", "DD"): 1.0,
            ("DD", "CC", "CC"): 0.0,
            ("DD", "CC", "CD"): 1.0,
            ("DD", "CC", "DC"): 0.16240799,
            ("DD", "CC", "DD"): 0.0,
            ("DD", "CD", "CC"): 0.0,
            ("DD", "CD", "CD"): 1.0,
            ("DD", "CD", "DC"): 1.0,
            ("DD", "CD", "DD"): 0.0,
            ("DD", "DC", "CC"): 0.0,
            ("DD", "DC", "CD"): 1.0,
            ("DD", "DC", "DC"): 0.87463905,
            ("DD", "DC", "DD"): 0.0,
            ("DD", "DD", "CC"): 0.0,
            ("DD", "DD", "CD"): 1.0,
            ("DD", "DD", "DC"): 0.0,
            ("DD", "DD", "DD"): 0.0,
        }
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_dict, converted_original)

    def test_vs_defector(self):
        expected = [(C, D), (C, D)] + [(D, D)] * 10
        self.versus_test(axelrod.Defector(), expected_actions=expected)

    def test_vs_cooperator(self):
        expected = [(C, C)] * 10
        self.versus_test(axelrod.Cooperator(), expected_actions=expected)

    def test_vs_alternator(self):
        seed = 2
        expected = [(C, C), (C, D), (C, C), (D, D), (D, C), (D, D), (C, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=expected, seed=seed)

        new_seed = 1
        expected[4] = (C, C)
        expected[6] = (D, C)
        self.versus_test(axelrod.Alternator(), expected_actions=expected, seed=new_seed)

    def test_vs_DCDDC(self):
        opponent_actions = [D, C, D, D, C]

        seed = 1
        expected = [
            (C, D),
            (C, C),
            (D, D),
            (D, D),
            (C, C),
            (D, D),
            (D, C),
            (C, D),
            (C, D),
        ]
        self.versus_test(
            axelrod.MockPlayer(opponent_actions), expected_actions=expected, seed=seed
        )

        new_seed = 3
        expected[8] = (D, D)
        self.versus_test(
            axelrod.MockPlayer(opponent_actions),
            expected_actions=expected,
            seed=new_seed,
        )

        new_seed = 2
        new_expected = expected[:6] + [(C, C), (D, D), (D, D)]
        self.versus_test(
            axelrod.MockPlayer(opponent_actions),
            expected_actions=new_expected,
            seed=new_seed,
        )


class TestZDMem2(TestPlayer):
    name = "ZD-Mem2"
    player = axelrod.ZDMem2

    expected_classifier = {
        "memory_depth": 2,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_new_data(self):
        original_data = {
            ("", "CC", "CC"): 11 / 12,
            ("", "CC", "CD"): 4 / 11,
            ("", "CC", "DC"): 7 / 9,
            ("", "CC", "DD"): 1 / 10,
            ("", "CD", "CC"): 5 / 6,
            ("", "CD", "CD"): 3 / 11,
            ("", "CD", "DC"): 7 / 9,
            ("", "CD", "DD"): 1 / 10,
            ("", "DC", "CC"): 2 / 3,
            ("", "DC", "CD"): 1 / 11,
            ("", "DC", "DC"): 7 / 9,
            ("", "DC", "DD"): 1 / 10,
            ("", "DD", "CC"): 3 / 4,
            ("", "DD", "CD"): 2 / 11,
            ("", "DD", "DC"): 7 / 9,
            ("", "DD", "DD"): 1 / 10,
        }
        converted_original = convert_original_to_current(original_data)
        self.assertEqual(self.player().lookup_dict, converted_original)

    def test_vs_defector(self):
        seed = 5
        expected = [
            (C, D),
            (C, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (C, D),
            (D, D),
        ]

        self.versus_test(axelrod.Defector(), expected_actions=expected, seed=seed)

    def test_vs_cooperator(self):
        seed = 5
        expected = [
            (C, C),
            (C, C),
            (C, C),
            (C, C),
            (C, C),
            (D, C),
            (C, C),
            (D, C),
            (C, C),
            (C, C),
        ]

        self.versus_test(axelrod.Cooperator(), expected_actions=expected, seed=seed)

    def test_vs_alternator(self):
        seed = 2
        expected = [(C, C), (C, D), (D, C), (D, D), (C, C), (C, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=expected, seed=seed)

        new_seed = 1
        expected = [(C, C), (C, D), (C, C), (D, D), (D, C), (C, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=expected, seed=new_seed)


class TestEvolvableGambler(unittest.TestCase):

    def test_receive_vector(self):
        plays, op_plays, op_start_plays = 1, 1, 1
        player = axelrod.EvolvableGambler(
            parameters=(plays, op_plays, op_start_plays))

        self.assertRaises(AttributeError, axelrod.EvolvableGambler.__getattribute__,
                          *[player, 'vector'])

        vector = [random.random() for _ in range(8)]
        player.receive_vector(vector)
        self.assertEqual(player.pattern, vector)

    def test_vector_to_instance(self):
        plays, op_plays, op_start_plays = 1, 1, 1
        player = axelrod.EvolvableGambler(
            parameters=(plays, op_plays, op_start_plays))

        vector = [random.random() for _ in range(8)]
        player.receive_vector(vector)
        keys = create_lookup_table_keys(player_depth=plays, op_depth=op_plays,
                                        op_openings_depth=op_start_plays)
        action_dict = dict(zip(keys, vector))
        self.assertEqual(player._lookup.dictionary, action_dict)

    def test_create_vector_bounds(self):
        plays, op_plays, op_start_plays = 1, 1, 1
        player = axelrod.EvolvableGambler(
            parameters=(plays, op_plays, op_start_plays))
        lb, ub = player.create_vector_bounds()
        self.assertIsInstance(lb, list)
        self.assertIsInstance(ub, list)
        self.assertEqual(len(lb), 8)
        self.assertEqual(len(ub), 8)


class TestEvolvableGambler2(TestEvolvablePlayer):
    name = "EvolvableGambler"
    player_class = axelrod.EvolvableGambler
    parent_class = axelrod.Gambler
    parent_kwargs = ["lookup_dict"]
    init_parameters = {"parameters": (1, 1, 1),
                       "initial_actions": (C,)}


class TestEvolvableGambler3(TestEvolvablePlayer):
    name = "EvolvableGambler"
    player_class = axelrod.EvolvableGambler
    parent_class = axelrod.Gambler
    parent_kwargs = ["lookup_dict"]
    init_parameters = {"parameters": (3, 2, 1),
                       "initial_actions": (C, C, C,)}


class TestEvolvableGambler4(TestEvolvablePlayer):
    name = "EvolvableGambler"
    player_class = axelrod.EvolvableGambler
    parent_class = axelrod.Gambler
    parent_kwargs = ["lookup_dict"]
    init_parameters = {"parameters": (2, 2, 2),
                       "pattern": [random.random() for _ in range(64)],
                       "initial_actions": (C, C,)}


# Substitute EvolvableHMMPlayer as a regular HMMPlayer.
EvolvableGamblerWithDefault = PartialClass(
    axelrod.EvolvableGambler,
    pattern=tables[("PSO Gambler 2_2_2", 2, 2, 2)],
    parameters=(2, 2, 2),
    initial_actions=(C,C,)
)


class EvolvableGamblerAsGambler(TestPSOGambler2_2_2):
    player = EvolvableGamblerWithDefault

    def test_equality_of_clone(self):
        pass

    def test_equality_of_pickle_clone(self):
        pass

    def test_repr(self):
        pass
