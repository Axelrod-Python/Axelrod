"""Tests for the Ecosystem class"""

import unittest

import axelrod


class TestEcosystem(unittest.TestCase):

    zeros = [[0 for i in range(10)] for i in range(10)]

    def test_init(self):
        """Are the populations created correctly?"""

        eco = axelrod.Ecosystem(self.zeros)
        self.assertEquals(eco.nplayers, 10)
        self.assertEquals(len(eco.populations), 1)
        self.assertEquals(len(eco.populations[0]), 10)
        self.assertAlmostEqual(sum(eco.populations[0]), 1.0)

    def test_reproduce(self):
        """Does the reproduction mechanism work as expected?"""

        eco = axelrod.Ecosystem(self.zeros)
        eco.reproduce(100)
        self.assertEquals(len(eco.populations), 101)
        