"""Tests for the classification"""

import unittest
import axelrod


class TestClassification(unittest.TestCase):

    def test_known_classifiers(self):
        # Grabbing all the strategies: this will be changed to just be
        # `axelrod.strategies`
        strategies = axelrod.basic_strategies
        strategies += axelrod.ordinary_strategies
        strategies += axelrod.cheating_strategies

        # A set of dimensions that are known to have been fully applied
        known_keys = ['stochastic',
                      'memory_depth',
                      'inspects_opponent_source',
                      'manipulates_opponent_source',
                      'manipulates_opponent_state']

        for s in strategies:
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
