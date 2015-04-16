import unittest

import axelrod


class TestGame(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()

    def test_init(self):
        expected_scores = {('C', 'D'): (0, 5), ('D', 'C'): (5, 0), ('D', 'D'): (1, 1), ('C', 'C'): (3, 3)}
        self.assertEquals(self.game.scores, expected_scores)

    def test_RPTS(self):
        expected_values = (3, 1, 0, 5)
        self.assertEquals(self.game.RPTS(), expected_values)

    def test_score(self):
        self.assertEquals(self.game.score(('C', 'C')), (3, 3))
        self.assertEquals(self.game.score(('D', 'D')), (1, 1))
        self.assertEquals(self.game.score(('C', 'D')), (0, 5))
        self.assertEquals(self.game.score(('D', 'C')), (5, 0))
