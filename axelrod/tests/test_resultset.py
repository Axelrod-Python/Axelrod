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
        self.assertEquals(rs.nplayers, 2)
        self.assertEquals(rs.players, players)
        self.assertEquals(rs.results, expected_results)
        self.assertFalse(rs.output_initialised)

    def test_generate_scores(self):
        players = (axelrod.Player(), axelrod.Player())
        rs = axelrod.ResultSet(players, 4)
        expected_results = numpy.array([[0, 0, 0, 0], [0, 0, 0, 0]])
        self.assertTrue(numpy.array_equal(rs.generate_scores(), expected_results))

    def test_generate_ranking(self):
        pass

    def test_generate_ranked_names(self):
        pass

    def test_init_output(self):
        pass

    def test_plot(self):
        pass

    def test_csv(self):
        players = (axelrod.Player(), axelrod.Player())
        rs = axelrod.ResultSet(players, 4)
        expected_results = 'Player, Player\n0, 0\n0, 0\n0, 0\n0, 0\n'
        self.assertEquals(rs.csv(), expected_results)
