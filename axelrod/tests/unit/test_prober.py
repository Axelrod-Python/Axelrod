"""Tests for Prober strategies."""

import axelrod
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

    def test_strategy(self):
        # Starts by playing CD.
        self.responses_test([C, D])
        # Defects forever unless opponent matched first two moves
        self.responses_test([D] * 10, [C, D], [C, C])
        self.responses_test([D] * 10, [C, D], [D, C])
        self.responses_test([D] * 10, [C, D], [D, D])

        self.responses_test([C] * 10, [C, D], [C, D])
        self.responses_test([D] * 10, [C, D, D], [C, D, D])


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

    def test_strategy(self):
        # Starts by playing DCC.
        self.responses_test([D, C, C])
        # Defects forever if opponent cooperated in moves 2 and 3
        self.responses_test([D] * 10, [D, C, C], [C, C, C])
        self.responses_test([D] * 10, [D, C, C], [D, C, C])
        # Otherwise it plays like TFT
        self.responses_test([C], [D, C, C], [C, D, C])
        self.responses_test([D], [D, C, C], [C, D, D])
        self.responses_test([D], [D, C, C, C], [C, D, C, D])
        self.responses_test([D], [D, C, C, D], [C, D, D])


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

    def test_strategy(self):
        # Starts by playing DCC.
        self.responses_test([D, C, C])
        # Cooperates forever if opponent played D, C in moves 2 and 3
        self.responses_test([C] * 10, [D, C, C], [C, D, C])
        self.responses_test([C] * 10, [D, C, C], [D, D, C])
        # Otherwise it plays like TFT
        self.responses_test([C], [D, C, C], [C, C, C])
        self.responses_test([D], [D, C, C], [C, D, D])
        self.responses_test([D], [D, C, C, D], [C, D, D, D])
        self.responses_test([C], [D, C, C, D], [C, D, D, C])


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

    def test_strategy(self):
        # Starts by playing DC.
        self.responses_test([D, C])
        # Defects forever if opponent played C in move 2
        self.responses_test([D] * 10, [D, C], [C, C])
        self.responses_test([D] * 10, [D, C], [D, C])
        # Otherwise it plays like TFT
        self.responses_test([D], [D, C, C], [C, D])
        self.responses_test([D], [D, C, C], [D, D])
        self.responses_test([C], [D, C, C, D], [C, D, C])
        self.responses_test([D], [D, C, C, D], [D, D, D])
        self.responses_test([C], [D, C, C, D, C], [C, D, C, C])


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

    def test_strategy(self):
        # Starts by playing CCDCDDDCCDCDCCDCDDCD.
        self.responses_test(self.initial_sequence)

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
            self.responses_test(responses, history1, history2, attrs=attrs)

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
            self.responses_test(responses, history1, history2, attrs=attrs)

            # and plays like TFT afterwards
            history1 += responses
            history2 += responses
            self.responses_test([C], history1, history2, attrs=attrs)

            history1 += [C]
            history2 += [D]
            self.responses_test([D], history1, history2, attrs=attrs)

            history1 += [D]
            history2 += [C]
            self.responses_test([C], history1, history2, attrs=attrs)

            history1 += [C]
            history2 += [D]
            self.responses_test([D], history1, history2, attrs=attrs)


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

    def test_strategy(self):
        # Starts by playing DC.
        self.responses_test([D, D, C, C])
        # Cooperates forever if opponent played C in moves 2 and 3
        self.responses_test([D] * 10, [D, D, C, C], [C, C, C, C])
        self.responses_test([D] * 10, [D, D, C, C], [C, C, C, D])
        self.responses_test([D] * 10, [D, D, C, C], [D, C, C, C])
        self.responses_test([D] * 10, [D, D, C, C], [D, C, C, D])
        # Otherwise it plays like TFT
        self.responses_test([C, C], [D, D, C, C], [C, C, D, C])
        self.responses_test([D], [D, D, C, C], [C, C, D, D])
        self.responses_test([C, C], [D, D, C, C], [D, D, C, C])
        self.responses_test([D], [D, D, C, C], [D, D, C, D])
        self.responses_test([D], [D, D, C, C, D], [C, C, D, D])
        self.responses_test([C], [D, D, C, C, D], [D, D, C, C])


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
        # Randomly defects and always retaliates like tit for tat.
        self.first_play_test(C)
        # Always retaliate a defection
        self.responses_test([D], [C] * 2, [C, D])

    def test_random_defection(self):
        # Random defection
        player = self.player(0.4)
        opponent = axelrod.Random()
        test_responses(self, player, opponent, [D], [C], [C], seed=1)

    def test_reduction_to_TFT(self):
        player = self.player(0)
        opponent = axelrod.Random()
        test_responses(self, player, opponent, [C], [C], [C], seed=1)
        test_responses(self, player, opponent, [D], [C], [D])
        test_responses(self, player, opponent, [C], [C, D], [D, C])
        test_responses(self, player, opponent, [D], [C, D], [D, D])


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
        # Randomly defects (probes) and always retaliates like tit for tat.
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

        test_responses(self, player, opponent, [C], [C], [C], seed=3,
                       attrs={'probing': False})

        test_responses(self, player, opponent, [D], [C], [C], seed=1,
                       attrs={'probing': True})

        test_responses(self, player, opponent, [D], [C, D], [C, D],
                       attrs={'probing': False})

        test_responses(self, player, opponent, [D], [C, D, C], [C, D, D],
                       attrs={'probing': False})

    def test_reduction_to_TFT(self):
        player = self.player(0)
        opponent = axelrod.Random()
        test_responses(self, player, opponent, [C], [C], [C], seed=1,
                       attrs={'probing': False})
        test_responses(self, player, opponent, [D], [C], [D],
                       attrs={'probing': False})
        test_responses(self, player, opponent, [C], [C, D], [D, C],
                       attrs={'probing': False})
        test_responses(self, player, opponent, [D], [C, D], [D, D],
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
        test_responses(self, player, opponent, [D], [C], [C], seed=1)
