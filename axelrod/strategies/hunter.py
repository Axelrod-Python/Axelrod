from __future__ import absolute_import

from axelrod import Player


class DefectorHunter(Player):
    """A player who hunts for defectors."""

    name = 'Defector Hunter'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        if len(self.history) >= 4 and len(opponent.history) == opponent.defections:
            return 'D'
        return 'C'


class CooperatorHunter(Player):
    """A player who hunts for cooperators."""

    name = 'Cooperator Hunter'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        if len(self.history) >= 4 and len(opponent.history) == opponent.cooperations:
            return 'D'
        return 'C'


class AlternatorHunter(Player):
    """A player who hunts for alternators."""

    name = 'Alternator Hunter'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        oh = opponent.history
        if len(self.history) >= 6 and all([oh[i] != oh[i+1] for i in range(len(oh)-1)]):
            return 'D'
        return 'C'


class MathConstantHunter(Player):
    """A player who hunts for mathematical constant players."""

    name = "Math Constant Hunter"
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        """
        Check whether the number of cooperations in the first and second halves
        of the history are close. The variance of the uniform distribution (1/4)
        is a reasonable delta but use something lower for certainty and avoiding
        false positives. This approach will also detect a lot of random players.
        """

        n = len(self.history)
        if n >= 8 and opponent.cooperations and opponent.defections:

            start1, end1 = 0, n // 2
            start2, end2 = n // 4, 3 * n // 4
            start3, end3 = n // 2, n
            count1 = opponent.history[start1: end1].count('C') + self.history[start1: end1].count('C')
            count2 = opponent.history[start2: end2].count('C') + self.history[start2: end2].count('C')
            count3 = opponent.history[start3: end3].count('C') + self.history[start3: end3].count('C')
            ratio1 = 0.5 * count1 / (end1 - start1)
            ratio2 = 0.5 * count2 / (end2 - start2)
            ratio3 = 0.5 * count3 / (end3 - start3)
            if abs(ratio1 - ratio2) < 0.2 and abs(ratio1 - ratio3) < 0.2:
                return 'D'

        return 'C'


class RandomHunter(Player):
    """A player who hunts for random players."""

    name = "Random Hunter"
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        """
        A random player is unpredictable, which means the conditional frequency
        of cooperation after cooperation, and defection after defections, should
        be close to 50%... although how close is debatable.
        """

        n = len(self.history)
        if n > 10:
            probabilities = []
            if self.history[:-1].count('C') > 5:
                countCC = len([i for i in range(n-1) if self.history[i] == "C" and opponent.history[i+1] == "C"])
                probabilities.append(1.0 * countCC / self.history[:-1].count("C"))
            if self.history[:-1].count('D') > 5:
                countDD = len([i for i in range(n-1) if self.history[i] == "D" and opponent.history[i+1] == "D"])
                probabilities.append(1.0 * countDD / self.history[:-1].count("D"))

            if probabilities and all([abs(p - 0.5) < 0.25 for p in probabilities]):
                return 'D'

        return 'C'
