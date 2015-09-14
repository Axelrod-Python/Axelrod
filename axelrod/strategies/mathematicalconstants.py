from axelrod import Player
from math import sqrt, pi, e


class CotoDeRatio(Player):
    """The player will always aim to bring the ratio of co-operations to
    defections closer to the ratio as given in a sub class"""

    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),  # Long memory
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):

        # Initially cooperate
        if len(opponent.history) == 0:
            return 'C'

        # Avoid initial division by zero
        if not opponent.defections:
            return 'D'

        # Otherwise compare ratio to golden mean
        cooperations = opponent.cooperations + self.cooperations
        defections = float(opponent.defections + self.defections)
        if cooperations / defections > self.ratio:
            return 'D'
        return 'C'


class Golden(CotoDeRatio):
    """The player will always aim to bring the ratio of co-operations to defections closer to the golden mean"""

    name = '$\phi$'
    ratio = (1 + sqrt(5)) / 2


class Pi(CotoDeRatio):
    """The player will always aim to bring the ratio of co-operations to defections closer to the pi"""

    name = '$\pi$'
    ratio = pi


class e(CotoDeRatio):
    """The player will always aim to bring the ratio of co-operations to defections closer to the e"""

    name = '$e$'
    ratio = e
