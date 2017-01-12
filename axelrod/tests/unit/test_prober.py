"""Tests for prober strategies."""

import axelrod
import random

from .test_player import TestPlayer, test_responses

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestCollectiveStrategy(TestPlayer):

    name = "CollectiveStrategy"
    player = axelrod.CollectiveStrategy
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """Starts by playing CD."""
        self.responses_test([], [], [C, D])

    def test_strategy(self):
        # Defects forever unless opponent matched first two moves
        self.responses_test([C, D], [C, C], [D] * 10)
        self.responses_test([C, D], [D, C], [D] * 10)
        self.responses_test([C, D], [D, D], [D] * 10)

        self.responses_test([C, D], [C, D], [C] * 10)
        self.responses_test([C, D, D], [C, D, D], [D] * 10)


class TestProber(TestPlayer):

    name = "Prober"
    player = axelrod.Prober
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
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
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
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
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
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


class TestProber4(TestPlayer):

    name = "Prober 4"
    player = axelrod.Prober4
    expected_classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }
    initial_sequence = [
        C, C, D, C, D, D, D, C, C, D, C, D, C, C, D, C, D, D, C, D
    ]

    def test_initial_strategy(self):
        """Starts by playing CCDCDDDCCDCDCCDCDDCD."""
        self.responses_test([], [], self.initial_sequence)

    def test_strategy(self):
        # After playing the initial sequence defects forever
        # if the absolute difference in the number of retaliating
        # and provocative defections of the opponent is smaller or equal to 2

        provocative_histories = [
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, D, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, D, C, D, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, D, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, D, C, D, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D],
        ]

        history1 = self.initial_sequence
        responses = [D] * 10
        attrs = {'turned_defector': True}
        for history2 in provocative_histories:
            self.responses_test(history1, history2, responses, attrs=attrs)

        # Otherwise cooperates for 5 rounds
        unprovocative_histories = [
            [C, C, D, C, D, D, D, C, C, D, C, D, C, C, D, C, D, D, C, D],
            [D, D, C, D, C, C, C, D, D, C, D, C, D, D, C, D, C, C, D, C],
            [C, C, D, C, D, D, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, D, C, D, D, C, C, D, C, C, C, C, C, C, D, D, D, C, C],
            [C, C, C, C, D, D, C, C, D, C, C, D, D, C, D, C, D, C, C, C],
        ]

        responses = [C] * 5
        attrs = {'turned_defector': False}
        for history2 in unprovocative_histories:
            self.responses_test(history1, history2, responses, attrs=attrs)

        # and plays like TFT afterwards
            history1 += responses
            history2 += responses
            self.responses_test(history1, history2, [C], attrs=attrs)

            history1 += [C]
            history2 += [D]
            self.responses_test(history1, history2, [D], attrs=attrs)

            history1 += [D]
            history2 += [C]
            self.responses_test(history1, history2, [C], attrs=attrs)

            history1 += [C]
            history2 += [D]
            self.responses_test(history1, history2, [D], attrs=attrs)


class TestHardProber(TestPlayer):

    name = "Hard Prober"
    player = axelrod.HardProber
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
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
        'long_run_time': False,
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
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Randomly defects (probes) and always retaliates like tit for tat."""
        self.first_play_test(C)

        player = self.player(0.4)
        opponent = axelrod.Random()
        player.history = [C, C]
        opponent.history = [C, D]
        self.assertEqual(player.strategy(opponent), D)

    def test_remorse(self):
        """After probing, if opponent retaliates, will offer a C."""
        player = self.player(0.4)
        opponent = axelrod.Cooperator()

        test_responses(self, player, opponent, [C], [C], [C],
                       random_seed=3, attrs={'probing': False})

        test_responses(self, player, opponent, [C], [C], [D],
                       random_seed=1, attrs={'probing': True})

        test_responses(self, player, opponent, [C, D], [C, D], [D],
                       attrs={'probing': False})

        test_responses(self, player, opponent, [C, D, C], [C, D, D], [D],
                       attrs={'probing': False})

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

    def test_random_defection(self):
        # Random defection
        player = self.player(0.4)
        opponent = axelrod.Random()
        test_responses(self, player, opponent, [C], [C], [D], random_seed=1)
