import unittest

import axelrod


class TestPlayer(unittest.TestCase):

    name = "Player"
    player = axelrod.Player
    stochastic = False

    def test_initialisation(self):
        """Test that the player initiates correctly."""
        self.assertEqual(self.player().history, [])
        self.assertEqual(self.player().stochastic, self.stochastic)

    def test_repr(self):
        """Test that the representation is correct."""
        self.assertEquals(str(self.player()), self.name)

    def test_strategy(self):
        """Test that strategy method."""
        self.assertEquals(self.player().strategy(self.player()), None)

    def test_reset(self):
        """Make sure reseting works correctly."""
        p = self.player()
        p.history = ['C', 'C']
        p.reset()
        self.assertEquals(p.history, [])
