import unittest
import axelrod.cooperation as ac


class TestCooperation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.expected_cooperation_results = [
            [[3, 3], [3, 3], [3, 3]],
            [[3, 3], [5, 5], [4, 2]],
            [[4, 3], [4, 1], [1, 4]]
        ]

        cls.expected_cooperation_matrix = [
            [6, 6, 6],
            [6, 10, 6],
            [7, 5, 5]
        ]

        cls.expected_normalised_cooperation = [
            [0.6, 0.6, 0.6],
            [0.6, 1.0, 0.6],
            [0.7, 0.5, 0.5]
        ]

        cls.expected_vengeful_cooperation = [
            [0.2, 0.2, 0.2],
            [0.2, 1.0, 0.2],
            [0.4, 0.0, 0.0]]

        cls.expected_cooperating_rating = [0.6, 0.73, 0.57]

    def test_cooperation_matrix(self):
        cooperation_matrix = ac.cooperation_matrix(
            self.expected_cooperation_results
        )
        self.assertEqual(cooperation_matrix, self.expected_cooperation_matrix)

    def test_normalised_cooperation(self):
        normalised_cooperation = ac.normalised_cooperation(
            self.expected_cooperation_matrix, 5, 2
        )
        self.assertEqual(
            normalised_cooperation, self.expected_normalised_cooperation
        )

    @staticmethod
    def round_matrix(matrix, precision):
        return [[round(x, precision) for x in row] for row in matrix]

    def test_vengeful_cooperation(self):
        vengeful_cooperation = ac.vengeful_cooperation(
            self.expected_normalised_cooperation
        )
        self.assertEqual(
            self.round_matrix(vengeful_cooperation, 2),
            self.expected_vengeful_cooperation
        )

    @staticmethod
    def round_rating(rating, precision):
        return [round(x, precision) for x in rating]

    def test_cooperating_rating(self):
        cooperating_rating = ac.cooperating_rating(
            self.expected_cooperation_matrix, 3, 5, 2
        )
        self.assertEqual(
            self.round_rating(cooperating_rating, 2),
            self.expected_cooperating_rating
        )
