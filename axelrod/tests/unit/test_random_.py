"""Tests for the random functions."""
<<<<<<< HEAD

=======
>>>>>>> First pass on reproducible matches and parallel tournaments with random seeding
import unittest

import random

from collections import Counter

<<<<<<< HEAD
import numpy
=======
from axelrod import Action, BulkRandomGenerator, Pdf, RandomGenerator
>>>>>>> First pass on reproducible matches and parallel tournaments with random seeding

import axelrod as axl

C, D = axl.Action.C, axl.Action.D


class TestRandomGenerator(unittest.TestCase):
    def test_return_values(self):
<<<<<<< HEAD
        self.assertEqual(axl.random_choice(1), C)
        self.assertEqual(axl.random_choice(0), D)
        axl.seed(1)
        self.assertEqual(axl.random_choice(), C)
        axl.seed(2)
        self.assertEqual(axl.random_choice(), D)

    def test_set_seed(self):
        """Test that numpy and stdlib random seed is set by axelrod seed"""

        numpy_random_numbers = []
        stdlib_random_numbers = []
        for _ in range(2):
            axl.seed(0)
            numpy_random_numbers.append(numpy.random.random())
            stdlib_random_numbers.append(random.random())

        self.assertEqual(numpy_random_numbers[0], numpy_random_numbers[1])
        self.assertEqual(stdlib_random_numbers[0], stdlib_random_numbers[1])
=======
        random = RandomGenerator()
        self.assertEqual(random.random_choice(1), C)
        self.assertEqual(random.random_choice(0), D)
        random.seed(1)
        self.assertEqual(random.random_choice(), C)
        random.seed(2)
        self.assertEqual(random.random_choice(), D)
>>>>>>> First pass on reproducible matches and parallel tournaments with random seeding

    def test_seed_not_offset_by_deterministic_call(self):
        """Test that when called with p = 0 or 1, the random seed is not
        affected."""
        random = RandomGenerator()
        for p in [0, 1]:
<<<<<<< HEAD
            axl.seed(0)
            r = random.random()
            axl.seed(0)
            axl.random_choice(p)
            self.assertEqual(r, random.random())

    def test_random_flip(self):
        self.assertEqual(C, axl.random_flip(C, 0))
        self.assertEqual(C, axl.random_flip(D, 1))
        axl.seed(0)
        self.assertEqual(C, axl.random_flip(C, 0.2))
        axl.seed(1)
        self.assertEqual(C, axl.random_flip(D, 0.2))
=======
            random.seed(0)
            r = random.random()
            random.seed(0)
            random.random_choice(p)
            self.assertEqual(r, random.random())

    def test_random_flip(self):
        random = RandomGenerator()
        self.assertEqual(C, random.random_flip(C, 0))
        self.assertEqual(C, random.random_flip(D, 1))
        random.seed(0)
        self.assertEqual(C, random.random_flip(C, 0.1))
        random.seed(1)
        self.assertEqual(C, random.random_flip(D, 0.8))


class TestBulkRandomGenerator(unittest.TestCase):
    def test_generator(self):
        """Test that the generator produces arrays of random values of
        the expected length and that seeding works properly."""
        batch_size = 100
        batches = 20

        # Test that we get the same results for two instances when the
        # seeds are equal
        rg1 = BulkRandomGenerator(seed=0, batch_size=batch_size)
        randoms1 = [next(rg1) for _ in range(batches * batch_size)]
        self.assertEqual(batches * batch_size, len(randoms1))

        rg2 = BulkRandomGenerator(seed=0, batch_size=batch_size)
        randoms2 = [next(rg2) for _ in range(batches * batch_size)]
        self.assertEqual(batches * batch_size, len(randoms2))

        self.assertSequenceEqual(randoms1, randoms2)

        # Test that we get different results for different seeds
        rg3 = BulkRandomGenerator(seed=50, batch_size=batch_size)
        randoms3 = [next(rg3) for _ in range(batches * batch_size)]
        self.assertEqual(len(randoms3), len(randoms2))
        self.assertNotIn(randoms3[-1], randoms2)
>>>>>>> First pass on reproducible matches and parallel tournaments with random seeding


class TestPdf(unittest.TestCase):
    """A suite of tests for the Pdf class"""

    observations = [(C, D)] * 4 + [(C, C)] * 12 + [(D, C)] * 2 + [(D, D)] * 15
    counter = Counter(observations)
    pdf = axl.Pdf(counter)

    def test_init(self):
        self.assertEqual(set(self.pdf.sample_space), set(self.counter.keys()))
        self.assertEqual(set(self.pdf.counts), set([4, 12, 2, 15]))
        self.assertEqual(self.pdf.total, sum([4, 12, 2, 15]))
        self.assertAlmostEqual(sum(self.pdf.probability), 1)

    def test_sample(self):
        """Test that sample maps to correct domain"""
        all_samples = []
<<<<<<< HEAD

        axl.seed(0)
=======
        random = RandomGenerator()
        random.seed(0)
>>>>>>> First pass on reproducible matches and parallel tournaments with random seeding
        for sample in range(100):
            all_samples.append(self.pdf.sample())

        self.assertEqual(len(all_samples), 100)
        self.assertEqual(set(all_samples), set(self.observations))

    def test_seed(self):
        """Test that numpy seeds the sample properly"""

        for s in range(10):
<<<<<<< HEAD
            axl.seed(s)
            sample = self.pdf.sample()
            axl.seed(s)
            self.assertEqual(sample, self.pdf.sample())
=======
            pdf1 = Pdf(self.counter, s)
            sample = pdf1.sample()
            pdf2 = Pdf(self.counter, s)
            self.assertEqual(sample, pdf2.sample())
>>>>>>> First pass on reproducible matches and parallel tournaments with random seeding
