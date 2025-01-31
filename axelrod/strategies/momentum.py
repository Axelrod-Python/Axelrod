from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class Momentum(Player):
    """
    This strategy is inspired by the concept of Gradual and the mathematical foundation of
    the Momentum optimizer used in deep learning.

    The idea is that trust (or cooperation) evolves dynamically. A shift in trust can
    create significant and rapid changes in the player's behavior, much like how momentum
    responds to gradients in optimization.

    Parameters:
     - alpha: Momentum decay factor that determines the rate of trust reduction. A higher value leads to slower decay, and the opponent's Defect acts as a trigger. (Optimized by Genetic Algorithm)
     - threshold: The minimum momentum required to continue cooperation. If momentum falls below this value, the strategy switches to Defect as punishment. (Optimized by Genetic Algorithm)
     - momentum: Represents the inertia of trust, dynamically changing based on past cooperation.

    Names:
     - Momentum: Original name by Dong Won Moon

    """

    name = "Momentum"
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
        alpha=0.9914655399877477,
        threshold=0.9676595613724907,
    ) -> None:
        super().__init__()
        self.alpha = alpha
        self.threshold = threshold
        self.momentum = 1.0

    def __repr__(self):
        return f"Momentum: {self.momentum}, Alpha: {self.alpha}, Threshold: {self.threshold}"

    def update_momentum(self, opponent_action):
        # If the opponent defects, the momentum decreases, reflecting a loss of trust.
        action_value = 1 if opponent_action == C else 0
        self.momentum = (
            self.alpha * self.momentum + (1 - self.alpha) * action_value
        )

    def strategy(self, opponent: Player) -> Action:
        if len(self.history) == 0:
            self.momentum = 1.0
            return C

        else:
            self.update_momentum(opponent.history[-1])
            return C if self.momentum >= self.threshold else D
