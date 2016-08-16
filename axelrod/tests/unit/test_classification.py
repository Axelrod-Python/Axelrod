"""Tests for the classification"""

import unittest
import axelrod


class TestClassification(unittest.TestCase):

    def test_known_classifiers(self):
        # A set of dimensions that are known to have been fully applied
        known_keys = ['stochastic',
                      'memory_depth',
                      'long_run_time',
                      'inspects_source',
                      'manipulates_source',
                      'manipulates_state']

        for s in axelrod.all_strategies:
            s = s()
            self.assertTrue(None not in [s.classifier[key] for key in known_keys])

    def test_multiple_instances(self):
        """Certain instances of classes of strategies will have different
        classifiers based on the initialisation variables"""
        P1 = axelrod.MemoryOnePlayer((.5, .5, .5, .5))
        P2 = axelrod.MemoryOnePlayer((1, 0, 0, 1))
        self.assertNotEqual(P1.classifier, P2.classifier)

        P1 = axelrod.Joss()
        P2 = axelrod.Joss(0)
        self.assertNotEqual(P1.classifier, P2.classifier)

        P1 = axelrod.GTFT(1)
        P2 = axelrod.GTFT(.5)
        self.assertNotEqual(P1.classifier, P2.classifier)

        P1 = axelrod.StochasticWSLS()
        P2 = axelrod.StochasticWSLS(0)
        self.assertNotEqual(P1.classifier, P2.classifier)

        P1 = axelrod.GoByMajority(5)
        P2 = axelrod.StochasticWSLS(.1)
        self.assertNotEqual(P1.classifier, P2.classifier)

    def test_manipulation_of_classifier(self):
        """Test that can change the classifier of an instance without changing
        the classifier of the class"""
        player = axelrod.Cooperator()
        player.classifier['memory_depth'] += 1
        self.assertNotEqual(player.classifier, axelrod.Cooperator.classifier)
        player = axelrod.Defector()
        player.classifier['memory_depth'] += 1
        self.assertNotEqual(player.classifier, axelrod.Defector.classifier)

    def test_obey_axelrod(self):
        """A test that verifies if the obey_axelrod function works correctly"""
        known_cheaters = [axelrod.Darwin,
                          axelrod.Geller,
                          axelrod.GellerCooperator,
                          axelrod.GellerDefector,
                          axelrod.MindBender,
                          axelrod.MindController,
                          axelrod.MindWarper,
                          axelrod.MindReader]

        known_basic = [axelrod.Alternator,
                       axelrod.AntiTitForTat,
                       axelrod.Bully,
                       axelrod.Cooperator,
                       axelrod.Defector,
                       axelrod.GoByMajority,
                       axelrod.SuspiciousTitForTat,
                       axelrod.TitForTat,
                       axelrod.WinStayLoseShift]

        known_ordinary = [axelrod.AverageCopier,
                          axelrod.ForgivingTitForTat,
                          axelrod.GoByMajority20,
                          axelrod.GTFT,
                          axelrod.Grudger,
                          axelrod.Inverse,
                          axelrod.Random]

        for strategy in known_cheaters:
            self.assertFalse(axelrod.obey_axelrod(strategy()), msg=strategy)

        for strategy in known_basic:
            self.assertTrue(axelrod.obey_axelrod(strategy()), msg=strategy)

        for strategy in known_ordinary:
            self.assertTrue(axelrod.obey_axelrod(strategy()), msg=strategy)

    def test_is_basic(self):
        """A test that verifies if the is_basic function works correctly"""
        known_cheaters = [axelrod.Darwin,
                          axelrod.Geller,
                          axelrod.GellerCooperator,
                          axelrod.GellerDefector,
                          axelrod.MindBender,
                          axelrod.MindController,
                          axelrod.MindWarper,
                          axelrod.MindReader]

        known_basic = [axelrod.Alternator,
                       axelrod.AntiTitForTat,
                       axelrod.Bully,
                       axelrod.Cooperator,
                       axelrod.Defector,
                       axelrod.SuspiciousTitForTat,
                       axelrod.TitForTat,
                       axelrod.WinStayLoseShift]

        known_ordinary = [axelrod.AverageCopier,
                          axelrod.ForgivingTitForTat,
                          axelrod.GoByMajority20,
                          axelrod.GTFT,
                          axelrod.Grudger,
                          axelrod.Inverse,
                          axelrod.Random]

        for strategy in known_cheaters:
            self.assertFalse(axelrod.is_basic(strategy()), msg=strategy)

        for strategy in known_basic:
            self.assertTrue(axelrod.is_basic(strategy()), msg=strategy)

        for strategy in known_ordinary:
            self.assertFalse(axelrod.is_basic(strategy()), msg=strategy)


class TestStrategies(unittest.TestCase):

    def test_strategy_id(self):
        for strategy in axelrod.all_strategies:
            self.assertIsNotNone(axelrod.strategy_id(strategy))

        self.assertEqual(
            axelrod.strategy_id(axelrod.TitForTat),
            'tit_for_tat')

        self.assertEqual(
            axelrod.strategy_id(axelrod.Defector),
            'defector')

    def test_strategy_index(self):
        for strategy in axelrod.all_strategies:
            unique_id = strategy.name.lower().replace(' ', '_')
            self.assertIn(unique_id, axelrod.strategy_index)

        self.assertIn('tit_for_tat', axelrod.strategy_index)
        self.assertIn('defector', axelrod.strategy_index)

    def test_strategy_list(self):
        for strategy_list in ["all_strategies",
                              "demo_strategies",
                              "basic_strategies",
                              "long_run_time_strategies",
                              "strategies",
                              "ordinary_strategies",
                              "cheating_strategies"]:
            self.assertTrue(hasattr(axelrod, strategy_list))

    def test_lists_not_empty(self):
        for strategy_list in [axelrod.all_strategies,
                              axelrod.demo_strategies,
                              axelrod.basic_strategies,
                              axelrod.long_run_time_strategies,
                              axelrod.strategies,
                              axelrod.ordinary_strategies,
                              axelrod.cheating_strategies]:
            self.assertTrue(len(strategy_list) > 0)

    def test_inclusion_of_strategy_lists(self):
        all_strategies_set = set(axelrod.all_strategies)
        for strategy_list in [axelrod.demo_strategies,
                              axelrod.basic_strategies,
                              axelrod.long_run_time_strategies,
                              axelrod.strategies,
                              axelrod.ordinary_strategies,
                              axelrod.cheating_strategies]:
            self.assertTrue(set(strategy_list).issubset(all_strategies_set))

        strategies_set = set(axelrod.strategies)
        for strategy_list in [axelrod.demo_strategies,
                              axelrod.basic_strategies,
                              axelrod.long_run_time_strategies]:
            self.assertTrue(set(strategy_list).issubset(strategies_set))

    def test_long_run_strategies(self):
        long_run_time_strategies = [axelrod.MetaMajority,
                                    axelrod.MetaMinority,
                                    axelrod.MetaWinner,
                                    axelrod.MetaMajorityMemoryOne,
                                    axelrod.MetaWinnerMemoryOne,
                                    axelrod.MetaMajorityFiniteMemory,
                                    axelrod.MetaWinnerFiniteMemory,
                                    axelrod.MetaMajorityLongMemory,
                                    axelrod.MetaWinnerLongMemory,
                                    axelrod.MetaMixer]
        self.assertTrue(long_run_time_strategies,
                        axelrod.long_run_time_strategies)

    def test_meta_inclusion(self):
        self.assertTrue(axelrod.MetaMajority in axelrod.strategies)

        self.assertTrue(axelrod.MetaHunter in axelrod.strategies)
        self.assertFalse(axelrod.MetaHunter in axelrod.long_run_time_strategies)

    def test_demo_strategies(self):
        demo_strategies = [axelrod.Cooperator,
                           axelrod.Defector,
                           axelrod.TitForTat,
                           axelrod.Grudger,
                           axelrod.Random]
        self.assertTrue(demo_strategies, axelrod.demo_strategies)
