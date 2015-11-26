"""Test for the retaliate strategy."""

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
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """If opponent has defected more than 10 percent of the time, defect."""
        P1 = axelrod.Retaliate()
        P2 = axelrod.Player()
        self.responses_test([C] * 4, [C] * 4, [C])
        self.responses_test([C, C, C, C, D], [C, C, C, D, C], [D])
        self.responses_test([C] * 6, [C] * 5 + [D], [D])


class TestLimitedRetaliate(TestPlayer):

    name = 'Limited Retaliate (0.1/20)'
    player = axelrod.LimitedRetaliate
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        P1 = axelrod.LimitedRetaliate()
        P2 = axelrod.Player()
        """If opponent has never defected, co-operate"""
        self.responses_test([C] * 4, [C] * 4, [C])
        P1.history = [C] * 5
        self.assertFalse(P1.retaliating)

        """If opponent has previously defected and won, defect and be retaliating"""
        self.responses_test([C, C, C, C, D], [C, C, C, D, C], [D])
        P1.history = [C, C, C, C, D, D]
        self.assertFalse(P1.retaliating)

        """If opponent has just defected and won, defect and be retaliating"""
        self.responses_test([C, C, C, C, C, C], [C, C, C, C, C, D], [D])
        P1.history = [C] * 6 + [D]
        self.assertFalse(P1.retaliating)

        """If I've hit the limit for retaliation attempts, co-operate"""
        P1.history = [C, C, C, C, D]
        P2.history = [C, C, C, D, C]
        P1.retaliation_count = 20
        self.assertEqual(P1.strategy(P2), C)
        self.assertFalse(P1.retaliating)

    def test_reset(self):
        P1 = axelrod.LimitedRetaliate()
        P1.history = [C, C, C, C, D]
        P1.retaliating = True
        P1.retaliation_count = 4
        P1.reset()
        self.assertEqual(P1.history, [])
        self.assertFalse(P1.retaliating)
        self.assertEqual(P1.retaliation_count, 0)
