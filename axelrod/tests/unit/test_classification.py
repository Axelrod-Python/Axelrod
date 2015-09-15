"""Tests for the classification"""

import unittest
import axelrod


class TestClassification(unittest.TestCase):

    def test_known_classifiers(self):
        # A set of dimensions that are known to have been fully applied
        known_keys = ['stochastic',
                      'memory_depth',
                      'inspects_source',
                      'manipulates_source',
                      'manipulates_state']

        for s in axelrod.strategies:
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
        P2 = axelrod.StochasticWSLS(10)
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

    def test_is_cheater(self):
        """A test that verifies if the is_cheater function works correctly"""
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
                       axelrod.CyclerCCCCCD,
                       axelrod.CyclerCCCD,
                       axelrod.CyclerCCD,
                       axelrod.Defector,
                       axelrod.GoByMajority,
                       axelrod.SuspiciousTitForTat,
                       axelrod.TitForTat,
                       axelrod.WinStayLoseShift]

        for strategy in known_cheaters:
            self.assertTrue(axelrod.is_cheater(strategy), msg=strategy)
            self.assertFalse(axelrod.is_basic(strategy), msg=strategy)

        for strategy in known_basic:
            self.assertTrue(axelrod.is_basic(strategy), msg=strategy)
            self.assertFalse(axelrod.is_cheater(strategy), msg=strategy)


    def test_is_basic(self):
        pass



class TestStrategies(unittest.TestCase):

    def test_strategy_list(self):
        self.assertTrue(hasattr(axelrod, "strategies"))
        self.assertTrue(hasattr(axelrod, "basic_strategies"))
        self.assertTrue(hasattr(axelrod, "ordinary_strategies"))
        self.assertTrue(hasattr(axelrod, "cheating_strategies"))

    def test_lists_not_empty(self):
        self.assertTrue(len(axelrod.strategies) > 0)
        self.assertTrue(len(axelrod.basic_strategies) > 0)
        self.assertTrue(len(axelrod.ordinary_strategies) > 0)
        self.assertTrue(len(axelrod.cheating_strategies) > 0)

    def test_meta_inclusion(self):
        self.assertTrue(axelrod.MetaMajority in axelrod.strategies)


