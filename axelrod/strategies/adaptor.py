from typing import Dict, Tuple

from axelrod.action import Action
from axelrod.player import Player
from axelrod.random_ import random_choice

from numpy import heaviside

C, D = Action.C, Action.D


class AbstractAdaptor(Player):
    """
    An adaptive strategy that updates an internal state based on the last
    round of play. Using this state the player Cooperates with a probability
    derived from the state.

    Names:

    - Adaptor: [Hauert2002]_

    """

    name = "AbstractAdaptor"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, d: Dict[Tuple[Action], float], perr: float = 0.01) -> None:
        super().__init__()
        self.perr = perr
        if not d:
            d = {(C, C): 1., # R
                 (C, D): 1., # S
                 (D, C): 1., # T
                 (D, D): 1.  # P
                 }
        self.d = d
        self.s = 0.

    def strategy(self, opponent: Player) -> Action:
        if self.history:
            # Update internal state from the last play
            last_round = (self.history[-1], opponent.history[-1])
            self.s += d[last_round]

        # Compute probability of Cooperation
        p = self.perr + (1.0 - 2 * self.perr) * (
            heaviside(self.s + 1, 1) - heaviside(self.s - 1, 1))
        # Draw action
        action = random_choice(p)
        return action


class AdaptorBrief(Player):
    """
    An Adaptor trained on short interactions.

    Names:

    - AdaptorBrief: [Hauert2002]_

    """

    name = "AdaptorBrief"

    def __init__(self) -> None:
        d = {(C, C): 0.,        # R
             (C, D): 1.001505,  # S
             (D, C): 0.992107,  # T
             (D, D): 0.638734   # P
             }
        super().__init__(d=d)


class AdaptorLong(Player):
    """
    An Adaptor trained on long interactions.

    Names:

    - AdaptorLong: [Hauert2002]_

    """

    name = "AdaptorLong"

    def __init__(self) -> None:
        d = {(C, C): 0.,        # R
             (C, D): 1.888159,  # S
             (D, C): 1.858883,  # T
             (D, D): 0.995703   # P
             }
        super().__init__(d=d)
