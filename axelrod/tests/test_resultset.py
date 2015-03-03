import unittest
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
        self.assertEquals(rs.results, expected_results)

    def test_plot(self):
        pass

    def test_csv(self):
        pass
