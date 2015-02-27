from axelrod import Player
from math import sqrt, pi, e

class Golden(Player):
    """The player will always aim to bring the ratio of co-operations to defections closer to the golden mean"""

    name = 'Golden'
    golden_ratio = (1 + sqrt(5)) / 2

    def strategy(self,opponent):

        """initially co-operates"""
        if len(opponent.history) == 0:
            return 'C'

        """to avoid initial division by zero"""
        if sum([s == 'D' for s in opponent.history]) == 0:
            return 'D'

        """otherwise compare ratio to golden mean"""
        if (sum([p == 'C' for p in opponent.history]) + sum([q == 'C' for q in self.history]))/(sum([x == 'D' for x in opponent.history]) + sum([y == 'D' for y in self.history])) > self.golden_ratio:
            return 'D'
        return 'C'


class Pi(Player):
    """The player will always aim to bring the ratio of co-operations to defections closer to the golden mean"""

    name = 'Pi'

    def strategy(self,opponent):

        """initially co-operates"""
        if len(opponent.history) == 0:
            return 'C'

        """to avoid initial division by zero"""
        if sum([s == 'D' for s in opponent.history]) == 0:
            return 'D'

        """otherwise compare ratio to golden mean"""
        if (sum([p == 'C' for p in opponent.history]) + sum([q == 'C' for q in self.history]))/(sum([x == 'D' for x in opponent.history]) + sum([y == 'D' for y in self.history])) > pi:
            return 'D'
        return 'C'


class e(Player):
    """The player will always aim to bring the ratio of co-operations to defections closer to the golden mean"""

    name = 'e'

    def strategy(self,opponent):

        """initially co-operates"""
        if len(opponent.history) == 0:
            return 'C'

        """to avoid initial division by zero"""
        if sum([s == 'D' for s in opponent.history]) == 0:
            return 'D'

        """otherwise compare ratio to golden mean"""
        if (sum([p == 'C' for p in opponent.history]) + sum([q == 'C' for q in self.history]))/(sum([x == 'D' for x in opponent.history]) + sum([y == 'D' for y in self.history])) > e:
            return 'D'
        return 'C'

