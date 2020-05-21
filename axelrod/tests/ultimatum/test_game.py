import numpy as np
import unittest

from axelrod.ultimatum.game import UltimatumScorer

class TestUltimatumScorer(unittest.TestCase):
    def test_accept(self):
        scorer = UltimatumScorer()
        np.testing.assert_almost_equal(scorer.score((0.5, True)), (0.5, 0.5))
        np.testing.assert_almost_equal(scorer.score((0.3, True)), (0.7, 0.3))
        np.testing.assert_almost_equal(scorer.score((0.0, True)), (1.0, 0.0))
        np.testing.assert_almost_equal(scorer.score((1.0, True)), (0.0, 1.0))

    def test_reject(self):
        scorer = UltimatumScorer()
        np.testing.assert_almost_equal(scorer.score((0.5, False)), (0.0, 0.0))
        np.testing.assert_almost_equal(scorer.score((0.0, False)), (0.0, 0.0))
        np.testing.assert_almost_equal(scorer.score((1.0, False)), (0.0, 0.0))
