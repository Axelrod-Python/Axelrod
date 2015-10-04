import unittest
import axelrod


class TestResultSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.players = ('Alternator', 'TitForTat', 'Random')

        cls.expected_payoff = [
            [[11.0, 11.0], [13, 13], [15, 12]],
            [[13, 13], [15.0, 15.0], [14, 7]],
            [[10, 12], [14, 12], [8.0, 14.5]],
        ]

        cls.expected_scores = [
            [28, 25],
            [27, 20],
            [24, 24]
        ]

        cls.expected_normalised_scores = [
            [2.8, 2.5],
            [2.7, 2.0],
            [2.4, 2.4]
        ]

        cls.expected_ranking = [0, 2, 1]
        cls.expected_ranked_names = ['Alternator', 'Random', 'TitForTat']

    def test_scores(self):
        scores = axelrod.scores(self.expected_payoff, 3, 2)
        self.assertEqual(scores, self.expected_scores)

    def test_normalised_scores(self):
        scores = axelrod.normalised_scores(self.expected_scores, 3, 5)
        self.assertEqual(scores, self.expected_normalised_scores)

    def test_median(self):
        median = axelrod.median([])
        self.assertEqual(median, None)
        median = axelrod.median([1, 2, 4, 6])
        self.assertEqual(median, 3.0)
        median = axelrod.median(self.expected_scores)
        self.assertEqual(median, [27, 20])

    def test_ranking(self):
        ranking = axelrod.ranking(self.expected_scores, 3)
        self.assertEqual(ranking, self.expected_ranking)

    def test_ranked_names(self):
        ranked_names = axelrod.ranked_names(
            self.players, self.expected_ranking,)
        self.assertEqual(ranked_names, self.expected_ranked_names)
