from typing import Dict, Tuple

from axelrod.action import Action
from axelrod.player import Player
from numpy import heaviside

C, D = Action.C, Action.D


class AbstractAdaptor(Player):
    """
    An adaptive strategy that updates an internal state based on the last
    round of play. Using this state the player Cooperates with a probability
    derived from the state.

    s, float:
        the internal state, initially 0
    perr, float:
        an error threshold for misinterpreted moves
    delta, a dictionary of floats:
        additive update values for s depending on the last round's outcome

    Names:

    - Adaptor: [Hauert2002]_

    """

    name = "AbstractAdaptor"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, delta: Dict[Tuple[Action, Action], float],
                 perr: float = 0.01) -> None:
        super().__init__()
        self.perr = perr
        self.delta = delta
        self.s = 0.

    def strategy(self, opponent: Player) -> Action:
        if self.history:
            # Update internal state from the last play
            last_round = (self.history[-1], opponent.history[-1])
            self.s += self.delta[last_round]

        # Compute probability of Cooperation
        p = self.perr + (1.0 - 2 * self.perr) * (
            heaviside(self.s + 1, 1) - heaviside(self.s - 1, 1))
        # Draw action
        action = self._random.random_choice(p)
        return action


class AdaptorBrief(AbstractAdaptor):
    """
    An Adaptor trained on short interactions.

    Names:

    - AdaptorBrief: [Hauert2002]_

    """

    name = "AdaptorBrief"

    def __init__(self) -> None:
        delta = {
            (C, C): 0.,         # R
            (C, D): -1.001505,  # S
            (D, C): 0.992107,   # T
            (D, D): -0.638734   # P
        }
        super().__init__(delta=delta)


class AdaptorLong(AbstractAdaptor):
    """
    An Adaptor trained on long interactions.

    Names:

    - AdaptorLong: [Hauert2002]_

    """

    name = "AdaptorLong"

    def __init__(self) -> None:
        delta = {
            (C, C): 0.,        # R
            (C, D): 1.888159,  # S
            (D, C): 1.858883,  # T
            (D, D): -0.995703  # P
        }
        super().__init__(delta=delta)
