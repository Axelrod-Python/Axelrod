"""Test for eigen.py."""

import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal

from axelrod.eigen import _normalise, principal_eigenvector


class FunctionCases(unittest.TestCase):
    def test_identity_matrices(self):
        for size in range(2, 6):
            mat = np.identity(size)
            evector, evalue = principal_eigenvector(mat)
            self.assertAlmostEqual(evalue, 1)
            assert_array_almost_equal(evector, _normalise(np.ones(size)))

    def test_zero_matrix(self):
        mat = np.array([[0, 0], [0, 0]])
        evector, evalue = principal_eigenvector(mat)
        self.assertTrue(np.isnan(evalue))
        self.assertTrue(np.isnan(evector[0]))
        self.assertTrue(np.isnan(evector[1]))

    def test_2x2_matrix(self):
        mat = np.array([[2, 1], [1, 2]])
        evector, evalue = principal_eigenvector(mat)
        self.assertAlmostEqual(evalue, 3)
        assert_array_almost_equal(evector, np.dot(mat, evector) / evalue)
        assert_array_almost_equal(evector, _normalise(np.array([1, 1])))

    def test_3x3_matrix(self):
        mat = np.array([[1, 2, 0], [-2, 1, 2], [1, 3, 1]])
        evector, evalue = principal_eigenvector(
            mat, maximum_iterations=None, max_error=1e-10
        )
        self.assertAlmostEqual(evalue, 3)
        assert_array_almost_equal(evector, np.dot(mat, evector) / evalue)
        assert_array_almost_equal(evector, _normalise(np.array([0.5, 0.5, 1])))

    def test_4x4_matrix(self):
        mat = np.array([[2, 0, 0, 0], [1, 2, 0, 0], [0, 1, 3, 0], [0, 0, 1, 3]])
        evector, evalue = principal_eigenvector(
            mat, maximum_iterations=None, max_error=1e-10
        )
        self.assertAlmostEqual(evalue, 3, places=3)
        assert_array_almost_equal(evector, np.dot(mat, evector) / evalue)
        assert_array_almost_equal(
            evector, _normalise(np.array([0, 0, 0, 1])), decimal=4
        )
