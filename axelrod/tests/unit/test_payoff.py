import unittest
import axelrod


class TestResultSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.test_payoff = [
            [[11.0, 11.0], [13, 13], [15, 12]],
            [[13, 13], [15.0, 15.0], [14, 7]],
            [[10, 12], [14, 12], [8.0, 14.5]],
        ]

        cls.expected_scores = [
            [28, 25],
            [27, 20],
            [24, 24]
        ]

    def test_scores(self):
        scores = axelrod.scores(self.test_payoff, 3, 2)
        self.assertEqual(scores, self.expected_scores)
