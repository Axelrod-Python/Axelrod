import unittest

import axelrod


class TestResultSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = ('Player1', 'Player2', 'Player3')
        cls.test_results = [
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
        cls.test_payoffs_list = [
            [[0, 10, 21], [10, 0, 16], [16, 16, 0]],
            [[0, 10, 21], [8, 0, 20], [16, 16, 0]],
        ]
        cls.expected_stddevs = [
            [0.0, 0.0, 0.0],
            [0.20, 0.0, 0.40],
            [0.0, 0.0, 0.0],
        ]
        cls.expected_ranking = [1, 0, 2]
        cls.expected_ranked_names = ['Player2', 'Player1', 'Player3']
        cls.expected_csv = 'Player2,Player1,Player3\n2.6,3.1,3.2\n2.8,3.1,3.2\n'

    def test_init(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        expected_results = [[[0,0] for j in range(3)] for i in range(3)]
        self.assertEquals(rs.nplayers, 3)
        self.assertEquals(rs.players, self.players)
        self.assertEquals(rs.turns, 5)
        self.assertEquals(rs.repetitions, 2)
        self.assertTrue(rs.results, expected_results)
        self.assertFalse(rs.finalised)

    def test_generate_scores(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        rs.results = self.test_results
        self.assertEquals(rs.generate_scores(), self.expected_scores)

    def test_generate_ranking(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        rs.results = self.test_results
        scores = rs.generate_scores()
        self.assertEquals(rs.generate_ranking(scores), self.expected_ranking)

    def test_generate_ranked_names(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        rs.results = self.test_results
        scores = rs.generate_scores()
        rankings = rs.generate_ranking(scores)
        self.assertEquals(rs.generate_ranked_names(rankings), self.expected_ranked_names)

    def test_generate_payoff_matrix(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        rs.results = self.test_results
        payoffs, stddevs = rs.generate_payoff_matrix()
        stddevs = [[round(x, 1) for x in row] for row in stddevs]
        self.assertEquals(payoffs, self.expected_payoffs)
        self.assertEquals(stddevs, self.expected_stddevs)

    def test_finalise(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        rs.finalise(self.test_payoffs_list)
        self.assertEquals(rs.scores, self.expected_scores)
        self.assertEquals(rs.ranking, self.expected_ranking)
        self.assertEquals(rs.ranked_names, self.expected_ranked_names)
        self.assertTrue(rs.finalised)
        self.assertRaises(AttributeError, rs.finalise, self.test_payoffs_list)

    def test_csv(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        self.assertRaises(AttributeError, rs.csv)
        rs.finalise(self.test_payoffs_list)
        rs.results = self.test_results
        self.assertEquals(rs.csv(), self.expected_csv)
