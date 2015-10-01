import unittest
import axelrod


class TestResultSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = ('Alternator', 'TitForTat', 'Random')
        cls.test_outcome = {
            'payoff': [
                [[11.0, 13, 15], [13, 15.0, 14], [10, 14, 8.0]],
                [[11.0, 13, 12], [13, 15.0, 7], [12, 12, 14.5]],
            ],
            'cooperation': [
                [[3, 3, 3], [3, 5, 4], [4, 4, 1]],
                [[3, 3, 3], [3, 5, 2], [3, 1, 4]]
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
                [[11.0, 11.0], [13, 13], [15, 12]],
                [[13, 13], [15.0, 15.0], [14, 7]],
                [[10, 12], [14, 12], [8.0, 14.5]],
            ],
            'cooperation': [
                [[3, 3], [3, 3], [3, 3]],
                [[3, 3], [5, 5], [4, 2]],
                [[4, 3], [4, 1], [1, 4]]
            ]
        }
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
        cls.expected_payoffs = [
            [2.2, 2.6, 2.7],
            [2.6, 3.0, 2.1],
            [2.2, 2.6, 2.25]
        ]
        cls.expected_stddevs = [
            [0.0, 0.0, 0.3],
            [0.0, 0.0, 0.7],
            [0.2, 0.2, 0.65]
        ]
        cls.expected_ranking = [0, 2, 1]
        cls.expected_ranked_names = ['Alternator', 'Random', 'TitForTat']
        cls.expected_wins = [[2, 0], [0, 0], [0, 2]]
        cls.expected_cooperation = [
            [6, 6, 6],
            [6, 10, 6],
            [7, 5, 5]
        ]
        cls.expected_normalised_cooperation = [
            [0.6, 0.6, 0.6],
            [0.6, 1.0, 0.6],
            [0.7, 0.5, 0.5]
        ]
        cls.expected_vengeful_cooperation = [
            [0.2, 0.2, 0.2],
            [0.2, 1.0, 0.2],
            [0.4, 0.0, 0.0]]
        cls.expected_cooperating_rating = [0.6, 0.73, 0.57]
        cls.expected_good_partner_matrix = [
            [0, 2, 1],
            [2, 0, 2],
            [2, 1, 0]
        ]
        cls.expected_good_partner_rating = [0.75, 1.0, 0.75]
        cls.expected_eigenjesus_rating = [0.537, 0.678, 0.503]
        cls.expected_eigenmoses_rating = [0.243, 0.966, 0.091]
        cls.expected_csv = (
            'Alternator,Random,TitForTat\n2.8,2.4,2.7\n2.5,2.4,2.0\n')

    def test_init(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(rs.players, self.players)
        self.assertEqual(rs.nplayers, 3)
        self.assertEqual(rs.turns, 5)
        self.assertEqual(rs.repetitions, 2)
        self.assertEqual(rs.outcome, self.test_outcome)
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome, False)
        self.assertEqual(rs.cooperation, None)

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
    def round_matrix(matrix, precision):
        return [[round(x, precision) for x in row] for row in matrix]

    def test_payoff_matrix(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        averages, stddevs = rs._payoff_matrix(self.expected_results['payoff'])
        self.assertEqual(
            self.round_matrix(averages, 2), self.expected_payoffs)
        self.assertEqual(
            self.round_matrix(stddevs, 2), self.expected_stddevs)
        self.assertEqual(
            self.round_matrix(rs.payoff_matrix, 2), self.expected_payoffs)
        self.assertEqual(self.round_matrix(
            rs.payoff_stddevs, 2), self.expected_stddevs)

    def test_wins(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        wins = rs.wins
        self.assertEqual(wins, self.expected_wins)

    def test_winner(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        test_players = (8, 4)
        test_payoffs = (34, 44)
        winner = rs._winner(test_players, test_payoffs)
        self.assertEqual(winner, 4)
        test_payoffs = (54, 44)
        winner = rs._winner(test_players, test_payoffs)
        self.assertEqual(winner, 8)
        test_payoffs = (34, 34)
        winner = rs._winner(test_players, test_payoffs)
        self.assertEqual(winner, None)

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

    def test_vengeful_cooperation(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        vengeful_cooperation = (
            rs._vengeful_cooperation(self.expected_normalised_cooperation))
        self.assertEqual(
            self.round_matrix(vengeful_cooperation, 1),
            self.expected_vengeful_cooperation
        )
        self.assertEqual(
            self.round_matrix(rs.vengeful_cooperation, 1),
            self.expected_vengeful_cooperation)

    @staticmethod
    def round_rating(rating, precision):
        return [round(x, precision) for x in rating]

    def test_cooperating_rating(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        cooperating_rating = rs._cooperating_rating(self.expected_cooperation)
        self.assertEqual(
            self.round_rating(cooperating_rating, 2),
            self.expected_cooperating_rating)
        self.assertEqual(
            self.round_rating(rs.cooperating_rating, 2),
            self.expected_cooperating_rating)

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
        self.assertEqual(rs._interactions, 4)

    def test_good_partner_rating(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        good_partner_rating = (
            rs._good_partner_rating(self.expected_good_partner_matrix))
        self.assertEqual(
            self.round_rating(good_partner_rating, 2),
            self.expected_good_partner_rating
        )
        self.assertEqual(
            self.round_rating(rs.good_partner_rating, 2),
            self.expected_good_partner_rating
        )

    def test_eigenjesus_rating(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        eigenjesus_rating = (
            rs._eigenvector(self.expected_normalised_cooperation))
        self.assertEqual(
            self.round_rating(eigenjesus_rating, 3),
            self.expected_eigenjesus_rating
        )
        self.assertEqual(
            self.round_rating(rs.eigenjesus_rating, 3),
            self.expected_eigenjesus_rating
        )

    def test_eigenmoses_rating(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        eigenmoses_rating = (
            rs._eigenvector(self.expected_vengeful_cooperation))
        self.assertEqual(
            self.round_rating(eigenmoses_rating, 3),
            self.expected_eigenmoses_rating
        )
        self.assertEqual(
            self.round_rating(rs.eigenmoses_rating, 3),
            self.expected_eigenmoses_rating
        )

    def test_csv(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(rs.csv(), self.expected_csv)
