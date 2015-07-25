from axelrod import Player
from meta import MetaPlayer


class DefectorHunter(Player):
    """A player who hunts for defectors."""

    name = 'Defector Hunter'
    memory_depth = float('inf')  # Long memory

    def strategy(self, opponent):
        if len(self.history) >= 5 and set(opponent.history) == set(['D']):
            return 'D'
        return 'C'


class CooperatorHunter(Player):
    """A player who hunts for cooperators."""

    name = 'Cooperator Hunter'
    memory_depth = float('inf')  # Long memory

    def strategy(self, opponent):
        if len(self.history) >= 5 and set(opponent.history) == set(['C']):
            return 'D'
        return 'C'


class AlternatorHunter(Player):
    """A player who hunts for alternators."""

    name = 'Alternator Hunter'
    memory_depth = float('inf')  # Long memory

    def strategy(self, opponent):
        oh = opponent.history
        if len(self.history) >= 5 and all([oh[i] != oh[i+1] for i in range(len(oh)-1)]):
            return 'D'
        return 'C'


class MathConstantHunter(Player):
    """A player who hunts for mathemtical constant players."""

    name = "Math Constant Hunter"
    memory_depth = float('inf')  # Long memory

    def strategy(self, opponent):
        """
        Check whether the number of cooperations in the first and second halves
        of the history are close. The variance of the uniform distribution (1/4)
        is a reasonable delta but use something lower for certainty. Note that
        this approach will also detect a lot of random players.
        """

        n = len(self.history)
        if n >= 10 and 'C' in opponent.history and 'D' in opponent.history:

            count1 = opponent.history[:n/2].count('C') + self.history[:n/2].count('C')
            count2 = opponent.history[n/2:].count('C') + self.history[n/2:].count('C')
            ratio1 = 1.0 * count1 / n
            ratio2 = 1.0 * count2 / n
            if abs(ratio1 - ratio2) < 0.2:
                return 'D'

        return 'C'


class RandomHunter(Player):
    """A player who hunts for random players."""

    name = "Random Hunter"
    memory_depth = float('inf')  # Long memory

    # We need to make sure this is not marked as stochastic.
    def __init__(self):
        Player.__init__(self)
        self.stochastic = False

    def strategy(self, opponent):
        """
        A random player is unpredictable, which means the conditional frequency
        of cooperation after cooperation, and defection afte defections, should
        be close 50%... although how close is debatable.
        """

        n = len(self.history)
        if n > 10:

            probabilities = []
            if 'C' in self.history[:-1]:
                countCC = len([i for i in range(n-1) if self.history[i] == "C" and opponent.history[i+1] == "C"])
                probabilities.append(1.0 * countCC / self.history[:-1].count("C"))
            if 'D' in self.history[:-1]:
                countDD = len([i for i in range(n-1) if self.history[i] == "D" and opponent.history[i+1] == "D"])
                probabilities.append(1.0 * countDD / self.history[:-1].count("D"))

            if all([abs(p - 0.5) < 0.11 for p in probabilities]):
                return 'D'

        return 'C'


class MetaHunter(MetaPlayer):
    """A player who uses a selection of hunters sequentially."""

    name = "Meta Hunter"
    memory_depth = float('inf')  # Long memory

    def __init__(self):

        # We need to make sure this is not marked as stochastic.
        self.stochastic = False

        # Notice that we don't include the cooperator hunter, because it leads to excessive
        # defection and therefore bad performance against unforgiving strategies. We will stick
        # to hunters that use defections as cues. However, a really tangible benefit comes from
        # combining Random Hunter and Math Constant Hunter, since together they catch strategies
        # that are lightly randomized but still quite constant (the tricky/suspecious ones).
        self.team = [DefectorHunter, AlternatorHunter, RandomHunter, MathConstantHunter]

        MetaPlayer.__init__(self)

    @staticmethod
    def meta_strategy(results):

        # If any of the hunters smells prey, then defect!
        if 'D' in results:
            return 'D'

        return 'C'
