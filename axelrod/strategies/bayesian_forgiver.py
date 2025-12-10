"""
Bayesian Forgiver - A strategy using Bayesian inference for adaptive forgiveness.

This strategy maintains a Bayesian belief about the opponent's cooperation probability
using a Beta distribution, and makes forgiveness decisions based on both the estimated
cooperation rate and the uncertainty in that estimate.
"""

from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class BayesianForgiver(Player):
    """
    A strategy that uses Bayesian inference to model opponent behavior and
    adaptively adjust forgiveness based on uncertainty.

    The strategy maintains a Beta distribution representing beliefs about the
    opponent's cooperation probability. It uses both the mean (expected cooperation
    rate) and variance (uncertainty) to make decisions:

    - When uncertain about the opponent's nature, it is optimistic and forgives more
    - When certain the opponent is hostile, it punishes consistently
    - When certain the opponent is cooperative, it cooperates consistently

    Algorithm:
    1. Maintain Beta(alpha, beta) distribution for opponent's cooperation probability
    2. Start with Beta(1, 1) - neutral/uniform prior
    3. Update after each round: C → alpha += 1, D → beta += 1
    4. Calculate mean = alpha / (alpha + beta)
    5. Calculate uncertainty (std deviation)
    6. Adaptive forgiveness: threshold = base_threshold + uncertainty_factor * uncertainty
    7. Forgive if mean > threshold, otherwise punish

    Names:
    - Bayesian Forgiver: Original name by Matt Hodges
    """

    name = "Bayesian Forgiver"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(
        self,
        prior_alpha: float = 1.0,
        prior_beta: float = 1.0,
        base_forgiveness_threshold: float = 0.45,
        uncertainty_factor: float = 2.5,
    ) -> None:
        """
        Initialize the Bayesian Forgiver strategy.

        Parameters
        ----------
        prior_alpha : float
            Initial alpha parameter for Beta distribution (default: 1.0)
            Represents prior belief in cooperation count + 1
            Higher values indicate stronger prior belief in cooperation
        prior_beta : float
            Initial beta parameter for Beta distribution (default: 1.0)
            Represents prior belief in defection count + 1
            Higher values indicate stronger prior belief in defection
        base_forgiveness_threshold : float
            Base threshold for forgiveness decision (default: 0.45)
            If estimated cooperation probability > threshold, forgive defections
        uncertainty_factor : float
            How much uncertainty increases forgiveness (default: 2.5)
            Higher values mean more optimism under uncertainty

        Note: Default parameters have been optimized through grid search
        to maximize performance against common IPD strategies.
        """
        super().__init__()
        self.prior_alpha = prior_alpha
        self.prior_beta = prior_beta
        self.base_forgiveness_threshold = base_forgiveness_threshold
        self.uncertainty_factor = uncertainty_factor

        # Initialize Bayesian belief parameters
        self.alpha = prior_alpha
        self.beta = prior_beta

    def reset(self):
        """Reset the strategy to initial state."""
        super().reset()
        self.alpha = self.prior_alpha
        self.beta = self.prior_beta

    def strategy(self, opponent: Player) -> Action:
        """
        Determine next action using Bayesian opponent model.

        Returns
        -------
        Action
            C (cooperate) or D (defect)
        """
        # First move: Start with cooperation (optimistic prior)
        if not self.history:
            return C

        # Update Bayesian belief based on opponent's last action
        if opponent.history[-1] == C:
            self.alpha += 1.0
        else:
            self.beta += 1.0

        # Calculate statistics from Beta distribution
        total = self.alpha + self.beta
        mean_cooperation = self.alpha / total

        # Calculate variance and standard deviation (uncertainty)
        # Var(Beta(α,β)) = αβ / ((α+β)²(α+β+1))
        variance = (self.alpha * self.beta) / (total * total * (total + 1))
        uncertainty = variance**0.5

        # Adaptive forgiveness threshold
        # Higher uncertainty → higher threshold → more forgiving
        forgiveness_threshold = (
            self.base_forgiveness_threshold
            + self.uncertainty_factor * uncertainty
        )

        # Decision logic
        if opponent.history[-1] == C:
            # Opponent cooperated last round - reciprocate cooperation
            return C
        else:
            # Opponent defected last round - decide whether to forgive or punish
            if mean_cooperation >= forgiveness_threshold:
                # Opponent's estimated cooperation rate is high enough to forgive
                # OR we're uncertain enough to be optimistic
                return C
            else:
                # Opponent appears to be hostile with sufficient confidence
                # Punish the defection
                return D
