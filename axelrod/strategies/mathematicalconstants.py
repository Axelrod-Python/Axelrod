from axelrod import Player
from math import sqrt, pi, e

class CotoDeRatio(Player):
    """The player will always aim to bring the ratio of co-operations to defections closer to the ratio as given in a sub class"""

    def strategy(self,opponent):

        """initially co-operates"""
        if len(opponent.history) == 0:
            return 'C'

        """to avoid initial division by zero"""
        if sum([s == 'D' for s in opponent.history]) == 0:
            return 'D'

        """otherwise compare ratio to golden mean"""
        if (sum([p == 'C' for p in opponent.history]) + sum([q == 'C' for q in self.history]))/(sum([x == 'D' for x in opponent.history]) + sum([y == 'D' for y in self.history])) > self.ratio:
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
