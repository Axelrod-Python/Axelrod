import unittest

import numpy

import axelrod


class TestResultSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = ('Player1', 'Player2', 'Player3')
        cls.test_results = numpy.array([
            [[0, 0], [10, 10], [21, 21]],
            [[10, 8], [0, 0], [16, 20]],
            [[16, 16], [16, 16], [0, 0]]])
        cls.expected_scores = numpy.array(
            [[31, 31],
             [26, 28],
             [32, 32]])
        cls.expected_payoffs = numpy.array([
            [0.0, 2.0, 4.2],
            [1.8, 0.0, 3.6],
            [3.2, 3.2, 0.0]
        ])
        cls.expected_ranking = [1, 0, 2]
        cls.expected_ranked_names = ['Player2', 'Player1', 'Player3']
        cls.expected_csv = 'Player2, Player1, Player3\n26, 31, 32\n28, 31, 32\n'

    def test_init(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        expected_results = numpy.zeros((3, 3, 2))
        self.assertEquals(rs.nplayers, 3)
        self.assertEquals(rs.players, self.players)
        self.assertEquals(rs.turns, 5)
        self.assertEquals(rs.repetitions, 2)
        self.assertTrue((rs.results == expected_results).all())
        self.assertFalse(rs.output_initialised)

    def test_generate_scores(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        rs.results = self.test_results
        self.assertTrue(numpy.array_equal(rs.generate_scores(), self.expected_scores))

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
        payoffs = rs.generate_payoff_matrix()
        self.assertTrue((payoffs == self.expected_payoffs).all())

    def test_init_output(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        rs.results = self.test_results
        rs.init_output()
        self.assertTrue(numpy.array_equal(rs.scores, self.expected_scores))
        self.assertEquals(rs.ranking, self.expected_ranking)
        self.assertEquals(rs.ranked_names, self.expected_ranked_names)
        self.assertTrue(rs.output_initialised)

    def test_csv(self):
        rs = axelrod.ResultSet(self.players, 5, 2)
        rs.results = self.test_results
        self.assertEquals(rs.csv(), self.expected_csv)

if __name__ == '__main__':
    unittest.main()
