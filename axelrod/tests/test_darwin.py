"""
    Tests for the Darwin PD strategy.
"""

import axelrod
from test_player import TestPlayer

class TestDarwin(TestPlayer):

    name = "Darwin"
    player = axelrod.Darwin

    def test_strategy(self):
        p1 = self.player()
        p2 = axelrod.Player()
        self.assertEqual(p1.strategy(p2), 'C') # Always cooperate first.


    def test_play(self):
        """valid_callers must contain at least one entry..."""
        self.assertTrue(len(self.player.valid_callers)>0)
        """...and should allow round_robin.play to call"""
        self.assertTrue("play" in self.player.valid_callers)
        self.play()


    def play(self):
        """We need this to circumvent the agent's anti-inspection measure"""
        p1 = self.player()
        p2 = axelrod.Player()
        p1.reset()
        p1.strategy(p2)
        # Genome contains only valid responses.
        self.assertEqual(p1.genome.count('C') + p1.genome.count('D'), len(p1.genome))


    def test_reset(self):
        """Is instance correctly reset between rounds"""
        p1 = self.player()
        p1.reset()
        self.assertEqual(p1.history, [])
        self.assertEqual(p1.genome[0], 'C')


    def test_unique_genome(self):
        """Ensure genome remains unique class property"""
        p1 = self.player()
        p2 = self.player()
        self.assertTrue(p1.genome is p2.genome)
