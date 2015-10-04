import unittest
import axelrod.payoff


class TestPayoff(unittest.TestCase):

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

        cls.expected_payoff_matrix = [
            [2.2, 2.6, 2.7],
            [2.6, 3.0, 2.1],
            [2.2, 2.6, 2.25]
        ]
        cls.expected_payoff_stddevs = [
            [0.0, 0.0, 0.3],
            [0.0, 0.0, 0.7],
            [0.2, 0.2, 0.65]
        ]

        cls.expected_wins = [[2, 0], [0, 0], [0, 2]]

    def test_scores(self):
        scores = axelrod.payoff.scores(self.expected_payoff, 3, 2)
        self.assertEqual(scores, self.expected_scores)

    def test_normalised_scores(self):
        scores = axelrod.payoff.normalised_scores(self.expected_scores, 3, 5)
        self.assertEqual(scores, self.expected_normalised_scores)

    def test_median(self):
        median = axelrod.payoff.median([])
        self.assertEqual(median, None)
        median = axelrod.payoff.median([1, 2, 4, 6])
        self.assertEqual(median, 3.0)
        median = axelrod.payoff.median(self.expected_scores)
        self.assertEqual(median, [27, 20])

    def test_ranking(self):
        ranking = axelrod.payoff.ranking(self.expected_scores, 3)
        self.assertEqual(ranking, self.expected_ranking)

    def test_ranked_names(self):
        ranked_names = axelrod.payoff.ranked_names(
            self.players, self.expected_ranking,)
        self.assertEqual(ranked_names, self.expected_ranked_names)

    @staticmethod
    def round_matrix(matrix, precision):
        return [[round(x, precision) for x in row] for row in matrix]

    def test_payoff_matrix(self):
        averages, stddevs = axelrod.payoff.payoff_matrix(self.expected_payoff, 5, 2)
        self.assertEqual(
            self.round_matrix(averages, 2), self.expected_payoff_matrix)
        self.assertEqual(
            self.round_matrix(stddevs, 2), self.expected_payoff_stddevs)

    def test_winning_player(self):
        test_players = (8, 4)
        test_payoffs = (34, 44)
        winner = axelrod.payoff.winning_player(test_players, test_payoffs)
        self.assertEqual(winner, 4)
        test_payoffs = (54, 44)
        winner = axelrod.payoff.winning_player(test_players, test_payoffs)
        self.assertEqual(winner, 8)
        test_payoffs = (34, 34)
        winner = axelrod.payoff.winning_player(test_players, test_payoffs)
        self.assertEqual(winner, None)

    def test_wins(self):
        wins = axelrod.payoff.wins(self.expected_payoff, 3, 2)
        self.assertEqual(wins, self.expected_wins)
