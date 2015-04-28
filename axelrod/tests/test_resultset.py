import unittest

import axelrod


class TestResultSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = ('Player1', 'Player2', 'Player3')
        cls.expected_initial_results = [
            [[0, 0] for j in range(3)] for i in range(3)]
        cls.test_payoffs_list = [
            [[0, 10, 21], [10, 0, 16], [16, 16, 0]],
            [[0, 10, 21], [8, 0, 20], [16, 16, 0]],
        ]
        cls.expected_results = [
            [[0, 0], [10, 10], [21, 21]],
            [[10, 8], [0, 0], [16, 20]],
            [[16, 16], [16, 16], [0, 0]],
        ]
        cls.expected_scores = [
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
        cls.expected_csv = 'Player3,Player1,Player2\n3.2,3.1,2.6\n3.2,3.1,2.8\n'

    def test_init(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        self.assertEquals(rs.nplayers, 3)
        self.assertEquals(rs.players, self.players)
        self.assertEquals(rs.turns, 5)
        self.assertEquals(rs.repetitions, 2)
        self.assertTrue(rs._results, self.expected_initial_results)
        self.assertFalse(rs._finalised)

    def test_payoffs(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        rs.payoffs_list = self.test_payoffs_list
        self.assertEquals(rs.payoffs_list, self.test_payoffs_list)
        del(rs.payoffs_list)
        self.assertFalse(rs._finalised)

    def test_results(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        self.assertRaises(AttributeError, getattr, rs, 'results')
        rs.payoffs_list = self.test_payoffs_list
        self.assertEquals(rs.results, self.expected_results)
        del(rs.payoffs_list)
        self.assertTrue(rs._results, self.expected_initial_results)

    def test_scores(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        self.assertRaises(AttributeError, getattr, rs, 'scores')
        rs.payoffs_list = self.test_payoffs_list
        self.assertEquals(rs.scores, self.expected_scores)

    def test_ranking(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        self.assertRaises(AttributeError, getattr, rs, 'ranking')
        rs.payoffs_list = self.test_payoffs_list
        self.assertEquals(rs.ranking, self.expected_ranking)

    def test_ranked_names(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        self.assertRaises(AttributeError, getattr, rs, 'ranked_names')
        rs.payoffs_list = self.test_payoffs_list
        self.assertEquals(rs.ranked_names, self.expected_ranked_names)

    def test_payoff_matrix(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        self.assertRaises(AttributeError, getattr, rs, 'payoff_matrix')
        self.assertRaises(AttributeError, getattr, rs, 'payoff_stddevs')
        rs.payoffs_list = self.test_payoffs_list
        stddevs = [[round(x, 1) for x in row] for row in rs.payoff_stddevs]
        self.assertEquals(rs.payoff_matrix, self.expected_payoffs)
        self.assertEquals(stddevs, self.expected_stddevs)

    def test_csv(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        self.assertRaises(AttributeError, rs.csv)
        rs.payoffs_list = self.test_payoffs_list
        self.assertEquals(rs.csv(), self.expected_csv)
