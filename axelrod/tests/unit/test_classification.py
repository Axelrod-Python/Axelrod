"""Tests for the classification."""

import unittest

import axelrod as axl


class TestClassification(unittest.TestCase):
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
            self.assertTrue(None not in [s.classifier[key] for key in known_keys])

    def test_multiple_instances(self):
        """Certain instances of classes of strategies will have different
        classifiers based on the initialisation variables"""
        P1 = axl.MemoryOnePlayer(four_vector=(.5, .5, .5, .5))
        P2 = axl.MemoryOnePlayer(four_vector=(1, 0, 0, 1))
        self.assertNotEqual(P1.classifier, P2.classifier)

        P1 = axl.Joss()
        P2 = axl.Joss(p=0)
        self.assertNotEqual(P1.classifier, P2.classifier)

        P1 = axl.GTFT(p=1)
        P2 = axl.GTFT(p=.5)
        self.assertNotEqual(P1.classifier, P2.classifier)

        P1 = axl.StochasticWSLS()
        P2 = axl.StochasticWSLS(ep=0)
        self.assertNotEqual(P1.classifier, P2.classifier)

        P1 = axl.GoByMajority(memory_depth=5)
        P2 = axl.StochasticWSLS(ep=.1)
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
            axl.Geller,
            axl.GellerCooperator,
            axl.GellerDefector,
            axl.MindBender,
            axl.MindController,
            axl.MindWarper,
            axl.MindReader,
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
            self.assertFalse(axl.obey_axelrod(strategy()), msg=strategy)

        for strategy in known_basic:
            self.assertTrue(axl.obey_axelrod(strategy()), msg=strategy)

        for strategy in known_ordinary:
            self.assertTrue(axl.obey_axelrod(strategy()), msg=strategy)

    def test_is_basic(self):
        """A test that verifies if the is_basic function works correctly"""
        known_cheaters = [
            axl.Darwin,
            axl.Geller,
            axl.GellerCooperator,
            axl.GellerDefector,
            axl.MindBender,
            axl.MindController,
            axl.MindWarper,
            axl.MindReader,
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
            self.assertFalse(axl.is_basic(strategy()), msg=strategy)

        for strategy in known_basic:
            self.assertTrue(axl.is_basic(strategy()), msg=strategy)

        for strategy in known_ordinary:
            self.assertFalse(axl.is_basic(strategy()), msg=strategy)


def str_reps(xs):
    """Maps a collection of player classes to their string representations."""
    return set(map(str, [x() for x in xs]))


class TestStrategies(unittest.TestCase):
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
            self.assertTrue(str_reps(strategy_list).issubset(str_reps(strategies_set)))

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
            str_reps(long_run_time_strategies), str_reps(axl.long_run_time_strategies)
        )
        self.assertTrue(
            all(s().classifier["long_run_time"] for s in axl.long_run_time_strategies)
        )

    def test_short_run_strategies(self):
        short_run_time_strategies = [
            s for s in axl.strategies if s not in axl.long_run_time_strategies
        ]

        self.assertEqual(
            str_reps(short_run_time_strategies), str_reps(axl.short_run_time_strategies)
        )
        self.assertFalse(
            any(s().classifier["long_run_time"] for s in axl.short_run_time_strategies)
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
        self.assertTrue(str_reps(demo_strategies), str_reps(axl.demo_strategies))
