"""Tests for the random functions."""

import unittest
from collections import Counter

import axelrod as axl
from axelrod import BulkRandomGenerator, Pdf, RandomGenerator

C, D = axl.Action.C, axl.Action.D


class TestRandomGenerator(unittest.TestCase):
    def test_return_values(self):
        # The seed doesn't matter for p=0 or p=1
        for seed in range(10):
            random = RandomGenerator(seed=seed)
            self.assertEqual(random.random_choice(1), C)
            self.assertEqual(random.random_choice(0), D)
        random.seed(1)
        self.assertEqual(random.random_choice(0.5), C)
        random.seed(3)
        self.assertEqual(random.random_choice(0.5), D)

    def test_seed_not_offset_by_deterministic_call(self):
        """Test that when called with p = 0 or 1, the random seed is not
        affected."""
        random = RandomGenerator()
        for p in [0, 1]:
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


class TestPdf(unittest.TestCase):
    """A suite of tests for the Pdf class"""

    observations = [(C, D)] * 4 + [(C, C)] * 12 + [(D, C)] * 2 + [(D, D)] * 15
    counter = Counter(observations)
    pdf = axl.Pdf(counter)

    def test_init(self):
        self.assertEqual(set(self.pdf.sample_space), set(self.counter.keys()))
        self.assertEqual(set(self.pdf.counts), {4, 12, 2, 15})
        self.assertEqual(self.pdf.total, sum([4, 12, 2, 15]))
        self.assertAlmostEqual(sum(self.pdf.probability), 1)

    def test_sample(self):
        """Test that sample maps to correct domain"""
        all_samples = []
        random = RandomGenerator()
        random.seed(0)
        for sample in range(100):
            all_samples.append(self.pdf.sample())

        self.assertEqual(len(all_samples), 100)
        self.assertEqual(set(all_samples), set(self.observations))

    def test_seed(self):
        """Test that numpy seeds the sample properly"""

        for s in range(10):
            pdf1 = Pdf(self.counter, s)
            sample = pdf1.sample()
            pdf2 = Pdf(self.counter, s)
            self.assertEqual(sample, pdf2.sample())
