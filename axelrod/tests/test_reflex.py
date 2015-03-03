"""
Test suite for Reflex Axelrod PD player.
"""
import axelrod
from test_player import TestPlayer


class Reflex_test(TestPlayer):

    def test_initial_nice_strategy(self):
        """ First response should always be cooperation. """
        p1 = axelrod.Reflex()
        p2 = axelrod.Player()
        self.assertEqual(p1.strategy(p2), 'C')


    def test_representation(self):
        """ How do we appear? """
        p1 = axelrod.Reflex()
        self.assertEqual(str(p1), "Reflex")


    def test_reset_method(self):
        """ Does self.reset() reset the self? """
        p1 = axelrod.Reflex()
        p1.history = ['C', 'D', 'C', 'C']
        p1.reset()
        self.assertEqual(p1.history, [])
        self.assertEqual(p1.response, 'C')

    def test_stochastic(self):
        """ We are not stochastic. """
        self.assertFalse(axelrod.Reflex().stochastic)
