"""Tests for the classification."""

import os
import unittest
import warnings
from typing import Any, Text

import yaml

import axelrod as axl
from axelrod.classifier import (
    Classifier,
    Classifiers,
    _Classifiers,
    memory_depth,
    rebuild_classifier_table,
)
from axelrod.player import Player


class TitForTatWithEmptyClassifier(Player):
    """
    Same name as TitForTat, but with empty classifier.
    """

    # Classifiers are looked up by name, so only the name matters.
    name = "Tit For Tat"
    classifier = {}


class TitForTatWithNonTrivialInitialzer(Player):
    """
    Same name as TitForTat, but with empty classifier.
    """

    def __init__(self, x: Any):
        pass  # pragma: no cover

    # Classifiers are looked up by name, so only the name matters.
    name = "Tit For Tat"
    classifier = {}


class TestClassification(unittest.TestCase):
    def setUp(self) -> None:
        # Ignore warnings about classifiers running on instances
        warnings.simplefilter("ignore", category=UserWarning)

    def tearDown(self) -> None:
        warnings.simplefilter("default", category=UserWarning)

    def test_classifier_build(self):
        dirname = os.path.dirname(__file__)
        test_path = os.path.join(
            dirname, "../../../test_outputs/classifier_test.yaml"
        )

        # Just returns the name of the player.  For testing.
        name_classifier = Classifier[Text]("name", lambda player: player.name)
        rebuild_classifier_table(
            classifiers=[name_classifier],
            players=[axl.Cooperator, axl.Defector],
            path=test_path,
        )

        filename = os.path.join("../..", test_path)
        with open(filename, "r") as f:
            all_player_dicts = yaml.load(f, Loader=yaml.FullLoader)

        self.assertDictEqual(
            all_player_dicts,
            {
                "Cooperator": {"name": "Cooperator"},
                "Defector": {"name": "Defector"},
            },
        )

    def test_singletonity_of_classifiers_class(self):
        classifiers_1 = _Classifiers()
        classifiers_2 = _Classifiers()

        self.assertIs(classifiers_1, classifiers_2)

    def test_get_name_from_classifier(self):
        # Should be able to take a string or a Classifier instance.
        self.assertEqual(Classifiers["memory_depth"](axl.TitForTat()), 1)
        self.assertEqual(Classifiers[memory_depth](axl.TitForTat()), 1)

    def test_classifier_works_on_non_instances(self):
        warnings.simplefilter("default", category=UserWarning)
        with warnings.catch_warnings(record=True) as w:
            self.assertEqual(Classifiers["memory_depth"](axl.TitForTat), 1)
            self.assertEqual(len(w), 1)

    def test_key_error_on_uknown_classifier(self):
        with self.assertRaises(KeyError):
            Classifiers["invalid_key"](axl.TitForTat)

    def test_will_lookup_key_in_dict(self):
        self.assertEqual(
            Classifiers["memory_depth"](TitForTatWithEmptyClassifier), 1
        )

    def test_will_lookup_key_for_classes_that_cant_init(self):
        with self.assertRaises(Exception) as exptn:
            Classifiers["memory_depth"](TitForTatWithNonTrivialInitialzer)
        self.assertEqual(
            str(exptn.exception),
            "Passed player class doesn't have a trivial initializer.",
        )

    def test_known_classifiers(self):
        # A set of dimensions that are known to have been fully applied
        known_keys = [
            "stochastic",
            "memory_depth",
            "long_run_time",
            "inspects_source",
            "manipulates_source",
            "manipulates_state",
        ]

        for s in axl.all_strategies:
            s = s()
            self.assertTrue(
                None not in [Classifiers[key](s) for key in known_keys]
            )

    def test_multiple_instances(self):
        """Certain instances of classes of strategies will have different
        classifiers based on the initialisation variables"""
        P1 = axl.MemoryOnePlayer(four_vector=(0.5, 0.5, 0.5, 0.5))
        P2 = axl.MemoryOnePlayer(four_vector=(1, 0, 0, 1))
        self.assertNotEqual(P1.classifier, P2.classifier)

        P1 = axl.FirstByJoss()
        P2 = axl.FirstByJoss(p=0)
        self.assertNotEqual(P1.classifier, P2.classifier)

        P1 = axl.GTFT(p=1)
        P2 = axl.GTFT(p=0.5)
        self.assertNotEqual(P1.classifier, P2.classifier)

        P1 = axl.StochasticWSLS()
        P2 = axl.StochasticWSLS(ep=0)
        self.assertNotEqual(P1.classifier, P2.classifier)

        P1 = axl.GoByMajority(memory_depth=5)
        P2 = axl.StochasticWSLS(ep=0.1)
        self.assertNotEqual(P1.classifier, P2.classifier)

    def test_manipulation_of_classifier(self):
        """Test that can change the classifier of an instance without changing
        the classifier of the class"""
        player = axl.Cooperator()
        player.classifier["memory_depth"] += 1
        self.assertNotEqual(player.classifier, axl.Cooperator.classifier)
        player = axl.Defector()
        player.classifier["memory_depth"] += 1
        self.assertNotEqual(player.classifier, axl.Defector.classifier)

    def test_obey_axelrod(self):
        """A test that verifies if the obey_axl function works correctly"""
        known_cheaters = [
            axl.Darwin,
        ]

        known_basic = [
            axl.Alternator,
            axl.AntiTitForTat,
            axl.Bully,
            axl.Cooperator,
            axl.Defector,
            axl.GoByMajority,
            axl.SuspiciousTitForTat,
            axl.TitForTat,
            axl.WinStayLoseShift,
        ]

        known_ordinary = [
            axl.AverageCopier,
            axl.ForgivingTitForTat,
            axl.GoByMajority20,
            axl.GTFT,
            axl.Grudger,
            axl.Inverse,
            axl.Random,
        ]

        for strategy in known_cheaters:
            self.assertFalse(
                axl.Classifiers.obey_axelrod(strategy()), msg=strategy
            )

        for strategy in known_basic:
            self.assertTrue(
                axl.Classifiers.obey_axelrod(strategy()), msg=strategy
            )

        for strategy in known_ordinary:
            self.assertTrue(
                axl.Classifiers.obey_axelrod(strategy()), msg=strategy
            )

    def test_is_basic(self):
        """A test that verifies if the is_basic function works correctly"""
        known_cheaters = [
            axl.Darwin,
        ]

        known_basic = [
            axl.Alternator,
            axl.AntiTitForTat,
            axl.Bully,
            axl.Cooperator,
            axl.Defector,
            axl.SuspiciousTitForTat,
            axl.TitForTat,
            axl.WinStayLoseShift,
        ]

        known_ordinary = [
            axl.AverageCopier,
            axl.ForgivingTitForTat,
            axl.GoByMajority20,
            axl.GTFT,
            axl.Inverse,
            axl.Random,
        ]

        for strategy in known_cheaters:
            self.assertFalse(axl.Classifiers.is_basic(strategy()), msg=strategy)

        for strategy in known_basic:
            self.assertTrue(axl.Classifiers.is_basic(strategy()), msg=strategy)

        for strategy in known_ordinary:
            self.assertFalse(axl.Classifiers.is_basic(strategy()), msg=strategy)


def str_reps(xs):
    """Maps a collection of player classes to their string representations."""
    return set(map(str, [x() for x in xs]))


class TestStrategies(unittest.TestCase):
    def setUp(self) -> None:
        # Ignore warnings about classifiers running on instances.  We want to
        # allow this for some of the map functions.
        warnings.simplefilter("ignore", category=UserWarning)

    def tearDown(self) -> None:
        warnings.simplefilter("default", category=UserWarning)

    def test_strategy_list(self):
        for strategy_list in [
            "all_strategies",
            "demo_strategies",
            "basic_strategies",
            "long_run_time_strategies",
            "strategies",
            "ordinary_strategies",
            "cheating_strategies",
        ]:
            self.assertTrue(hasattr(axl, strategy_list))

    def test_lists_not_empty(self):
        for strategy_list in [
            axl.all_strategies,
            axl.demo_strategies,
            axl.basic_strategies,
            axl.long_run_time_strategies,
            axl.strategies,
            axl.ordinary_strategies,
            axl.cheating_strategies,
        ]:
            self.assertTrue(len(strategy_list) > 0)

    def test_inclusion_of_strategy_lists(self):
        all_strategies_set = set(axl.all_strategies)
        for strategy_list in [
            axl.demo_strategies,
            axl.basic_strategies,
            axl.long_run_time_strategies,
            axl.strategies,
            axl.ordinary_strategies,
            axl.cheating_strategies,
        ]:
            self.assertTrue(
                str_reps(strategy_list).issubset(str_reps(all_strategies_set))
            )

        strategies_set = set(axl.strategies)
        for strategy_list in [
            axl.demo_strategies,
            axl.basic_strategies,
            axl.long_run_time_strategies,
        ]:
            self.assertTrue(
                str_reps(strategy_list).issubset(str_reps(strategies_set))
            )

    def test_long_run_strategies(self):
        long_run_time_strategies = [
            axl.DBS,
            axl.MetaMajority,
            axl.MetaMajorityFiniteMemory,
            axl.MetaMajorityLongMemory,
            axl.MetaMinority,
            axl.MetaMixer,
            axl.MetaWinner,
            axl.MetaWinnerDeterministic,
            axl.MetaWinnerEnsemble,
            axl.MetaWinnerFiniteMemory,
            axl.MetaWinnerLongMemory,
            axl.MetaWinnerStochastic,
            axl.NMWEDeterministic,
            axl.NMWEFiniteMemory,
            axl.NMWELongMemory,
            axl.NMWEStochastic,
            axl.NiceMetaWinner,
            axl.NiceMetaWinnerEnsemble,
        ]

        self.assertEqual(
            str_reps(long_run_time_strategies),
            str_reps(axl.long_run_time_strategies),
        )
        self.assertTrue(
            all(map(Classifiers["long_run_time"], axl.long_run_time_strategies))
        )

    def test_short_run_strategies(self):
        short_run_time_strategies = [
            s for s in axl.strategies if s not in axl.long_run_time_strategies
        ]

        self.assertEqual(
            str_reps(short_run_time_strategies),
            str_reps(axl.short_run_time_strategies),
        )
        self.assertFalse(
            any(
                map(Classifiers["long_run_time"], axl.short_run_time_strategies)
            )
        )

    def test_meta_inclusion(self):
        self.assertTrue(str(axl.MetaMajority()) in str_reps(axl.strategies))

        self.assertTrue(str(axl.MetaHunter()) in str_reps(axl.strategies))
        self.assertFalse(
            str(axl.MetaHunter()) in str_reps(axl.long_run_time_strategies)
        )

    def test_demo_strategies(self):
        demo_strategies = [
            axl.Cooperator,
            axl.Defector,
            axl.TitForTat,
            axl.Grudger,
            axl.Random,
        ]
        self.assertTrue(
            str_reps(demo_strategies), str_reps(axl.demo_strategies)
        )
