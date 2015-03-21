"""Tests for the Ecosystem class"""

import unittest

import axelrod


class TestEcosystem(unittest.TestCase):



    @classmethod
    def setUpClass(cls):
        cooperators = axelrod.Tournament(players=[
            axelrod.Cooperator(),
            axelrod.Cooperator(),
            axelrod.Cooperator(),
            axelrod.Cooperator(),
        ])
        defector_wins = axelrod.Tournament(players=[
            axelrod.Cooperator(),
            axelrod.Cooperator(),
            axelrod.Cooperator(),
            axelrod.Defector(),
        ])
        cls.res_cooperators = cooperators.play()
        cls.res_defector_wins = defector_wins.play()

    def test_init(self):
        """Are the populations created correctly?"""

        # By default create populations of equal size
        eco = axelrod.Ecosystem(self.res_cooperators)
        pops = eco.population_sizes
        self.assertEquals(eco.nplayers, 4)
        self.assertEquals(len(pops), 1)
        self.assertEquals(len(pops[0]), 4)
        self.assertAlmostEqual(sum(pops[0]), 1.0)
        self.assertEquals(list(set(pops[0])), [0.25])

        # Can pass list of initial population distributions
        eco = axelrod.Ecosystem(self.res_cooperators, population=[.7, .25, .03, .02])
        pops = eco.population_sizes
        self.assertEquals(eco.nplayers, 4)
        self.assertEquals(len(pops), 1)
        self.assertEquals(len(pops[0]), 4)
        self.assertAlmostEqual(sum(pops[0]), 1.0)
        self.assertEquals(pops[0], [.7, .25, .03, .02])

        # Distribution will automatically normalise
        eco = axelrod.Ecosystem(self.res_cooperators, population=[70, 25, 3, 2])
        pops = eco.population_sizes
        self.assertEquals(eco.nplayers, 4)
        self.assertEquals(len(pops), 1)
        self.assertEquals(len(pops[0]), 4)
        self.assertAlmostEqual(sum(pops[0]), 1.0)
        self.assertEquals(pops[0], [.7, .25, .03, .02])

        # If passed list is of incorrect size get error
        self.assertRaises(TypeError, axelrod.Ecosystem, self.res_cooperators, population=[.7, .2, .03, .1, .1])

        # If passed list has negative values
        self.assertRaises(TypeError, axelrod.Ecosystem, self.res_cooperators, population=[.7, -.2, .03, .2])

    def test_cooperators(self):
        """Are cooperators stable over time?"""

        eco = axelrod.Ecosystem(self.res_cooperators)
        eco.reproduce(100)
        pops = eco.population_sizes
        self.assertEquals(len(pops), 101)
        for p in pops:
            self.assertEquals(len(p), 4)
            self.assertEquals(sum(p), 1.0)
            self.assertEquals(list(set(p)), [0.25])

    def test_defector_wins(self):
        """Does one defector win over time?"""

        eco = axelrod.Ecosystem(self.res_defector_wins)
        eco.reproduce(1000)
        pops = eco.population_sizes
        self.assertEquals(len(pops), 1001)
        for p in pops:
            self.assertEquals(len(p), 4)
            self.assertAlmostEquals(sum(p), 1.0)
        last = pops[-1]
        self.assertAlmostEquals(last[0], 0.0)
        self.assertAlmostEquals(last[1], 0.0)
        self.assertAlmostEquals(last[2], 0.0)
        self.assertAlmostEquals(last[3], 1.0)
