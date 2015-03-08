"""Test for the golden and other mathematical strategies."""

import axelrod

from test_player import TestPlayer


class TestGolden(TestPlayer):

    name = '$\phi$'
    player = axelrod.Golden

    def test_strategy(self):
        """test initial strategy co-operates"""
        P1 = axelrod.Golden()
        P2 = axelrod.Player()
        P2.history = []
        self.assertEqual(P1.strategy(P2), 'C')

    def test_when_no_defection(self):
        """tests that if the opposing player does not defect initially then strategy defects"""
        P1 = axelrod.Golden()
        P2 = axelrod.Player()
        P1.history = ['C']
        P2.history = ['C']
        self.assertEqual(P1.strategy(P2), 'D')

    def test_when_greater_than_golden_ratio(self):
        """tests that if the ratio of Cs to Ds is greater than the golden ratio then strategy defects"""
        P1 = axelrod.Golden()
        P2 = axelrod.Player()
        P1.history = ['C','C','C','C']
        P2.history = ['C','C','D','D']
        self.assertEqual(P1.strategy(P2), 'D')

    def test_when_less_than_golder_ratio(self):
        """tests that if the ratio of Cs to Ds is less than the golden ratio then strategy co-operates"""
        P1 = axelrod.Golden()
        P2 = axelrod.Player()
        P1.history = ['C','C','C','C']
        P2.history = ['D','D','D','D']
        self.assertEqual(P1.strategy(P2), 'C')


class TestPi(TestPlayer):

    name = '$\pi$'
    player = axelrod.Pi

    def test_strategy(self):
        """test initial strategy co-operates"""
        P1 = axelrod.Pi()
        P2 = axelrod.Player()
        P2.history = []
        self.assertEqual(P1.strategy(P2), 'C')

    def test_when_no_defection(self):
        """tests that if the opposing player does not defect initially then strategy defects"""
        P1 = axelrod.Pi()
        P2 = axelrod.Player()
        P1.history = ['C']
        P2.history = ['C']
        self.assertEqual(P1.strategy(P2), 'D')

    def test_when_greater_than_pi(self):
        """tests that if the ratio of Cs to Ds is greater than pi then strategy defects"""
        P1 = axelrod.Pi()
        P2 = axelrod.Player()
        P1.history = ['C','C','C','C']
        P2.history = ['C','C','C','D']
        self.assertEqual(P1.strategy(P2), 'D')

    def test_when_less_than_pi(self):
        """tests that if the ratio of Cs to Ds is less than pi then strategy co-operates"""
        P1 = axelrod.Pi()
        P2 = axelrod.Player()
        P1.history = ['C','C','C','C']
        P2.history = ['C','C','D','D']
        self.assertEqual(P1.strategy(P2), 'C')


class e(TestPlayer):

    name = '$e$'
    player = axelrod.e

    def test_strategy(self):
        """test initial strategy co-operates"""
        P1 = axelrod.e()
        P2 = axelrod.Player()
        P2.history = []
        self.assertEqual(P1.strategy(P2), 'C')

    def test_when_no_defection(self):
        """tests that if the opposing player does not defect initially then strategy defects"""
        P1 = axelrod.e()
        P2 = axelrod.Player()
        P1.history = ['C']
        P2.history = ['C']
        self.assertEqual(P1.strategy(P2), 'D')

    def test_when_greater_than_e(self):
        """tests that if the ratio of Cs to Ds is greater than e then strategy defects"""
        P1 = axelrod.e()
        P2 = axelrod.Player()
        P1.history = ['C','C','C','C']
        P2.history = ['C','C','D','D']
        self.assertEqual(P1.strategy(P2), 'D')

    def test_when_less_than_e(self):
        """tests that if the ratio of Cs to Ds is less than e then strategy co-operates"""
        P1 = axelrod.e()
        P2 = axelrod.Player()
        P1.history = ['C','C','C','C']
        P2.history = ['C','D','D','D']
        self.assertEqual(P1.strategy(P2), 'C')
