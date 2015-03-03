import unittest
import axelrod


class TestResultSet(unittest.TestCase):

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
