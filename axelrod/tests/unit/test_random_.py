"""Tests for the random functions."""
from collections import Counter
import random
import unittest
import numpy
from axelrod import random_choice, seed, Action, Pdf

C, D = Action.C, Action.D


class TestRandom_(unittest.TestCase):

    def test_return_values(self):
        self.assertEqual(random_choice(1), C)
        self.assertEqual(random_choice(0), D)
        seed(1)
        self.assertEqual(random_choice(), C)
        seed(2)
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

    def test_seed_not_offset_by_deterministic_call(self):
        """Test that when called with p = 0 or 1, the random seed is not
        affected."""
        for p in [0, 1]:
            seed(0)
            r = random.random()
            seed(0)
            random_choice(p)
            self.assertEqual(r, random.random())


class TestPdf(unittest.TestCase):
    """A suite of tests for the Pdf class"""
    observations = [(C, D)] * 4 + [(C, C)] * 12 + \
                   [(D, C)] * 2 + [(D, D)] * 15
    counter = Counter(observations)
    pdf = Pdf(counter)

    def test_init(self):
        self.assertEqual(set(self.pdf.sample_space), set(self.counter.keys()))
        self.assertEqual(set(self.pdf.counts), set([4, 12, 2, 15]))
        self.assertEqual(self.pdf.total, sum([4, 12, 2, 15]))
        self.assertAlmostEqual(sum(self.pdf.probability), 1)

    def test_sample(self):
        """Test that sample maps to correct domain"""
        all_samples = []

        seed(0)
        for sample in range(100):
            all_samples.append(self.pdf.sample())

        self.assertEqual(len(all_samples), 100)
        self.assertEqual(set(all_samples), set(self.observations))

    def test_seed(self):
        """Test that numpy seeds the sample properly"""

        for s in range(10):
            seed(s)
            sample = self.pdf.sample()
            seed(s)
            self.assertEqual(sample, self.pdf.sample())
