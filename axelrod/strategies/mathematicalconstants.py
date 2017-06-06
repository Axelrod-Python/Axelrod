import math

from axelrod.actions import Actions, Action
from axelrod.player import Player

C, D = Actions.C, Actions.D


class CotoDeRatio(Player):
    """The player will always aim to bring the ratio of co-operations to
    defections closer to the ratio as given in a sub class

    Names:

    - Co to Do Ratio: Original Name by Timothy Standen
    """

    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),  # Long memory
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        # Initially cooperate
        if len(opponent.history) == 0:
            return C
        # Avoid initial division by zero
        if not opponent.defections:
            return D
        # Otherwise compare ratio to golden mean
        cooperations = opponent.cooperations + self.cooperations
        defections = opponent.defections + self.defections
        if cooperations / defections > self.ratio:
            return D
        return C


class Golden(CotoDeRatio):
    """The player will always aim to bring the ratio of co-operations to
    defections closer to the golden mean

    Names:

    - Golden: Original Name by Timothy Standen
    """

    name = '$\phi$'
    ratio = (1 + math.sqrt(5)) / 2


class Pi(CotoDeRatio):
    """The player will always aim to bring the ratio of co-operations to
    defections closer to the pi

    Names:

    - Pi: Original Name by Timothy Standen
    """

    name = '$\pi$'
    ratio = math.pi


class e(CotoDeRatio):
    """The player will always aim to bring the ratio of co-operations to
    defections closer to the e

    Names:

    - e: Original Name by Timothy Standen
    """

    name = '$e$'
    ratio = math.e
