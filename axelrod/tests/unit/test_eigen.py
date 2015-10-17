"""
Test for eigen.py
"""

import unittest

import numpy
from numpy.testing import assert_array_almost_equal

from axelrod.eigen import normalise, principal_eigenvector


class FunctionCases(unittest.TestCase):

    def test_eigen_1(self):
        # Test identity matrices
        for size in range(2, 6):
            mat = numpy.identity(size)
            evector, evalue = principal_eigenvector(mat)
            self.assertAlmostEqual(evalue, 1)
            assert_array_almost_equal(evector, normalise(numpy.ones(size)))

    def test_eigen_2(self):
        # Test a 2x2 matrix
        mat = [[2, 1], [1, 2]]
        evector, evalue = principal_eigenvector(mat)
        self.assertAlmostEqual(evalue, 3)
        assert_array_almost_equal(evector, numpy.dot(mat, evector) / evalue)
        assert_array_almost_equal(evector, normalise([1, 1]))

    def test_eigen_3(self):
        # Test a 3x3 matrix
        mat = [[1, 2, 0], [-2, 1, 2], [1, 3, 1]]
        evector, evalue = principal_eigenvector(mat)
        self.assertAlmostEqual(evalue, 3)
        assert_array_almost_equal(evector, numpy.dot(mat, evector) / evalue)
        assert_array_almost_equal(evector, normalise([0.5, 0.5, 1]))

    def test_eigen_4(self):
        # Test a 4x4 matrix
        mat = [[2, 0, 0, 0], [1, 2, 0, 0], [0, 1, 3, 0], [0, 0, 1, 3]]
        evector, evalue = principal_eigenvector(mat, max_error=1e-10)
        self.assertAlmostEqual(evalue, 3, places=3)
        assert_array_almost_equal(evector, numpy.dot(mat, evector) / evalue)
        assert_array_almost_equal(evector, normalise([0, 0, 0, 1]), decimal=4)
