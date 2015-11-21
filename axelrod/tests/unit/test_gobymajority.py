"""Test for the go by majority strategy."""

import axelrod

from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGoByMajority(TestPlayer):

    name = "Soft Go By Majority"
    player = axelrod.GoByMajority

    expected_classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """Starts by cooperating """
        self.first_play_test(C)

    def test_strategy(self):
        """
        If opponent cooperates at least as often as they defect then the player
        cooperates
        """
        self.responses_test([C, D, D, D], [D, D, C, C], [C])
        self.responses_test([C, C, D, D, C], [D, D, C, C, D], [D])

        # Test tie break rule for soft=False
        player = self.player(soft=False)
        opponent = axelrod.Cooperator()
        self.assertEqual('D', player.strategy(opponent))

    def test_repr(self):
        player = self.player(soft=True)
        name = str(player)
        self.assertEqual(name, "Soft Go By Majority")
        player = self.player(soft=False)
        name = str(player)
        self.assertEqual(name, "Hard Go By Majority")


class TestHardGoByMajority(TestGoByMajority):

    name = "Hard Go By Majority"
    player = axelrod.HardGoByMajority

    def test_initial_strategy(self):
        """Starts by defecting"""
        self.first_play_test(D)

    def test_strategy(self):
        """
        If opponent cooperates strictly more often as they defect then the
        player cooperates
        """
        self.responses_test([C, D, D, D], [D, D, C, C], [D])
        self.responses_test([C, C, D, D, C], [D, D, C, C, D], [D])

        # Test tie break rule for soft=True
        player = self.player(soft=True)
        opponent = axelrod.Cooperator()
        self.assertEqual('C', player.strategy(opponent))


def factory_TestGoByRecentMajority(L, soft=True):

    class TestGoByRecentMajority(TestPlayer):

        name = "Soft Go By Majority: %i" % L
        player = getattr(axelrod, 'GoByMajority%i' % L)

        expected_classifier = {
            'stochastic': False,
            'memory_depth': L,
            'makes_use_of': set(),
            'inspects_source': False,
            'manipulates_source': False,
            'manipulates_state': False
        }

        def test_initial_strategy(self):
            """Starts by cooperating."""
            self.first_play_test(C)

        def test_strategy(self):
            """If opponent cooperates at least as often as they defect then the
            player cooperates."""
            P1 = self.player()
            P2 = axelrod.Player()
            P1.history = [D] * int(1.5 * L)
            P2.history = [D] * (L - 1) + [C] * (L // 2 + 1)
            self.assertEqual(P1.strategy(P2), C)
            P1.history = [C] * int(1.5 * L)
            P2.history = [C] * (L - 1) + [D] * (L // 2 + 1)
            self.assertEqual(P1.strategy(P2), D)

    if not soft:  # Overwrite test class

        class TestGoByRecentMajority(TestGoByRecentMajority):
            name = "Hard Go By Majority: %i" % L
            player = getattr(axelrod, 'HardGoByMajority%i' % L)

            def test_initial_strategy(self):
                """Starts by defecting."""
                self.first_play_test(D)

    return TestGoByRecentMajority

TestGoByMajority5 = factory_TestGoByRecentMajority(5)
TestGoByMajority10 = factory_TestGoByRecentMajority(10)
TestGoByMajority20 = factory_TestGoByRecentMajority(20)
TestGoByMajority40 = factory_TestGoByRecentMajority(40)
TestHardGoByMajority5 = factory_TestGoByRecentMajority(5, soft=False)
TestHardGoByMajority10 = factory_TestGoByRecentMajority(10, soft=False)
TestHardGoByMajority20 = factory_TestGoByRecentMajority(20, soft=False)
TestHardGoByMajority40 = factory_TestGoByRecentMajority(40, soft=False)
