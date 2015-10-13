import unittest
import axelrod


class TestResultSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = ('Alternator', 'TitForTat', 'Random')
        cls.test_outcome = {
            'payoff': [
                [[11.0, 13, 15], [13, 15.0, 14], [10, 14, 8.0]],
                [[11.0, 13, 12], [13, 15.0, 7], [12, 12, 14.5]],
            ],
            'cooperation': [
                [[3, 3, 3], [3, 5, 4], [4, 4, 1]],
                [[3, 3, 3], [3, 5, 2], [3, 1, 4]]
            ]}

        cls.expected_null_results_matrix = [
            [[0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0]],
        ]

        cls.expected_results = {
            'payoff': [
                [[11.0, 11.0], [13, 13], [15, 12]],
                [[13, 13], [15.0, 15.0], [14, 7]],
                [[10, 12], [14, 12], [8.0, 14.5]],
            ],
            'cooperation': [
                [[3, 3], [3, 3], [3, 3]],
                [[3, 3], [5, 5], [4, 2]],
                [[4, 3], [4, 1], [1, 4]]
            ]
        }

        cls.expected_csv = (
            'Alternator,Random,TitForTat\n2.8,2.4,2.7\n2.5,2.4,2.0\n')

    def test_init(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(rs.players, self.players)
        self.assertEqual(rs.nplayers, 3)
        self.assertEqual(rs.turns, 5)
        self.assertEqual(rs.repetitions, 2)
        self.assertEqual(rs.outcome, self.test_outcome)
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome, False)
        self.assertEqual(rs.cooperation, None)

    def test_null_results_matrix(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(
            rs._null_results_matrix, self.expected_null_results_matrix)

    def test_results(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(rs._results(self.test_outcome), self.expected_results)
        self.assertEqual(rs.results, self.expected_results)

    def test_csv(self):
        rs = axelrod.ResultSet(self.players, 5, 2, self.test_outcome)
        self.assertEqual(rs.csv(), self.expected_csv)
