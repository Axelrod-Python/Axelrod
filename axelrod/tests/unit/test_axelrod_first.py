"""Tests for the First Axelrod strategies."""

import random

import axelrod
from .test_player import TestPlayer, test_four_vector

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestDavis(TestPlayer):

    name = "Davis"
    player = axelrod.Davis
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
        """
        Starts by cooperating
        """
        self.first_play_test(C)

    def test_strategy(self):
        # Cooperates for the first ten rounds
        player_history = []
        opponent_history = []
        for i in range(9):
            opponent_history.append(random.choice([C, D]))
            player_history.append(C)
            self.responses_test([C], player_history, opponent_history)

        # If opponent defects at any point then the player will defect forever
        # (after 10 rounds)
        self.responses_test([C], [C, D, D, D], [C, C, C, C])
        self.responses_test([C], [C, C, D, D, D], [C, D, C, C, C])
        self.responses_test([D], [C] * 10 + [C, C, D, D, D],
                            [C] * 10 + [C, D, C, C, C])


class TestRevisedDowning(TestPlayer):

    name = "Revised Downing"
    player = axelrod.RevisedDowning
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
        self.first_play_test(C)
        self.responses_test([C], [C], [C])
        self.responses_test([C], [C], [D])
        self.responses_test([C], [C, C], [C, C])
        self.responses_test([D], [C, C], [C, D])
        self.responses_test([C], [C, C], [D, C])
        self.responses_test([D], [C, C], [D, D])
        self.responses_test([D], [C, C, D], [C, D, C])
        self.responses_test([C], [C, C, C], [D, C, C])
        self.responses_test([D], [C, C, D], [C, D, D])
        self.responses_test([C], [C, C, C], [D, C, D])
        self.responses_test([D], [C, C, D, D], [C, D, D, D])
        self.responses_test([C], [C, C, C, C], [D, C, D, C])
        self.responses_test([C], [C, D, C, C, D, D], [C, C, C, C, D, D])

    def test_not_revised(self):
        # Test not revised
        p1 = self.player(revised=False)
        p2 = axelrod.Cooperator()
        p1.play(p2)
        p1.play(p2)
        self.assertEqual(p1.history, [D, D])


class TestFeld(TestPlayer):

    name = "Feld"
    player = axelrod.Feld
    expected_classifier = {
        'memory_depth': 200,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        # Test retaliate
        self.responses_test([D], [C], [D])
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
        player_history = [C] * 200
        opponent_history = [C] * 200
        self.responses_test([C, C, D, D], player_history, opponent_history,
                            seed=1)
        self.responses_test([D, D, D, D], player_history, opponent_history,
                            seed=50)


class TestGrofman(TestPlayer):

    name = "Grofman"
    player = axelrod.Grofman
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.responses_test([C, C, C])
        self.responses_test([D], [C, C], [C, D])
        self.responses_test([C], [C] * 6, [C] * 6)
        self.responses_test([D], [C] * 6, [D] * 6)
        self.responses_test([C], [C] * 7, [C] * 7)
        self.responses_test([C], [C] * 7, [D] * 7, seed=1)
        self.responses_test([D], [C] * 7, [D] * 7, seed=2)


class TestJoss(TestPlayer):

    name = "Joss: 0.9"
    player = axelrod.Joss
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 0.9, (C, D): 0, (D, C): 0.9, (D, D): 0}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        self.responses_test([D], [C], [C], seed=2)
        self.responses_test([D], [C], [D], seed=4)


class TestNydegger(TestPlayer):

    name = "Nydegger"
    player = axelrod.Nydegger
    expected_classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_score_history(self):
        """Tests many (but not all) possible combinations."""
        player = self.player()
        score_map = player.score_map
        score = player.score_history([C, C, C], [C, C, C], score_map)
        self.assertEqual(score, 0)
        score = player.score_history([D, C, C], [C, C, C], score_map)
        self.assertEqual(score, 1)
        score = player.score_history([C, C, C], [D, C, C], score_map)
        self.assertEqual(score, 2)
        score = player.score_history([D, D, C], [D, C, C], score_map)
        self.assertEqual(score, 7)
        score = player.score_history([C, D, C], [C, D, C], score_map)
        self.assertEqual(score, 12)
        score = player.score_history([D, C, D], [C, C, C], score_map)
        self.assertEqual(score, 17)
        score = player.score_history([D, D, D], [D, D, D], score_map)
        self.assertEqual(score, 63)

    def test_strategy(self):
        # Test TFT-type initial play
        self.first_play_test(C)
        self.responses_test([C, C], [C], [C])
        self.responses_test([D], [C], [D])
        self.responses_test([D], [C, D], [D, C])
        self.responses_test([D], [C, D], [D, D])

        # Test trailing post-round 3 play
        for i in range(4, 9):
            self.responses_test([C], [C] * i, [C] * i)
            self.responses_test([C], [D] * i, [D] * i)
            self.responses_test([C], [C] * i + [C, D, C], [C] * i + [C, D, C])
            self.responses_test([D], [C] * i + [D, C, D], [C] * i + [C, C, C])
            self.responses_test([D], [C] * i + [D, C, C], [C] * i + [C, C, C])
            self.responses_test([C], [C] * i + [C, C, C], [C] * i + [D, C, C])


class TestShubik(TestPlayer):

    name = 'Shubik'
    player = axelrod.Shubik
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
        # Starts by Cooperating
        self.first_play_test(C)
        # Looks like Tit-For-Tat at first
        self.second_play_test(C, D, C, D)

        # Plays a modified TFT.
        self.responses_test([C, C, C], [C, C, C], [C, C, C])
        # Make sure that the retaliations are increasing
        # Retaliate once and forgive
        self.responses_test([D], [C], [D])
        self.responses_test([C], [C, D], [D, C])
        self.responses_test([C], [C, D, C], [D, C, C])
        # Retaliate twice and forgive
        self.responses_test([D, D], [C, D, C], [D, C, D])
        self.responses_test([C], [C, D, C, D, D], [D, C, D, C, C])
        # Opponent defection during retaliation doesn't increase retaliation
        # period.
        self.responses_test([C], [C, D, C, D, D], [D, C, D, D, C])
        # Retaliate thrice and forgive
        self.responses_test([D, D, D], [C, D, C, D, D, C], [D, C, D, C, C, D])
        player_history = [C, D, C, D, D, C, D, D, D]
        opponent_history = [D, C, D, C, C, D, C, C, C]
        self.responses_test([C], player_history, opponent_history)


class TestTullock(TestPlayer):

    name = "Tullock"
    player = axelrod.Tullock
    expected_classifier = {
        'memory_depth': 11,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Cooperates for first ten rounds"""
        self.first_play_test(C)
        for i in range(10):
            player_history = [C] * i
            opponent_history = [C] * i
            self.responses_test([C], player_history, opponent_history)
        # Now cooperate 10% less than opponent
        player_history = [C] * 11
        opponent_history = [D] * 11
        self.responses_test([D], player_history, opponent_history, seed=10)
        player_history = [C] * 11
        opponent_history = [D] * 10 + [C]
        self.responses_test([D], player_history, opponent_history, seed=10)
        # Test beyond 10 rounds
        player_history = [C] * 11
        opponent_history = [D] * 5 + [C] * 6
        self.responses_test([D, D, D, D], player_history, opponent_history,
                            seed=20)
        player_history = [C] * 11
        opponent_history = [C] * 9 + [D] * 2
        self.responses_test([C, D, D, C], player_history, opponent_history,
                            seed=25)


class TestUnnamedStrategy(TestPlayer):

    name = "Unnamed Strategy"
    player = axelrod.UnnamedStrategy
    expected_classifier = {
        'memory_depth': 0,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.responses_test([C, C, D, C, C, D], seed=10)
