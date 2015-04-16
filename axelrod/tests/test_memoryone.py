"""Test for the memoryone strategies."""

import random

import axelrod

from test_player import TestPlayer


class TestWinStayLostShift(TestPlayer):

    name = "Win-Stay Lose-Shift"
    player = axelrod.WinStayLoseShift

    def test_strategy(self):
        """Starts by cooperating"""
        P1 = self.player()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """Check that switches if does not get best payoff."""
        P1 = self.player()
        P2 = axelrod.Player()
        P1.history = ['C']
        P2.history = ['C']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C']
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['D']
        P2.history = ['C']
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = ['D']
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'C')

class TestGTFT(TestPlayer):

    name = "Generous Tit-For-Tat"
    player = axelrod.GTFT
    stochastic = True

    def test_strategy(self):
        P1 = self.player()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

        P1.history = ['C']
        P2.history = ['C']
        random.seed(2)
        # With probability .05 will defect
        self.assertEqual(P1.strategy(P2), 'D')
        # But otherwise will cooperate
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')

        P1.history = ['C']
        P2.history = ['D']
        random.seed(31)
        # With probability .05 will cooperate
        self.assertEqual(P1.strategy(P2), 'C')
        # But otherwise will defect
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')

        P1.history = ['D']
        P2.history = ['C']
        random.seed(2)
        # With probability .05 will defect
        self.assertEqual(P1.strategy(P2), 'D')
        # But otherwise will cooperate
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')

        P1.history = ['D']
        P2.history = ['D']
        random.seed(31)
        # With probability .05 will cooperate
        self.assertEqual(P1.strategy(P2), 'C')
        # But otherwise will defect
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')


class TestStochasticCooperator(TestPlayer):

    name = "Stochastic Cooperator"
    player = axelrod.StochasticCooperator
    stochastic = True

    def test_strategy(self):
        P1 = self.player()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

        P1.history = ['C']
        P2.history = ['C']
        random.seed(15)
        # With probability .065 will defect
        self.assertEqual(P1.strategy(P2), 'D')
        # But otherwise will cooperate
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')

        P1.history = ['C']
        P2.history = ['D']
        random.seed(1)
        # With probability .229 will cooperate
        self.assertEqual(P1.strategy(P2), 'C')
        # But otherwise will defect
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')

        P1.history = ['D']
        P2.history = ['C']
        random.seed(3)
        # With probability .266 will cooperate
        self.assertEqual(P1.strategy(P2), 'C')
        # But otherwise will defect
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')

        P1.history = ['D']
        P2.history = ['D']
        random.seed(13)
        # With probability .42 will cooperate
        self.assertEqual(P1.strategy(P2), 'C')
        # But otherwise will defect
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')

class TestStochasticWSLS(TestPlayer):

    name = "Stochastic WSLS"
    player = axelrod.StochasticWSLS
    stochastic = True

    def test_strategy(self):
        P1 = self.player()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

        P1.history = ['C']
        P2.history = ['C']
        random.seed(2)
        # With probability .05 will defect
        self.assertEqual(P1.strategy(P2), 'D')
        # But otherwise will cooperate
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')

        P1.history = ['C']
        P2.history = ['D']
        random.seed(31)
        # With probability .05 will cooperate
        self.assertEqual(P1.strategy(P2), 'C')
        # But otherwise will defect
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')

        P1.history = ['D']
        P2.history = ['C']
        random.seed(31)
        # With probability .05 will cooperate
        self.assertEqual(P1.strategy(P2), 'C')
        # But otherwise will defect
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')

        P1.history = ['D']
        P2.history = ['D']
        random.seed(2)
        # With probability .05 will defect
        self.assertEqual(P1.strategy(P2), 'D')
        # But otherwise will defect
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')

class TestZDChi(TestPlayer):

    name = "ZDChi"
    player = axelrod.ZDChi
    stochastic = True

    def test_four_vector(self):
        P1 = self.player()
        expected_dictionary = {('C', 'D'): 0.5, ('D', 'C'): 0.75, ('D', 'D'): 0.0, ('C', 'C'): 1.1666666666666667}
        for key in sorted(expected_dictionary.keys()):
            self.assertAlmostEqual(P1._four_vector[key],
                    expected_dictionary[key])

    def test_strategy(self):
        # Testing the expected value is difficult here so these just ensure that
        # future changes that break these tests will be examined carefully.
        P1 = self.player()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

        P1.history = ['C']
        P2.history = ['C']
        random.seed(2)
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C']
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['D']
        P2.history = ['C']
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['D']
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
