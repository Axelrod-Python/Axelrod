"""Tests for the retaliate strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestRetaliate(TestPlayer):

    name = "Retaliate (0.1)"
    player = axelrod.Retaliate
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
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """If opponent has defected more than 10 percent of the time, defect."""
        self.responses_test(C, C * 4, C * 4)
        self.responses_test(D, C * 4 + D, C * 3 + D + C)
        self.responses_test(D, C * 6, C * 5 + D)


class TestLimitedRetaliate(TestPlayer):

    name = 'Limited Retaliate (0.1/20)'
    player = axelrod.LimitedRetaliate
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
        self.first_play_test(C)

        # If opponent has never defected, co-operate
        self.responses_test(C, C * 4, C * 4, attrs={"retaliating": False})

        # Retaliate after a (C, D) round
        self.responses_test(D, C * 4 + D, C * 3 + D + C,
                            attrs={"retaliating": True})
        self.responses_test(D, C * 6, C * 5 + D,
                            attrs={"retaliating": True})

        # Case were retaliation count is less than limit: cooperate, reset
        # retaliation count and be not retaliating
        P1 = axelrod.LimitedRetaliate()
        P2 = axelrod.Player()
        P1.history = [C, C, C, D, C]
        P2.history = [D, D, D, C, D]
        P1.retaliation_count = 1
        P1.retaliation_limit = 0
        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.retaliation_count, 0)
        self.assertFalse(P1.retaliating)

        # If I've hit the limit for retaliation attempts, co-operate
        P1.history = [C, C, C, C, D]
        P2.history = [C, C, C, D, C]
        P1.retaliation_count = 20
        self.assertEqual(P1.strategy(P2), C)
        self.assertFalse(P1.retaliating)

    def test_reset(self):
        P1 = axelrod.LimitedRetaliate()
        P1.retaliating = True
        P1.retaliation_count = 4
        P1.reset()
        self.assertFalse(P1.retaliating)
        self.assertEqual(P1.retaliation_count, 0)
