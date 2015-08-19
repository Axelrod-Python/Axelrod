import unittest
import axelrod


class TestResultSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = ('Player1', 'Player2', 'Player3')
        cls.test_outcome = {
            'payoff': [
                [[0, 10, 21], [10, 0, 16], [16, 16, 0]],
                [[0, 10, 21], [8, 0, 20], [16, 16, 0]],
            ],
            'cooperation': [
                [[0, 5, 5], [1, 4, 4], [2, 2, 3]],
                [[1, 5, 5], [2, 2, 2], [5, 5, 4]]
            ]}
        cls.expected_null_results_matrix = [
            [[0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0]],
        ]
        cls.expected_null_matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        cls.expected_results = {
            'payoff': [
                [[0, 0], [10, 10], [21, 21]],
                [[10, 8], [0, 0], [16, 20]],
                [[16, 16], [16, 16], [0, 0]],
            ],
            'cooperation': [
                [[0, 1], [5, 5], [5, 5]],
                [[1, 2], [4, 2], [4, 2]],
                [[2, 5], [2, 5], [3, 4]]
            ]
        }
        cls.expected_scores = [
            [31, 31],
            [26, 28],
            [32, 32],
        ]
        cls.expected_normalised_scores = [
            [3.1, 3.1],
            [2.6, 2.8],
            [3.2, 3.2],
        ]
        cls.expected_payoffs = [
            [0.0, 2.0, 4.2],
            [1.8, 0.0, 3.6],
            [3.2, 3.2, 0.0],
        ]
        cls.expected_stddevs = [
            [0.0, 0.0, 0.0],
            [0.20, 0.0, 0.40],
            [0.0, 0.0, 0.0],
        ]
        cls.expected_ranking = [2, 0, 1]
        cls.expected_ranked_names = ['Player3', 'Player1', 'Player2']
        cls.expected_cooperation = [
            [1, 10, 10],
            [3, 6, 6],
            [7, 7, 7]
        ]
        cls.expected_normalised_cooperation = [
            [0.1, 1, 1],
            [0.3, 0.6, 0.6],
            [0.7, 0.7, 0.7]
        ]
        cls.expected_cooperation_rates = [0.7, 0.5, 0.7]
        cls.expected_good_partner_matrix = [
            [0, 2, 2],
            [0, 0, 1],
            [1, 1, 0]
        ]
        cls.expected_good_partner_rating = [0.333, 0.083, 0.167]
        cls.expected_csv = (
            'Player3,Player1,Player2\n3.2,3.1,2.6\n3.2,3.1,2.8\n')

    def test_init(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(rs.players, self.players)
        self.assertEqual(rs.nplayers, 3)
        self.assertEqual(rs.turns, 5)
        self.assertEqual(rs.repetitions, 2)
        self.assertEqual(rs.outcome, self.test_outcome)

    def test_null_results_matrix(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(
            rs._null_results_matrix, self.expected_null_results_matrix)

    def test_null_matrix(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(
            rs._null_matrix, self.expected_null_matrix)

    def test_results(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(rs._results(self.test_outcome), self.expected_results)
        self.assertEqual(rs.results, self.expected_results)

    def test_scores(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(
            rs._scores(self.expected_results['payoff']), self.expected_scores)
        self.assertEqual(rs.scores, self.expected_scores)

    def test_normalised_scores(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(
            rs._normalised_scores(self.expected_scores),
            self.expected_normalised_scores)
        self.assertEqual(
            rs.normalised_scores, self.expected_normalised_scores)

    def test_ranking(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(
            rs._ranking(self.expected_scores), self.expected_ranking)
        self.assertEqual(rs.ranking, self.expected_ranking)

    def test_ranked_names(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(
            rs._ranked_names(self.expected_ranking),
            self.expected_ranked_names)
        self.assertEqual(rs.ranked_names, self.expected_ranked_names)

    @staticmethod
    def round_stddevs(stddevs):
        return [[round(x, 1) for x in row] for row in stddevs]

    def test_payoff_matrix(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        averages, stddevs = rs._payoff_matrix(self.expected_results['payoff'])
        self.assertEqual(averages, self.expected_payoffs)
        self.assertEqual(
            self.round_stddevs(stddevs), self.expected_stddevs)
        self.assertEqual(rs.payoff_matrix, self.expected_payoffs)
        self.assertEqual(self.round_stddevs(
            rs.payoff_stddevs), self.expected_stddevs)

    def test_cooperation(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(
            rs._cooperation(self.expected_results['cooperation']),
            self.expected_cooperation)
        self.assertEqual(rs.cooperation, self.expected_cooperation)

    def test_normalised_cooperation(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(
            rs._normalised_cooperation(self.expected_cooperation),
            self.expected_normalised_cooperation
        )
        self.assertEqual(
            rs.normalised_cooperation, self.expected_normalised_cooperation)

    def test_cooperation_rates(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(
            rs._cooperation_rates(self.expected_cooperation),
            self.expected_cooperation_rates)
        self.assertEqual(
            rs.cooperation_rates, self.expected_cooperation_rates)

    def test_good_partner_matrix(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(
            rs._good_partner_matrix(self.expected_results['cooperation']),
            self.expected_good_partner_matrix
        )
        self.assertEqual(
            rs.good_partner_matrix, self.expected_good_partner_matrix
        )

    def test_interactions(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(rs._interactions, 12)

    @staticmethod
    def round_good_partner_rating(good_partner_rating):
        return [round(x, 3) for x in good_partner_rating]

    def test_good_partner_rating(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        good_partner_rating = (
            rs._good_partner_rating(self.expected_good_partner_matrix))
        self.assertEqual(
            self.round_good_partner_rating(good_partner_rating),
            self.expected_good_partner_rating
        )
        self.assertEqual(
            self.round_good_partner_rating(good_partner_rating),
            self.expected_good_partner_rating
        )

    def test_csv(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(rs.csv(), self.expected_csv)
