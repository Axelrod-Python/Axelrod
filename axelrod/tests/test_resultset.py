import unittest
import numpy
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
        rs = axelrod.ResultSet(players, 4)
        expected_results = [
            [[0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0]]
        ]
        self.assertEquals(rs.players, players)
        self.assertEquals(rs.results, expected_results)

    def test_scores(self):
        players = (axelrod.Player(), axelrod.Player())
        rs = axelrod.ResultSet(players, 4)
        expected_results = numpy.array([[0, 0, 0, 0], [0, 0, 0, 0]])
        self.assertTrue(numpy.array_equal(rs.scores(), expected_results))

    def test_plot(self):
        pass

    def test_csv(self):
        players = (axelrod.Player(), axelrod.Player())
        rs = axelrod.ResultSet(players, 4)
        expected_results = 'Player, Player\n0, 0\n0, 0\n0, 0\n0, 0\n'
        self.assertEquals(rs.csv(), expected_results)
