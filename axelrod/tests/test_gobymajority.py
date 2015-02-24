"""
Test for the go by majority strategy
"""
import unittest
import axelrod

class TestGoByMajority(unittest.TestCase):

    def test_initial_strategy(self):
        """
        Starts by cooperating
        """
        P1 = axelrod.GoByMajority()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """
        If opponent cooperates at least as often as they defect then the player cooperates
        """
        P1 = axelrod.GoByMajority()
        P2 = axelrod.Player()
        P1.history = ['C', 'D', 'D', 'D']
        P2.history = ['D', 'D', 'C', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C', 'C', 'D', 'D', 'D']
        P2.history = ['D', 'D', 'C', 'C', 'D']
        self.assertEqual(P1.strategy(P2), 'D')

    def test_representation(self):
        P1 = axelrod.GoByMajority()
        self.assertEqual(str(P1), 'Go By Majority')

    def test_stochastic(self):
        self.assertFalse(axelrod.GoByMajority().stochastic)

class TestGoByRecentMajority(unittest.TestCase):

    lengths = [5, 10, 20, 40]
    get_player = lambda self, L: getattr(axelrod, 'GoByMajority%i' % L)()

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
        If opponent cooperates at least as often as they defect then the player cooperates
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

    def test_stochastic(self):
        for L in self.lengths:
            self.assertFalse(self.get_player(L).stochastic)