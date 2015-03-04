import unittest
import numpy
import matplotlib
import axelrod


class TestResultSet(unittest.TestCase):

    def test_all_sorted(self):
        """
        A dummy test so that Travis reports a test failure
        and ensures the pull request doesn't look ready to
        merge.
        """
        all_sorted = False
        self.assertTrue(all_sorted)

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
        players = (axelrod.Player(), axelrod.Player())
        rs = axelrod.ResultSet(players, 10, 4)
        expected_results = numpy.array([[0, 0, 0, 0], [0, 0, 0, 0]])
        self.assertTrue(numpy.array_equal(rs.generate_scores(), expected_results))

    def test_generate_ranking(self):
        players = (axelrod.Player(), axelrod.Player())
        rs = axelrod.ResultSet(players, 10, 4)
        scores = rs.generate_scores()
        expected_results = [0, 1]
        self.assertEquals(rs.generate_ranking(scores), expected_results)

    def test_generate_ranked_names(self):
        players = (axelrod.Player(), axelrod.Player())
        rs = axelrod.ResultSet(players, 10, 4)
        scores = rs.generate_scores()
        rankings = rs.generate_ranking(scores)
        expected_results = ['Player', 'Player']
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
        players = (axelrod.Player(), axelrod.Player())
        rs = axelrod.ResultSet(players, 10, 4)
        expected_results = 'Player, Player\n0, 0\n0, 0\n0, 0\n0, 0\n'
        self.assertEquals(rs.csv(), expected_results)
