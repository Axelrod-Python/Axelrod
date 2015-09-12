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
            self.assertTrue(None not in [s.behaviour[key] for key in known_keys])

    def test_multiple_instances(self):
        """Certain instances of classes of strategies will have different
        behaviours based on the initialisation variables"""
        P1 = axelrod.MemoryOnePlayer((.5, .5, .5, .5))
        P2 = axelrod.MemoryOnePlayer((1, 0, 0, 1))
        self.assertNotEqual(P1.behaviour, P2.behaviour)

        P1 = axelrod.Joss()
        P2 = axelrod.Joss(0)
        self.assertNotEqual(P1.behaviour, P2.behaviour)

        P1 = axelrod.GTFT(1)
        P2 = axelrod.GTFT(.5)
        self.assertNotEqual(P1.behaviour, P2.behaviour)

        P1 = axelrod.StochasticWSLS()
        P2 = axelrod.StochasticWSLS(0)
        self.assertNotEqual(P1.behaviour, P2.behaviour)

        P1 = axelrod.GoByMajority(5)
        P2 = axelrod.StochasticWSLS(10)
        self.assertNotEqual(P1.behaviour, P2.behaviour)

    def test_manipulation_of_behaviour(self):
        """Test that can change the behaviour of an instance without changing
        the behaviour of the class"""
        player = axelrod.Cooperator()
        player.behaviour['memory_depth'] += 1
        self.assertNotEqual(player.behaviour, axelrod.Cooperator.behaviour)
        player = axelrod.Defector()
        player.behaviour['memory_depth'] += 1
        self.assertNotEqual(player.behaviour, axelrod.Defector.behaviour)

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

        for strategy in known_cheaters:
            self.assertTrue(axelrod.is_cheater(strategy), msg=strategy)

        for strategy in axelrod.basic_strategies:
            self.assertFalse(axelrod.is_cheater(strategy), msg=strategy)
