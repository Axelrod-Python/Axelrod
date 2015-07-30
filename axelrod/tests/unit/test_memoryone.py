"""Test for the memoryone strategies."""
import axelrod
from axelrod import Game
from test_player import TestPlayer, test_four_vector

C, D = 'C', 'D'


class TestWinStayLoseShift(TestPlayer):

    name = "Win-Stay Lose-Shift"
    player = axelrod.WinStayLoseShift

    def test_strategy(self):
        """Starts by cooperating"""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Check that switches if does not get best payoff."""
        self.markov_test([C, D, D, C])


class TestGTFT(TestPlayer):

    name = "Generous Tit-For-Tat"
    player = axelrod.GTFT
    stochastic = True

    def test_strategy(self):
        self.first_play_test(C)

    def test_four_vector(self):
        player = self.player()
        (R, P, S, T) = Game().RPST()
        p = min(1 - float(T - R) / (R - S), float(R - P) / (T - P))
        expected_dictionary = {(C, C): 1., (C, D): p, (D, C): 1., (D, D): p}
        test_four_vector(self, expected_dictionary)


class TestStochasticCooperator(TestPlayer):

    name = "Stochastic Cooperator"
    player = axelrod.StochasticCooperator
    stochastic = True

    def test_four_vector(self):
        expected_dictionary = {(C, C): 0.935, (C, D): 0.229, (D, C): 0.266, (D, D): 0.42}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        # With probability 0.065 will defect
        self.responses_test([C], [C], [D, C, C, C], random_seed=15)
        # With probability 0.266 will cooperate
        self.responses_test([C], [D], [C, D, D, D], random_seed=1)
        # With probability 0.42 will cooperate
        self.responses_test([D], [C], [C, D, D, D], random_seed=3)
        # With probability 0.229 will cooperate
        self.responses_test([D], [D], [C, D, D, D], random_seed=13)


class TestStochasticWSLS(TestPlayer):

    name = "Stochastic WSLS"
    player = axelrod.StochasticWSLS
    stochastic = True

    def test_strategy(self):
        self.first_play_test(C)

    def test_four_vector(self):
        player = self.player()
        ep = player.ep
        expected_dictionary = {(C, C): 1.-ep, (C, D): ep, (D, C): ep, (D, D): 1.-ep}
        test_four_vector(self, expected_dictionary)

    def test_effect_of_strategy(self):
        # With probability 0.05 will defect
        self.responses_test([C], [C], [D, C, C, C], random_seed=2)
        # With probability 0.05 will cooperate
        self.responses_test([C], [D], [C, D,  D, D], random_seed=31)
        # With probability 0.05 will cooperate
        self.responses_test([D], [C], [C, D, D, D], random_seed=31)
        # With probability 0.05 will defect
        self.responses_test([D], [D], [D, C, C, C], random_seed=2)


class TestZDExtort2(TestPlayer):

    name = "ZD-Extort-2"
    player = axelrod.ZDExtort2
    stochastic = True

    def test_four_vector(self):
        expected_dictionary = {(C, C): 8./9, (C, D): 0.5, (D, C): 1./3, (D, D): 0.}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        self.responses_test([C], [C], [D, D, C, C], random_seed=2)
        self.responses_test([C], [D], [D, D, D, C])
        self.responses_test([D], [C], [D, D, D, C])
        self.responses_test([D], [D], [D, D, D, D])


class TestZDGTFT2(TestPlayer):

    name = "ZD-GTFT-2"
    player = axelrod.ZDGTFT2
    stochastic = True

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1., (C, D): 1./8, (D, C): 1., (D, D): 0.25}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        self.responses_test([C], [C], [C, C, C, C], random_seed=2)
        self.responses_test([C], [D], [D, D, D, D])
        self.responses_test([D], [C], [C, C, C, C])
        self.responses_test([D], [D], [D, D, D, D])


class TestGrofman(TestPlayer):

    name = "Grofman"
    player = axelrod.Grofman
    stochastic = True

    def test_four_vector(self):
        p = float(2) / 7
        expected_dictionary = {(C, C): p, (C, D): p, (D, C): p, (D, D): p}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.responses_test([C], [C], [D, D, C], random_seed=2)
        self.responses_test([C], [D], [C, D, D])


class TestJoss(TestPlayer):

    name = "Joss"
    player = axelrod.Joss
    stochastic = True

    def test_four_vector(self):
        expected_dictionary = {(C, C): 0.9, (C, D): 0, (D, C): 0.9, (D, D): 0}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.responses_test([C], [C], [D, D, C, C], random_seed=2)
        self.responses_test([C], [D], [D, D, D, D])


class TestSoftJoss(TestPlayer):

    name = "Soft Joss"
    player = axelrod.SoftJoss
    stochastic = True

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1, (C, D): 0.1, (D, C): 1., (D, D): 0.1}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.responses_test([C], [C], [C, C, C, C], random_seed=2)
        self.responses_test([C], [D], [D, D, D, D], random_seed=5)
