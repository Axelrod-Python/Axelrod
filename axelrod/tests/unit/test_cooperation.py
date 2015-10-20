import unittest
from axelrod import Actions
import axelrod.cooperation as ac

C, D = Actions.C, Actions.D

class TestCooperation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.interactions = {
            (0, 0): [(C, C), (D, D), (C, C), (D, D), (C, C)],
            (0, 1): [(C, C), (D, C), (C, D), (D, C), (C, D)],
            (0, 2): [(C, C), (D, C), (C, D), (D, C), (C, D)],
            (1, 1): [(C, C), (C, C), (C, C), (C, C), (C, C)],
            (1, 2): [(C, D), (D, D), (D, C), (C, D), (D, C)],
            (2, 2): [(D, C), (D, D), (D, C), (D, D), (D, D)]

        }

        cls.expected_cooperation_matrix = [
            [3, 3, 3],
            [3, 5, 2],
            [3, 2, 0]
        ]

        cls.expected_cooperation_results = [
            [[3, 3], [3, 3], [3, 3]],
            [[3, 3], [5, 5], [4, 2]],
            [[4, 3], [4, 1], [1, 4]]
        ]

        cls.expected_cooperation = [
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

        cls.expected_null_matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        cls.expected_good_partner_matrix = [
            [0, 2, 1],
            [2, 0, 2],
            [2, 1, 0]
        ]

        cls.expected_good_partner_rating = [0.75, 1.0, 0.75]

        cls.expected_eigenvector = [0.54, 0.68, 0.5]

    def test_cooperation_matrix(self):
        cooperation_matrix = ac.cooperation_matrix(self.interactions)
        self.assertEqual(cooperation_matrix, self.expected_cooperation_matrix)

    def test_cooperation(self):
        cooperation_matrix = ac.cooperation(self.expected_cooperation_results)
        self.assertEqual(cooperation_matrix, self.expected_cooperation)

    def test_normalised_cooperation(self):
        normalised_cooperation = ac.normalised_cooperation(
            self.expected_cooperation, 5, 2
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
            self.expected_cooperation, 3, 5, 2
        )
        self.assertEqual(
            self.round_rating(cooperating_rating, 2),
            self.expected_cooperating_rating
        )

    def test_null_matrix(self):
        null_matrix = ac.null_matrix(3)
        self.assertEqual(null_matrix, self.expected_null_matrix)

    def test_good_partner_matrix(self):
        good_partner_matrix = ac.good_partner_matrix(
            self.expected_cooperation_results, 3, 2
        )
        self.assertEqual(good_partner_matrix, self.expected_good_partner_matrix)

    def test_n_interactions(self):
        n_interactions = ac.n_interactions(3, 2)
        self.assertEqual(n_interactions, 4)

    def test_good_partner_rating(self):
        good_partner_rating = ac.good_partner_rating(
            self.expected_good_partner_matrix, 3, 2
        )
        self.assertEqual(good_partner_rating, self.expected_good_partner_rating)

    def test_eigenvector(self):
        eigenvector = ac.eigenvector(self.expected_cooperation)
        self.assertEqual(
            self.round_rating(eigenvector, 2), self.expected_eigenvector
        )
