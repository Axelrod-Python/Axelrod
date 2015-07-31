import unittest
import axelrod


class TestResultSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = ('Player1', 'Player2', 'Player3')
        cls.test_payoffs_list = [
            [[0, 10, 21], [10, 0, 16], [16, 16, 0]],
            [[0, 10, 21], [8, 0, 20], [16, 16, 0]],
        ]
        cls.test_cooperation_list = []
        cls.expected_null_results = [
            [[0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0]],
        ]
        cls.expected_results = [
            [[0, 0], [10, 10], [21, 21]],
            [[10, 8], [0, 0], [16, 20]],
            [[16, 16], [16, 16], [0, 0]],
        ]
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
        cls.expected_csv = (
            'Player3,Player1,Player2\n3.2,3.1,2.6\n3.2,3.1,2.8\n')

    def test_init(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_payoffs_list,
                               self.test_cooperation_list)
        self.assertEqual(rs.players, self.players)
        self.assertEqual(rs.nplayers, 3)
        self.assertEqual(rs.turns, 5)
        self.assertEqual(rs.repetitions, 2)
        self.assertEqual(rs.payoffs_list, self.test_payoffs_list)
        self.assertEqual(rs.cooperation_list, self.test_cooperation_list)

    def test_null_results_matrix(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_payoffs_list,
                               self.test_cooperation_list)
        self.assertEqual(rs._null_results_matrix(), self.expected_null_results)

    def test_results_matrix(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_payoffs_list,
                               self.test_cooperation_list)
        self.assertEqual(rs._results_matrix(), self.expected_results)
        self.assertEqual(rs.results, self.expected_results)

    def test_scores(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_payoffs_list,
                               self.test_cooperation_list)
        self.assertEqual(rs._scores(), self.expected_scores)
        self.assertEqual(rs.scores, self.expected_scores)

    def test_normalised_scores(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_payoffs_list,
                               self.test_cooperation_list)
        self.assertEqual(
            rs._normalised_scores(), self.expected_normalised_scores)
        self.assertEqual(
            rs.normalised_scores, self.expected_normalised_scores)

    def test_ranking(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_payoffs_list,
                               self.test_cooperation_list)
        self.assertEqual(
            rs._ranking(self.expected_scores), self.expected_ranking)
        self.assertEqual(rs.ranking, self.expected_ranking)

    def test_ranked_names(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_payoffs_list,
                               self.test_cooperation_list)
        self.assertEqual(
            rs._ranked_names(self.expected_ranking),
            self.expected_ranked_names)
        self.assertEqual(rs.ranked_names, self.expected_ranked_names)

    @staticmethod
    def round_stddevs(stddevs):
        return [[round(x, 1) for x in row] for row in stddevs]

    def test_payoff_matrix(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_payoffs_list,
                               self.test_cooperation_list)
        self.assertEqual(rs._payoff_matrix()[0], self.expected_payoffs)
        self.assertEqual(
            self.round_stddevs(rs._payoff_matrix()[1]), self.expected_stddevs)
        self.assertEqual(rs.payoff_matrix, self.expected_payoffs)
        self.assertEqual(self.round_stddevs(
            rs.payoff_stddevs), self.expected_stddevs)

    def test_csv(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_payoffs_list,
                               self.test_cooperation_list)
        self.assertEqual(rs.csv(), self.expected_csv)
