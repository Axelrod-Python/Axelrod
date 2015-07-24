"""Test for the random strategy."""

import random

import axelrod

from test_player import TestPlayer

C, D = 'C', 'D'


class TestRandom(TestPlayer):

    name = "Random"
    player = axelrod.Random
    stochastic = True

    def test_strategy(self):
        """Test that strategy is randomly picked (not affected by history)."""
        self.first_play_test(C, random_seed=1)
        self.first_play_test(D, random_seed=2)
        self.responses_test([C, D, C], [C, C, D], [C], random_seed=1)


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
