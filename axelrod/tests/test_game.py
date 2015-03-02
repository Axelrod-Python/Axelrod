import unittest
import axelrod


class TestGame(unittest.TestCase):

    def test_score(self):
        g = axelrod.Game()
        self.assertEquals(g.score(('C', 'C')), (2, 2))
        self.assertEquals(g.score(('D', 'D')), (4, 4))
        self.assertEquals(g.score(('C', 'D')), (5, 0))
        self.assertEquals(g.score(('D', 'C')), (0, 5))
