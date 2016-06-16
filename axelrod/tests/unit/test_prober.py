"""Tests for prober strategies."""

import axelrod
import random

from .test_player import TestPlayer, test_responses

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestProber(TestPlayer):

    name = "Prober"
    player = axelrod.Prober
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """Starts by playing DCC."""
        self.responses_test([], [], [D, C, C])

    def test_strategy(self):
        # Defects forever if opponent cooperated in moves 2 and 3
        self.responses_test([D, C, C], [C, C, C], [D] * 10)
        self.responses_test([D, C, C], [D, C, C], [D] * 10)

        # Otherwise it plays like TFT
        self.responses_test([D, C, C], [C, D, C], [C])
        self.responses_test([D, C, C], [C, D, D], [D])
        self.responses_test([D, C, C, C], [C, D, C, D], [D])
        self.responses_test([D, C, C, D], [C, D, D], [D])


class TestProber2(TestPlayer):

    name = "Prober 2"
    player = axelrod.Prober2
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """Starts by playing DCC."""
        self.responses_test([], [], [D, C, C])

    def test_strategy(self):
        # Cooperates forever if opponent played D, C in moves 2 and 3
        self.responses_test([D, C, C], [C, D, C], [C] * 10)
        self.responses_test([D, C, C], [D, D, C], [C] * 10)

        # Otherwise it plays like TFT
        self.responses_test([D, C, C], [C, C, C], [C])
        self.responses_test([D, C, C], [C, D, D], [D])
        self.responses_test([D, C, C, D], [C, D, D, D], [D])
        self.responses_test([D, C, C, D], [C, D, D, C], [C])


class TestProber3(TestPlayer):

    name = "Prober 3"
    player = axelrod.Prober3
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """Starts by playing DC."""
        self.responses_test([], [], [D, C])

    def test_strategy(self):
        # Defects forever if opponent played C in move 2
        self.responses_test([D, C], [C, C], [D] * 10)
        self.responses_test([D, C], [D, C], [D] * 10)

        # Otherwise it plays like TFT
        self.responses_test([D, C, C], [C, D], [D])
        self.responses_test([D, C, C], [D, D], [D])
        self.responses_test([D, C, C, D], [C, D, C], [C])
        self.responses_test([D, C, C, D], [D, D, D], [D])
        self.responses_test([D, C, C, D, C], [C, D, C, C], [C])


class TestHardProber(TestPlayer):

    name = "Hard Prober"
    player = axelrod.HardProber
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """Starts by playing DC."""
        self.responses_test([], [], [D, D, C, C])

    def test_strategy(self):
        # Cooperates forever if opponent played C in moves 2 and 3
        self.responses_test([D, D, C, C], [C, C, C, C], [D] * 10)
        self.responses_test([D, D, C, C], [C, C, C, D], [D] * 10)
        self.responses_test([D, D, C, C], [D, C, C, C], [D] * 10)
        self.responses_test([D, D, C, C], [D, C, C, D], [D] * 10)

        # Otherwise it plays like TFT
        self.responses_test([D, D, C, C], [C, C, D, C], [C, C])
        self.responses_test([D, D, C, C], [C, C, D, D], [D])
        self.responses_test([D, D, C, C], [D, D, C, C], [C, C])
        self.responses_test([D, D, C, C], [D, D, C, D], [D])
        self.responses_test([D, D, C, C, D], [C, C, D, D], [D])
        self.responses_test([D, D, C, C, D], [D, D, C, C], [C])


class TestNaiveProber(TestPlayer):

    name = "Naive Prober: 0.1"
    player = axelrod.NaiveProber
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        "Randomly defects and always retaliates like tit for tat."
        self.first_play_test(C)
        # Always retaliate a defection
        self.responses_test([C] * 2, [C, D], [D])

    def test_random_defection(self):
        # Random defection
        player = self.player(0.4)
        opponent = axelrod.Random()
        test_responses(self, player, opponent, [C], [C], [D], random_seed=1)

    def test_reduction_to_TFT(self):
        player = self.player(0)
        opponent = axelrod.Random()
        test_responses(self, player, opponent, [C], [C], [C], random_seed=1)
        test_responses(self, player, opponent, [C], [D], [D])
        test_responses(self, player, opponent, [C, D], [D, C], [C])
        test_responses(self, player, opponent, [C, D], [D, D], [D])


class TestRemorsefulProber(TestPlayer):

    name = "Remorseful Prober: 0.1"
    player = axelrod.RemorsefulProber
    expected_classifier = {
        'memory_depth': 2,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        "Randomly defects (probes) and always retaliates like tit for tat."
        self.first_play_test(C)

        player = self.player(0.4)
        opponent = axelrod.Random()
        player.history = [C, C]
        opponent.history = [C, D]
        self.assertEqual(player.strategy(opponent), D)

    def test_random_defection(self):
        # Random defection
        player = self.player(0.4)
        opponent = axelrod.Random()
        test_responses(self, player, opponent, [C], [C], [D], random_seed=1)

    def test_remorse(self):
        """After probing, if opponent retaliates, will offer a C"""
        player = self.player(0.4)
        opponent = axelrod.Random()

        random.seed(0)
        player.history = [C]
        opponent.history = [C]
        self.assertEqual(player.strategy(opponent), D)  # Random defection
        self.assertEqual(player.probing, True)

        player.history = [C, D]
        opponent.history = [C, D]
        self.assertEqual(player.strategy(opponent), C)  # Remorse
        self.assertEqual(player.probing, False)

        player.history = [C, D, C]
        opponent.history = [C, D, D]
        self.assertEqual(player.strategy(opponent), D)
        self.assertEqual(player.probing, False)

    def test_reduction_to_TFT(self):
        player = self.player(0)
        opponent = axelrod.Random()
        test_responses(self, player, opponent, [C], [C], [C], random_seed=1,
                       attrs={'probing': False})
        test_responses(self, player, opponent, [C], [D], [D],
                       attrs={'probing': False})
        test_responses(self, player, opponent, [C, D], [D, C], [C],
                       attrs={'probing': False})
        test_responses(self, player, opponent, [C, D], [D, D], [D],
                       attrs={'probing': False})

    def test_reset_probing(self):
        player = self.player(0.4)
        player.probing = True
        player.reset()
        self.assertFalse(player.probing)
