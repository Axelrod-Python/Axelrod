"""Test for the memoryone strategies."""

import random

import axelrod

from test_player import TestPlayer

C, D = 'C', 'D'

class TestWinStayLoseShift(TestPlayer):

    name = "Win-Stay Lose-Shift"
    player = axelrod.WinStayLoseShift

    def test_strategy(self):
        """Starts by cooperating"""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Check that switches if does not get best payoff."""
        self.markov_test([C,D,D,C])

class TestGTFT(TestPlayer):

    name = "Generous Tit-For-Tat"
    player = axelrod.GTFT
    stochastic = True

    def test_strategy(self):
        self.first_play_test(C)

class TestStochasticCooperator(TestPlayer):

    name = "Stochastic Cooperator"
    player = axelrod.StochasticCooperator
    stochastic = True

    def test_strategy(self):
        self.first_play_test(C)

    def test_four_vector(self):
        P1 = self.player()
        expected_dictionary = {(C, C): 0.935, (C, D): 0.229, (D,C): 0.266, (D, D): 0.42}
        for key in sorted(expected_dictionary.keys()):
            self.assertAlmostEqual(P1._four_vector[key],
                    expected_dictionary[key])

    def test_effect_of_strategy(self):
        # With probability 0.065 will defect
        self.responses_test([[[C],[C],[D,C,C,C]]], random_seed=15)
        # With probability 0.266 will cooperate
        self.responses_test([[[C],[D],[C,D,D,D]]], random_seed=1)
        # With probability 0.42 will cooperate
        self.responses_test([[[D],[C],[C,D,D,D]]], random_seed=3)
        # With probability 0.229 will cooperate
        self.responses_test([[[D],[D],[C,D,D,D]]], random_seed=13)

class TestStochasticWSLS(TestPlayer):

    name = "Stochastic WSLS"
    player = axelrod.StochasticWSLS
    stochastic = True

    def test_strategy(self):
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        # With probability 0.05 will defect
        self.responses_test([[[C],[C],[D,C,C,C]]], random_seed=2)
        # With probability 0.05 will cooperate
        self.responses_test([[[C],[D],[C,D,D,D]]], random_seed=31)
        # With probability 0.05 will cooperate
        self.responses_test([[[D],[C],[C,D,D,D]]], random_seed=31)
        # With probability 0.05 will defect
        self.responses_test([[[D],[D],[D,C,C,C]]], random_seed=2)

class TestZDExtort2(TestPlayer):

    name = "ZD-Extort-2"
    player = axelrod.ZDExtort2
    stochastic = True

    def test_four_vector(self):
        P1 = self.player()
        expected_dictionary = {('C', 'D'): 0.5, ('D', 'C'): 1./3, ('D', 'D'): 0., ('C', 'C'): 8./9}
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
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
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
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['D']
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.strategy(P2), 'D')

class TestZDGTFT2(TestPlayer):

    name = "ZD-GTFT-2"
    player = axelrod.ZDGTFT2
    stochastic = True

    def test_four_vector(self):
        P1 = self.player()
        expected_dictionary = {('C', 'D'): 1./8, ('D', 'C'): 1., ('D', 'D'): 0.25, ('C', 'C'): 1.}
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
        self.assertEqual(P1.strategy(P2), 'D')
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
