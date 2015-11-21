"""Tests for grudger strategies."""

import random

import axelrod

from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGrudger(TestPlayer):

    name = "Grudger"
    player = axelrod.Grudger
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
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
        """
        If opponent defects at any point then the player will defect forever
        """
        self.responses_test([C, D, D, D], [C, C, C, C], [C])
        self.responses_test([C, C, D, D, D], [C, D, C, C, C], [D])


class TestForgetfulGrudger(TestPlayer):

    name = "Forgetful Grudger"
    player = axelrod.ForgetfulGrudger
    expected_classifier = {
        'memory_depth': 10,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):

        self.responses_test([], [], [C], attrs={"grudged": False})
        self.responses_test([C], [C], [C], attrs={"grudged": False})
        self.responses_test([C], [D], [D], attrs={"grudged": True})
        for i in range(10):
            self.responses_test([C, C] + [D] * i, [C, D] + [C] * i, [D],
                                attrs={"grudged": True, "grudge_memory": i,
                                       "mem_length": 10})
        # Forgets the grudge eventually
        i = 10
        self.responses_test([C, C] + [D] * i + [C], [C, D] + [C] * i + [C], [C],
                            attrs={"grudged": False, "grudge_memory": 0,
                                    "mem_length": 10})

    def test_reset_method(self):
        """Tests the reset method."""
        P1 = axelrod.ForgetfulGrudger()
        P1.history = [C, D, D, D]
        P1.grudged = True
        P1.grudge_memory = 4
        P1.reset()
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.grudged, False)
        self.assertEqual(P1.grudge_memory, 0)


class TestOppositeGrudger(TestPlayer):

    name = 'Opposite Grudger'
    player = axelrod.OppositeGrudger
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """Starts by defecting."""
        self.first_play_test(D)

    def test_strategy(self):
        """If opponent cooperates at any point then the player will cooperate
        forever."""
        self.responses_test([C, D, D, D], [D, D, D, D], [D])
        self.responses_test([C, C, D, D, D], [C, D, C, C, C], [C])


class TestAggravater(TestPlayer):

    name = "Aggravater"
    player = axelrod.Aggravater
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """
        Starts by defecting
        """
        self.first_play_test(D)

    def test_strategy(self):
        """
        If opponent defects at any point then the player will defect forever
        """
        self.responses_test([C, D, D, D], [C, C, C, C], [C])
        self.responses_test([C, C, D, D, D], [C, D, C, C, C], [D])
