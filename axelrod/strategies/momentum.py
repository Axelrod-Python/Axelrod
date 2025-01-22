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

    Names:
     - Momentum: Original name by Dong Won Moon

    Notes:
     - While I am an undergraduate student with limited experience in game theory, I
       believe this strategy has potential in various scenarios.
     - I encourage experts to explore and extend this idea in other contexts, such as
       environments with noise, one-hot vectorization approaches at multiple actions.

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
        alpha=0.9914655399877477,  # Optimized by Genetic Algorithm. You can try to adapt it to any Env.
        threshold=0.9676595613724907, # This one too
    ) -> None:
        super().__init__()
        self.alpha = alpha
        self.threshold = threshold
        self.momentum = 1.0

    def __repr__(self):
        return f"Momentum: {self.alpha}, {self.threshold}"

    def update_momentum(self, opponent_action):
        action_value = 1 if opponent_action == C else 0
        # If the opponent defects, the momentum decreases, reflecting a loss of trust.
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
