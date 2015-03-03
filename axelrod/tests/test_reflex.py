"""
Test suite for Reflex Axelrod PD player.
"""
import axelrod
from test_player import TestPlayer


class Reflex_test(TestPlayer):

    name = "Reflex"
    player = axelrod.Reflex
    stochastic = False


    def test_strategy(self):
        """ First response should always be cooperation. """
        p1 = axelrod.Reflex()
        p2 = axelrod.Player()
        self.assertEqual(p1.strategy(p2), 'C')


    def test_reset_method(self):
        """ Does self.reset() reset the self? """
        p1 = axelrod.Reflex()
        p1.history = ['C', 'D', 'C', 'C']
        p1.reset()
        self.assertEqual(p1.history, [])
        self.assertEqual(p1.response, 'C')
