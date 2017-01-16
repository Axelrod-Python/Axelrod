"""Tests for the Gradual Killer strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGradualKiller(TestPlayer):

    name = "Gradual Killer"
    player = axelrod.GradualKiller
    expected_classifier = {
        'memory_depth': float('Inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by Defecting.
        self.first_play_test(D)
        self.second_play_test(D, D, D, D)
        # First seven moves.
        self.responses_test([D, D, D, D, D, C, C])

    def test_effect_of_strategy_with_history_CC(self):
        """Continues with C if opponent played CC on 6 and 7."""
        P1 = axelrod.GradualKiller()
        P2 = axelrod.Player()
        P1.history = [D, D, D, D, D, C, C]
        P2.history = [C, C, C, C, C, C, C]
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = [D, D, D, D, D, C, C, C]
        P2.history = [C, C, C, C, C, C, C, C]
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = [D, D, D, D, D, C, C, C, C]
        P2.history = [C, C, C, C, C, C, C, C, C]
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = [D, D, D, D, D, C, C, C, C, C]
        P2.history = [C, C, C, C, C, C, C, C, C, C]
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy_with_history_CD(self):
        """Continues with C if opponent played CD on 6 and 7."""
        P1 = axelrod.GradualKiller()
        P2 = axelrod.Player()
        P1.history = [D, D, D, D, D, C, C]
        P2.history = [C, C, C, C, C, C, D]
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = [D, D, D, D, D, C, C, C]
        P2.history = [C, C, C, C, C, C, D, D]
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = [D, D, D, D, D, C, C, C, C]
        P2.history = [C, C, C, C, C, C, D, D, C]
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = [D, D, D, D, D, C, C, C, C, C]
        P2.history = [C, C, C, C, C, C, D, D, C, C]
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy_with_history_DC(self):
        """Continues with C if opponent played DC on 6 and 7."""
        P1 = axelrod.GradualKiller()
        P2 = axelrod.Player()
        P1.history = [D, D, D, D, D, C, C]
        P2.history = [C, C, C, C, C, D, C]
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = [D, D, D, D, D, C, C, C]
        P2.history = [C, C, C, C, C, D, C, C]
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = [D, D, D, D, D, C, C, C, C]
        P2.history = [C, C, C, C, C, D, C, C, D]
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = [D, D, D, D, D, C, C, C, C, C]
        P2.history = [C, C, C, C, C, D, C, C, D, C]
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy_with_history_CC(self):
        """Continues with D if opponent played DD on 6 and 7."""
        P1 = axelrod.GradualKiller()
        P2 = axelrod.Player()
        P1.history = [D, D, D, D, D, C, C]
        P2.history = [C, C, C, C, C, D, D]
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = [D, D, D, D, D, C, C, D]
        P2.history = [C, C, C, C, C, D, D, C]
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = [D, D, D, D, D, C, C, D, D]
        P2.history = [C, C, C, C, C, D, D, C, C]
        self.assertEqual(P1.strategy(P2), 'D')
        P1.history = [D, D, D, D, D, C, C, D, D, D]
        P2.history = [C, C, C, C, C, D, D, C, C, D]
        self.assertEqual(P1.strategy(P2), 'D')

