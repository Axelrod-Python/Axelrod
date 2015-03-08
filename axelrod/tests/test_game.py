import unittest

import axelrod


class TestGame(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()

    def test_init(self):
        expected_scores = {('C', 'D'): (5, 0), ('D', 'C'): (0, 5), ('D', 'D'): (4, 4), ('C', 'C'): (2, 2)}
        self.assertEquals(self.game.scores, expected_scores)

    def test_RPTS(self):
        expected_values = (2, 4, 5, 0)
        self.assertEquals(self.game.RPTS(), expected_values)

    def test_score(self):
        self.assertEquals(self.game.score(('C', 'C')), (2, 2))
        self.assertEquals(self.game.score(('D', 'D')), (4, 4))
        self.assertEquals(self.game.score(('C', 'D')), (5, 0))
        self.assertEquals(self.game.score(('D', 'C')), (0, 5))
