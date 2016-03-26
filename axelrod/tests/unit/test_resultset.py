import unittest
import axelrod

from hypothesis import given
from hypothesis.strategies import floats, integers

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

class TestProbEndResultSet(TestResultSet):

    @classmethod
    def setUpClass(cls):
        cls.players = ('Alternator', 'TitForTat', 'Random')
        cls.test_outcome = {
            'cooperation': [
                    [[1, 3, 3],
                     [4, 1, 1],
                     [3, 0, 1]],
                    [[5, 4, 1],
                     [4, 1, 3],
                     [1, 3, 5]]
                            ],
             'match_lengths': [
                    [[1, 6, 5],
                     [6, 1, 2],
                     [5, 2, 2]],
                    [[9, 7, 1],
                     [7, 1, 3],
                     [1, 3, 8]]],
             'payoff': [
                    [[3, 18, 12],
                     [13, 3, 1],
                     [12, 6, 8]],
                    [[19, 18, 3],
                     [18, 3, 9],
                     [3, 9, 22]]]
            }

        cls.expected_null_results_matrix = [
            [[0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0]],
        ]

        cls.expected_match_lengths = [[11, 8], [8, 10], [7, 4]]

        cls.expected_results = {
                'cooperation': [
                    [[1, 5], [3, 4], [3, 1]],
                    [[4, 4], [1, 1], [1, 3]],
                    [[3, 1], [0, 3], [1, 5]]],
                'match_lengths': [
                    [[1, 9], [6, 7], [5, 1]],
                    [[6, 7], [1, 1], [2, 3]],
                    [[5, 1], [2, 3], [2, 8]]],
                'payoff': [
                    [[3, 19], [18, 18], [12, 3]],
                    [[13, 18], [3, 3], [1, 9]],
                    [[12, 3], [6, 9], [8, 22]]]}

    @given(p_end=floats(min_value=.05, max_value=1))
    def test_init(self, p_end):
        rs = axelrod.ProbEndResultSet(self.players, p_end,
                                      2, self.test_outcome)
        self.assertEqual(rs.players, self.players)
        self.assertEqual(rs.nplayers, 3)
        self.assertEqual(rs.prob_end, p_end)
        self.assertEqual(rs.repetitions, 2)
        self.assertEqual(len(rs.outcome), 3)
        self.assertIn('match_lengths', rs.outcome)
        self.assertIn('payoff', rs.outcome)
        self.assertIn('cooperation', rs.outcome)

    @given(p_end=floats(min_value=.05, max_value=1))
    def test_null_results_matrix(self, p_end):
        rs = axelrod.ProbEndResultSet(self.players, p_end, 2, self.test_outcome)
        self.assertEqual(
            rs._null_results_matrix, self.expected_null_results_matrix)

    def test_results(self):
        rs = axelrod.ProbEndResultSet(self.players, .3, 2, self.test_outcome)
        self.assertEqual(rs._results(self.test_outcome), self.expected_results)
        self.assertEqual(rs.results, self.expected_results)

    def test_format_match_lengths(self):
        rs = axelrod.ProbEndResultSet(self.players, .3, 2, self.test_outcome)
        self.assertEqual(rs._format_match_length(self.test_outcome['match_lengths']),
                         self.expected_match_lengths)

    @given(p_end=floats(min_value=.05, max_value=1))
    def test_csv(self, p_end):
        rs = axelrod.ProbEndResultSet(self.players, p_end, 2, self.test_outcome)
        self.assertIsInstance(rs.csv(), str)
