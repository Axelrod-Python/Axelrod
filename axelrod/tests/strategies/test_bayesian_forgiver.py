"""Tests for the Bayesian Forgiver strategy."""

import axelrod as axl
from axelrod.tests.property import strategy_lists

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestBayesianForgiver(TestPlayer):
    """Test suite for BayesianForgiver strategy."""

    name = "Bayesian Forgiver: 1.0, 1.0, 0.45, 2.5"
    player = axl.BayesianForgiver
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_initial_strategy(self):
        """Test that the strategy starts by cooperating."""
        actions = [(C, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions)

    def test_vs_cooperator(self):
        """Test behavior against always cooperate - should cooperate."""
        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions)

    def test_vs_defector(self):
        """Test behavior against always defect - should eventually defect back."""
        # First move: cooperate
        # After seeing D, Bayesian model updates: alpha=1, beta=2, mean=0.33
        # Even with high uncertainty, mean is below threshold, so defect
        actions = [(C, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(axl.Defector(), expected_actions=actions)

    def test_vs_alternator(self):
        """Test behavior against alternating strategy."""
        # With parameters (1.0, 1.0, 0.45, 2.5):
        # Early uncertainty is high, so threshold is high, but mean cooperation ~0.5
        # When opponent defects, we evaluate: mean < threshold → defect
        # This creates an alternating pattern
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D)]
        self.versus_test(axl.Alternator(), expected_actions=actions)

    def test_vs_tit_for_tat(self):
        """Test behavior against Tit For Tat - should achieve mutual cooperation."""
        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axl.TitForTat(), expected_actions=actions)

    def test_vs_suspicious_tit_for_tat(self):
        """Test against Suspicious Tit For Tat (starts with D)."""
        # STF starts with D, then mirrors
        # BF starts with C, sees D → defects back
        # This creates an alternating pattern
        actions = [(C, D), (D, C), (C, D), (D, C), (C, D)]
        self.versus_test(axl.SuspiciousTitForTat(), expected_actions=actions)

    def test_vs_grudger(self):
        """Test behavior against Grudger."""
        # Grudger cooperates until any defection, then defects forever
        # BayesianForgiver should cooperate, so mutual cooperation
        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axl.Grudger(), expected_actions=actions)

    def test_vs_random(self):
        """Test behavior against Random strategy with specific seed."""
        # Random behavior - BayesianForgiver should adapt
        # With seed=3, Random plays: C, C, C, C, D
        actions = [(C, C), (C, C), (C, C), (C, C), (C, D)]
        self.versus_test(axl.Random(), expected_actions=actions, seed=3)

    def test_vs_mock_single_defection(self):
        """Test response to a single defection."""
        # Opponent cooperates then defects once then cooperates
        # With new parameters: after seeing one D among many Cs, still punishes
        # but quickly returns to cooperation
        opponent = axl.MockPlayer(actions=[C, C, C, D, C, C, C])
        actions = [
            (C, C),  # Both cooperate
            (C, C),  # Both cooperate
            (C, C),  # Both cooperate
            (C, D),  # Opponent defects - alpha=4, beta=2
            (D, C),  # Punish the defection
            (C, C),  # Resume cooperation
            (C, C),  # Continue cooperation
        ]
        self.versus_test(opponent, expected_actions=actions)

    def test_vs_mock_consistent_defector(self):
        """Test punishment of consistent defector."""
        # Opponent defects consistently
        opponent = axl.MockPlayer(actions=[D, D, D, D, D, D])
        actions = [
            (C, D),  # Start optimistic, see D - alpha=1, beta=2
            (D, D),  # Mean = 0.33, below threshold even with uncertainty
            (D, D),  # Continue defecting
            (D, D),  # Continue defecting
            (D, D),  # Continue defecting
            (D, D),  # Continue defecting
        ]
        self.versus_test(opponent, expected_actions=actions)

    def test_vs_mock_mixed_behavior(self):
        """Test adaptation to mixed behavior."""
        # Opponent with mixed C and D: [C, C, D, C, D, C, C, D]
        # With default parameters, responds more reactively to defections
        opponent = axl.MockPlayer(actions=[C, C, D, C, D, C, C, D])
        actions = [
            (C, C),  # Start cooperating
            (C, C),  # Continue cooperating
            (C, D),  # Opponent defects
            (D, C),  # Punish defection
            (C, D),  # Opponent cooperated, we cooperate, they defect
            (D, C),  # Punish again
            (C, C),  # Resume cooperation
            (C, D),  # Cooperate, opponent defects
        ]
        self.versus_test(opponent, expected_actions=actions)

    def test_parameter_changes(self):
        """Test that different parameters affect behavior."""
        # Test with different prior - more pessimistic
        player = self.player(prior_alpha=1.0, prior_beta=2.0)
        opponent = axl.Defector()
        match = axl.Match([player, opponent], turns=3)
        result = match.play()
        # With pessimistic prior and defector opponent, should defect quickly
        self.assertEqual(result[0], (C, D))  # First move still C
        self.assertEqual(result[1][0], D)  # Should defect after seeing D

    def test_reset(self):
        """Test that reset properly reinitializes the strategy."""
        player = self.player()
        opponent = axl.Cooperator()

        # Play some rounds - opponent cooperates so alpha should increase
        for _ in range(5):
            player.strategy(opponent)
            opponent.strategy(player)
            player.update_history(C, C)
            opponent.update_history(C, C)

        # Alpha should have changed (beta stays the same since opponent always cooperates)
        self.assertNotEqual(player.alpha, player.prior_alpha)

        # Reset
        player.reset()

        # Should be back to initial values
        self.assertEqual(player.alpha, player.prior_alpha)
        self.assertEqual(player.beta, player.prior_beta)

    def test_clone(self):
        """Test that cloning preserves parameters."""
        player = self.player(
            prior_alpha=3.0,
            prior_beta=2.0,
            base_forgiveness_threshold=0.4,
            uncertainty_factor=2.0,
        )
        clone = player.clone()

        self.assertEqual(clone.prior_alpha, 3.0)
        self.assertEqual(clone.prior_beta, 2.0)
        self.assertEqual(clone.base_forgiveness_threshold, 0.4)
        self.assertEqual(clone.uncertainty_factor, 2.0)
        self.assertEqual(clone.alpha, 3.0)
        self.assertEqual(clone.beta, 2.0)
