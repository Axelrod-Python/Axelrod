"""Test for the inverse strategy."""

import random

import axelrod

from test_player import TestPlayer

C, D = 'C', 'D'


class TestFeld(TestPlayer):

    name = "Feld"
    player = axelrod.Feld
    stochastic = True

    def test_strategy(self):
        self.first_play_test(C)
        # Test retaliate
        self.responses_test([C], [D], [D])
        self.responses_test([D], [D], [D])
        # Test cooperation probabilities
        p1 = self.player(start_coop_prob=1.0, end_coop_prob=0.8,
                         rounds_of_decay=100)
        self.assertEqual(1.0, p1._cooperation_probability())
        p1.history = [C] * 50
        self.assertEqual(0.9, p1._cooperation_probability())
        p1.history = [C] * 100
        self.assertEqual(0.8, p1._cooperation_probability())
        # Test cooperation probabilities, second set of params
        p1 = self.player(start_coop_prob=1.0, end_coop_prob=0.5,
                         rounds_of_decay=200)
        self.assertEqual(1.0, p1._cooperation_probability())
        p1.history = [C] * 100
        self.assertEqual(0.75, p1._cooperation_probability())
        p1.history = [C] * 200
        self.assertEqual(0.5, p1._cooperation_probability())
        # Test beyond 200 rounds
        history_1 = [C] * 200
        history_2 = [C] * 200
        self.responses_test(history_1, history_2, [C, C, D, D], random_seed=1)
        self.responses_test(history_1, history_2, [D, D, D, D], random_seed=50)


class TestShubik(TestPlayer):

    name = 'Shubik'
    player = axelrod.Shubik

    def test_strategy(self):
        # Starts by Cooperating
        self.first_play_test(C)
        # Looks like Tit-For-Tat at first
        self.markov_test([C, D, C, D])

    def test_affect_of_strategy(self):
        """Plays a modified TFT."""
        self.responses_test([C, C, C], [C, C, C], [C, C, C])
        # Make sure that the retaliations are increasing
        # Retaliate once and forgive
        self.responses_test([C], [D], [D])
        self.responses_test([C, D], [D, C], [C])
        self.responses_test([C, D, C], [D, C, C], [C])
        # Retaliate twice and forgive
        self.responses_test([C, D, C], [D, C, D], [D, D])
        self.responses_test([C, D, C, D, D], [D, C, D, C, C], [C])
        # Opponent defection during retaliation doesn't increase retaliation period
        self.responses_test([C, D, C, D, D], [D, C, D, D, C], [C])
        # Retaliate thrice and forgive
        self.responses_test([C, D, C, D, D, C], [D, C, D, C, C, D], [D, D, D])
        history_1 = [C, D, C, D, D, C, D, D, D]
        history_2 = [D, C, D, C, C, D, C, C, C]
        self.responses_test(history_1, history_2, [C])


class TestTullock(TestPlayer):

    name = "Tullock"
    player = axelrod.Tullock
    stochastic = True

    def test_strategy(self):
        """Cooperates for first ten rounds"""
        self.first_play_test(C)
        for i in range(10):
            history_1 = [C] * i
            history_2 = [C] * i
            self.responses_test(history_1, history_2, [C])
        # Now cooperate 10% less than opponent
        history_1 = [C] * 11
        history_2 = [D] * 11
        self.responses_test(history_1, history_2, [D], random_seed=10)
        history_1 = [C] * 11
        history_2 = [D] * 10 + [C]
        self.responses_test(history_1, history_2, [D], random_seed=10)
        # Test beyond 10 rounds
        history_1 = [C] * 11
        history_2 = [D] * 5 + [C] * 6
        self.responses_test(history_1, history_2, [D, D, D, D], random_seed=20)
        history_1 = [C] * 11
        history_2 = [C] * 9 + [D] *2
        self.responses_test(history_1, history_2, [C, D, D, C], random_seed=25)


class TestChampion(TestPlayer):
    name = "Champion"
    player = axelrod.Champion
    stochastic = True

    def test_strategy(self):
        # Initially cooperates
        self.first_play_test(C)
        # Cooperates for num_rounds / 20 (10 by default)
        random.seed(3)
        random_sample = []
        for i in range(10):
            random_sample.append(random.choice([C,D]))
            self.responses_test([C] * i, random_sample, [C])

        # Mirror opponent in the next stage (15 rounds by default)
        my_responses = [C] * 10
        for i in range(15):
            self.responses_test(my_responses, random_sample,
                                [random_sample[-1]])
            my_responses.append(random_sample[-1])
            random_sample.append(random.choice([C,D]))

        # Cooperate unless the opponent defected, has defected at least 40% of
        # the time, and with a random choice
        for i in range(5):
            my_responses.append(C)
            random_sample.append(C)
            self.responses_test(my_responses, random_sample, [C])

        self.responses_test(my_responses + [C], random_sample + [D], [C],
                            random_seed=50)
        self.responses_test(my_responses + [C], random_sample + [D], [C],
                            random_seed=30)
        self.responses_test(my_responses + [C] * 40, random_sample + [D] * 40,
                            [D], random_seed=40)


class TestEatherly(TestPlayer):

    name = "Eatherley"
    player = axelrod.Eatherley
    stochastic = True

    def test_strategy(self):
        # Initially cooperates
        self.first_play_test(C)
        # Test cooperate after opponent cooperates
        self.responses_test([C], [C], [C])
        self.responses_test([C, C], [C, C], [C])
        self.responses_test([D, C], [D, C], [C])
        self.responses_test([D, C, C], [D, C, C], [C])
        # Test defection after opponent defection
        self.responses_test([D], [D], [D])
        self.responses_test([D, D], [D, D], [D])
        self.responses_test([D, C, C, D], [D, C, C, D], [D, C], random_seed=10)


class TestTester(TestPlayer):

    name = "Tester"
    player = axelrod.Tester

    def test_strategy(self):
        """Starts by defecting."""
        self.first_play_test(D)

    def test_effect_of_strategy(self):

        # Test Alternating CD
        self.responses_test([D], [C], [C])
        self.responses_test([D, C], [C, C], [C])
        self.responses_test([D, C, C], [C, C, C], [D])
        self.responses_test([D, C, C, D], [C, C, C, C], [C])
        self.responses_test([D, C, C, D, C], [C, C, C, C, C], [D])

        # Test cooperation after opponent defection
        self.responses_test([D, C], [D, C], [C])

        # Test TFT after defection
        self.responses_test([D, C, C], [D, C, C], [C])
        self.responses_test([D, C, C, C], [D, C, C, C], [C])
        self.responses_test([D, C, D], [D, D, D], [D])
        self.responses_test([D, C, C], [D, C, D], [D])
