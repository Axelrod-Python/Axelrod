"""
Test for the go by recent strategy
"""
import unittest
import axelrod

class TestGoByRecent(unittest.TestCase):

    lengths = [5, 10, 20, 40]
    get_player = lambda self, L: getattr(axelrod, 'GoByRecentMajority%i' % L)()

    def test_initial_strategy(self):
        """
        Starts by cooperating
        """
        P2 = axelrod.Player()
        for L in self.lengths:
            P1 = self.get_player(L)
            self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """
        If opponent cooperates at least as often as they defect in the last ten turns then the player cooperates
        """
        P2 = axelrod.Player()
        for L in self.lengths:
            P1 = self.get_player(L)
            P1.history = ['D'] * int(1.5*L)
            P2.history = ['D'] * (L-1) + ['C'] * (L//2 + 1)
            self.assertEqual(P1.strategy(P2), 'C')
            P1.history = ['C'] * int(1.5*L)
            P2.history = ['C'] * (L-1) + ['D'] * (L//2 + 1)
            self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        for L in self.lengths:
            P1 = self.get_player(L)
            self.assertEqual(str(P1), 'Go By Majority/%i' % L)
