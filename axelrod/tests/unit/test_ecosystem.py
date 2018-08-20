"""Tests for the Ecosystem class."""

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

    def test_default_population_sizes(self):
        eco = axelrod.Ecosystem(self.res_cooperators)
        pops = eco.population_sizes
        self.assertEqual(eco.num_players, 4)
        self.assertEqual(len(pops), 1)
        self.assertEqual(len(pops[0]), 4)
        self.assertAlmostEqual(sum(pops[0]), 1.0)
        self.assertEqual(list(set(pops[0])), [0.25])

    def test_non_default_population_sizes(self):
        eco = axelrod.Ecosystem(self.res_cooperators, population=[.7, .25, .03, .02])
        pops = eco.population_sizes
        self.assertEqual(eco.num_players, 4)
        self.assertEqual(len(pops), 1)
        self.assertEqual(len(pops[0]), 4)
        self.assertAlmostEqual(sum(pops[0]), 1.0)
        self.assertEqual(pops[0], [.7, .25, .03, .02])

    def test_population_normalization(self):
        eco = axelrod.Ecosystem(self.res_cooperators, population=[70, 25, 3, 2])
        pops = eco.population_sizes
        self.assertEqual(eco.num_players, 4)
        self.assertEqual(len(pops), 1)
        self.assertEqual(len(pops[0]), 4)
        self.assertAlmostEqual(sum(pops[0]), 1.0)
        self.assertEqual(pops[0], [.7, .25, .03, .02])

    def test_results_and_population_of_different_sizes(self):
        self.assertRaises(TypeError, axelrod.Ecosystem, self.res_cooperators,
                          population=[.7, .2, .03, .1, .1])

    def test_negative_populations(self):
        self.assertRaises(TypeError, axelrod.Ecosystem, self.res_cooperators,
                          population=[.7, -.2, .03, .2])

    def test_fitness_function(self):
        fitness = lambda p: 2 * p
        eco = axelrod.Ecosystem(self.res_cooperators, fitness=fitness)
        self.assertTrue(eco.fitness(10), 20)

    def test_cooperators_are_stable_over_time(self):
        eco = axelrod.Ecosystem(self.res_cooperators)
        eco.reproduce(100)
        pops = eco.population_sizes
        self.assertEqual(len(pops), 101)
        for p in pops:
            self.assertEqual(len(p), 4)
            self.assertEqual(sum(p), 1.0)
            self.assertEqual(list(set(p)), [0.25])

    def test_defector_wins_with_only_cooperators(self):
        eco = axelrod.Ecosystem(self.res_defector_wins)
        eco.reproduce(1000)
        pops = eco.population_sizes
        self.assertEqual(len(pops), 1001)
        for p in pops:
            self.assertEqual(len(p), 4)
            self.assertAlmostEqual(sum(p), 1.0)
        last = pops[-1]
        self.assertAlmostEqual(last[0], 0.0)
        self.assertAlmostEqual(last[1], 0.0)
        self.assertAlmostEqual(last[2], 0.0)
        self.assertAlmostEqual(last[3], 1.0)
