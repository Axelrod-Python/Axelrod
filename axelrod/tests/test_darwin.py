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
        self.assertTrue(len(self.player.valid_callers)>0)
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
        p1 = self.player()
        p1.reset()
        self.assertEqual(p1.history, [])
        self.assertEqual(p1.genome[0], 'C')
