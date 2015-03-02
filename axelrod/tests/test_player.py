import unittest
import axelrod


class TestPlayer(unittest.TestCase):

    def test_initialisation(self):
        """Test that can initiate a player."""
        P1 = axelrod.Player()
        self.assertEqual(P1.history, [])

    def test_play(self):
        """Test that play method looks for attribute strategy (which does not exist)."""
        P1, P2 = axelrod.Player(), axelrod.Player()
        self.assertEquals(P1.play(P2), None)
        self.assertEquals(P2.play(P1), None)
