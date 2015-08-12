"""Test for the go by majority strategy."""

import axelrod

from .test_player import TestPlayer

C, D = 'C', 'D'


class TestGoByMajority(TestPlayer):

    name = "Go By Majority"
    player = axelrod.GoByMajority
    stochastic = False

    def test_initial_strategy(self):
        """Starts by cooperating """
        self.first_play_test(C)

    def test_strategy(self):
        """
        If opponent cooperates at least as often as they defect then the player cooperates
        """
        self.responses_test([C, D, D, D], [D, D, C, C], [C])
        self.responses_test([C, C, D, D, C], [D, D, C, C, D], [D])

def factory_TestGoByRecentMajority(L):

    class TestGoByRecentMajority(TestPlayer):

        name = "Go By Majority:%i" % L
        player = getattr(axelrod, 'GoByMajority%i' % L)
        stochastic = False

        def test_initial_strategy(self):
            """Starts by cooperating."""
            self.first_play_test(C)

        def test_strategy(self):
            """If opponent cooperates at least as often as they defect then the player cooperates."""
            P1 = self.player()
            P2 = axelrod.Player()
            P1.history = [D] * int(1.5 * L)
            P2.history = [D] * (L - 1) + [C] * (L // 2 + 1)
            self.assertEqual(P1.strategy(P2), C)
            P1.history = [C] * int(1.5 * L)
            P2.history = [C] * (L - 1) + [D] * (L // 2 + 1)
            self.assertEqual(P1.strategy(P2), D)

    return TestGoByRecentMajority

TestGoByMajority5 = factory_TestGoByRecentMajority(5)
TestGoByMajority10 = factory_TestGoByRecentMajority(10)
TestGoByMajority20 = factory_TestGoByRecentMajority(20)
TestGoByMajority40 = factory_TestGoByRecentMajority(40)
