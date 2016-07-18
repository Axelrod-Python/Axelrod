"""Test for the random strategy."""

import numpy
import random
import unittest

from axelrod import random_choice, seed, Actions

C, D = Actions.C, Actions.D

class TestRandom_(unittest.TestCase):

    def test_return_values(self):
        self.assertEqual(random_choice(1), C)
        self.assertEqual(random_choice(0), D)
        random.seed(1)
        self.assertEqual(random_choice(), C)
        random.seed(2)
        self.assertEqual(random_choice(), D)

    def test_set_seed(self):
        """Test that numpy and stdlib random seed is set by axelrod seed"""

        numpy_random_numbers = []
        stdlib_random_numbers = []
        for _ in range(2):
            seed(0)
            numpy_random_numbers.append(numpy.random.random())
            stdlib_random_numbers.append(random.random())

        self.assertEqual(numpy_random_numbers[0], numpy_random_numbers[1])
        self.assertEqual(stdlib_random_numbers[0], stdlib_random_numbers[1])

