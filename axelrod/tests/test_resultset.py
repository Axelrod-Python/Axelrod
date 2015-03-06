import unittest
import numpy
import axelrod


class TestResultSet(unittest.TestCase):

    def test_init(self):
        players = (axelrod.Player(), axelrod.Player())
        rs = axelrod.ResultSet(players, 10, 4)
        expected_results = [
            [[0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0]]
        ]
        self.assertEquals(rs.nplayers, 2)
        self.assertEquals(rs.players, players)
        self.assertEquals(rs.turns, 10)
        self.assertEquals(rs.repetitions, 4)
        self.assertEquals(rs.results, expected_results)
        self.assertFalse(rs.output_initialised)

    def test_generate_scores(self):
        players = players = ('Player1', 'Player2', 'Player3')
        rs = axelrod.ResultSet(players, 5, 2)
        rs.results = [
            [[0, 0], [10, 10], [21, 21]],
            [[10, 8], [0, 0], [16, 20]],
            [[16, 16], [16, 16], [0, 0]]]
        expected_results = numpy.array(
            [[31, 31],
             [26, 28],
             [32, 32]])
        self.assertTrue(numpy.array_equal(rs.generate_scores(), expected_results))

    def test_generate_ranking(self):
        players = ('Player1', 'Player2', 'Player3')
        rs = axelrod.ResultSet(players, 5, 2)
        rs.results = [
            [[0, 0], [10, 10], [21, 21]],
            [[10, 8], [0, 0], [16, 20]],
            [[16, 16], [16, 16], [0, 0]]]
        scores = rs.generate_scores()
        expected_results = [1, 0, 2]
        self.assertEquals(rs.generate_ranking(scores), expected_results)

    def test_generate_ranked_names(self):
        players = ('Player1', 'Player2', 'Player3')
        rs = axelrod.ResultSet(players, 5, 2)
        rs.results = [
            [[0, 0], [10, 10], [21, 21]],
            [[10, 8], [0, 0], [16, 20]],
            [[16, 16], [16, 16], [0, 0]]]
        scores = rs.generate_scores()
        rankings = rs.generate_ranking(scores)
        expected_results = ['Player2', 'Player1', 'Player3']
        self.assertEquals(rs.generate_ranked_names(rankings), expected_results)

    def test_init_output(self):
        players = (axelrod.Player(), axelrod.Player())
        rs = axelrod.ResultSet(players, 10, 4)
        rs.init_output()
        expected_scores = numpy.array([[0, 0, 0, 0], [0, 0, 0, 0]])
        expected_ranking = [0, 1]
        expected_names = ['Player', 'Player']
        self.assertTrue(numpy.array_equal(rs.scores, expected_scores))
        self.assertEquals(rs.ranking, expected_ranking)
        self.assertEquals(rs.ranked_names, expected_names)

    def test_csv(self):
        players = ('Player1', 'Player2', 'Player3')
        rs = axelrod.ResultSet(players, 5, 2)
        rs.results = [
            [[0, 0], [10, 10], [21, 21]],
            [[10, 8], [0, 0], [16, 20]],
            [[16, 16], [16, 16], [0, 0]]]
        expected_results = 'Player2, Player1, Player3\n26, 31, 32\n28, 31, 32\n'
        self.assertEquals(rs.csv(), expected_results)

if __name__ == '__main__':
    unittest.main()
