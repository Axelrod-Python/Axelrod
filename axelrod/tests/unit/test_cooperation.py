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

    def test_cooperation_matrix(self):
        cooperation_matrix = ac.cooperation_matrix(
            self.expected_cooperation_results)
        self.assertEqual(cooperation_matrix, self.expected_cooperation_matrix)
