import random

from axelrod import Player

from meta import MetaPlayer


class DefectorHunter(Player):
    """A player who hunts for defectors."""

    name = 'Defector Hunter'

    def strategy(self, opponent):
        if len(self.history) >= 4 and all([h == 'D' for h in opponent.history]):
            return 'D'
        return 'C'


class CooperatorHunter(Player):
    """A player who hunts for cooperators."""

    name = 'Cooperator Hunter'

    def strategy(self, opponent):
        if len(self.history) >= 4 and all([h == 'C' for h in opponent.history]):
            return 'D'

        return 'C'


class AlternatorHunter(Player):
    """A player who hunts for alternators."""

    name = 'Alternator Hunter'

    def strategy(self, opponent):
        oh = opponent.history
        if len(self.history) >= 4 and all([oh[i] != oh[i+1] for i in range(len(oh)-1)]):
            return 'D'
        return 'C'


class MathConstantHunter(Player):
    """A player who hunts for mathemtical constant players."""

    name = "Math Constant Hunter"

    def strategy(self, opponent):

        n = len(self.history)
        if n >= 8 and 'C' in opponent.history and 'D' in opponent.history:

            # The variance of the uniform distribution is about 1/4, so we can expect
            # that the difference in proportion of defects/cooperations in two halves
            # will quickly vary by less than that.
            delta = abs(opponent.history[:n/2].count('D') - opponent.history[n/2:].count('D'))
            if delta < 0.25 * n:
                return 'D'

        return 'C'


class RandomHunter(Player):
    """A player who hunts for random players."""

    name = "Random Hunter"

    # We need to make sure this is not marked as stochastic.
    def __init__(self):
        Player.__init__(self)
        self.stochastic = False

    def strategy(self, opponent):

        n = len(self.history)
        if n >= 8 and 'C' in opponent.history and 'D' in opponent.history:

            # In terms of rewards, random players will produce unjustified defections,
            # more or less as often as expected by pure chance.
            justified = [i for i in range(1, n) if opponent.history[i] == 'D' and self.history[i-1] == 'D']
            expected = 1.0 * opponent.history.count('D') * self.history.count('D') / n
            if len(justified) < expected + 3:
                return 'D'

        return 'C'


class MetaHunter(MetaPlayer):
    """A player who uses a selection of hunters sequentially."""

    name = "Meta Hunter"

    def __init__(self):

        # We need to make sure this is not marked as stochastic.
        self.stochastic = False

        # Notice that we don't include the cooperator hunter, because it leads to excessive
        # defection and therefore bad performance against unforgiving strategies. We will stick
        # to hunters that use defections as cues. However, a really tangible benefit comes from
        # combining Random Hunter and Math Constant Hunter, since together they catch strategies
        # that are lightly randomized but still quite constant (the tricky/suspecious ones).
        self.team = [DefectorHunter, AlternatorHunter, MathConstantHunter, RandomHunter]

        MetaPlayer.__init__(self)

    def meta_strategy(self, results):

        # If any of the hunters smells prey, then defect!
        if 'D' in results:
            return 'D'
        return 'C'