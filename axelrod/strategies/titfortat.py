from axelrod import Actions, Player, init_args
from axelrod.strategy_transformers import TrackHistoryTransformer

C, D = Actions.C, Actions.D


class TitForTat(Player):
    """
    A player starts by cooperating and then mimics the previous action of the
    opponent.

    Note that the code for this strategy is written in a fairly verbose
    way. This is done so that it can serve as an example strategy for
    those who might be new to Python.

    Names:

    - Rapoport's strategy: [Axelrod1980]_
    - TitForTat: [Axelrod1980]_
    """

    # These are various properties for the strategy
    name = 'Tit For Tat'
    classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        """This is the actual strategy"""
        # First move
        if len(self.history) == 0:
            return C
        # React to the opponent's last move
        if opponent.history[-1] == D:
            return D
        return C


class TitFor2Tats(Player):
    """A player starts by cooperating and then defects only after two defects by
    opponent.

    Names:

    - Tit for two Tats: [Axelrod1984]_
    """

    name = "Tit For 2 Tats"
    classifier = {
        'memory_depth': 2,  # Long memory, memory-2
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return D if opponent.history[-2:] == [D, D] else C


class TwoTitsForTat(Player):
    """A player starts by cooperating and replies to each defect by two
    defections.

    Names:

    - Two Tits for Tats: [Axelrod1984]_
    """

    name = "Two Tits For Tat"
    classifier = {
        'memory_depth': 2,  # Long memory, memory-2
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return D if D in opponent.history[-2:] else C


class Bully(Player):
    """A player that behaves opposite to Tit For Tat, including first move.

    Starts by defecting and then does the opposite of opponent's previous move.
    This is the complete opposite of Tit For Tat, also called Bully in the
    literature.

    Names:

    - Reverse Tit For Tat: [Nachbar1992]_

    """

    name = "Bully"
    classifier = {
        'memory_depth': 1,   # Four-Vector = (0, 1, 0, 1)
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return C if opponent.history[-1:] == [D] else D


class SneakyTitForTat(Player):
    """Tries defecting once and repents if punished.

    Names:

    - Sneaky Tit For Tat: Reference Required
    """

    name = "Sneaky Tit For Tat"
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        if len(self.history) < 2:
            return "C"
        if D not in opponent.history:
            return D
        if opponent.history[-1] == D and self.history[-2] == D:
            return "C"
        return opponent.history[-1]


class SuspiciousTitForTat(Player):
    """A variant of Tit For Tat that starts off with a defection.

    Names:

    - Suspicious Tit For Tat: [Hilde2013]_
    """

    name = "Suspicious Tit For Tat"
    classifier = {
        'memory_depth': 1, # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return C if opponent.history[-1:] == [C] else D


class AntiTitForTat(Player):
    """A strategy that plays the opposite of the opponents previous move.
    This is similar to Bully, except that the first move is cooperation.

    Names:

    - Anti Tit For Tat: [Hilde2013]_
    """

    name = 'Anti Tit For Tat'
    classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return D if opponent.history[-1:] == [C] else C


class HardTitForTat(Player):
    """A variant of Tit For Tat that uses a longer history for retaliation.

    Names:

    - Hard Tit For Tat: Reference Required
    """

    name = 'Hard Tit For Tat'
    classifier = {
        'memory_depth': 3,  # memory-three
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        # Cooperate on the first move
        if not opponent.history:
            return C
        # Defects if D in the opponent's last three moves
        if D in opponent.history[-3:]:
            return D
        # Otherwise cooperates
        return C


class HardTitFor2Tats(Player):
    """A variant of Tit For Two Tats that uses a longer history for
    retaliation.

    Names:

    - Hard Tit For Two Tats: Reference Required
    """

    name = "Hard Tit For 2 Tats"
    classifier = {
        'memory_depth': 3,  # memory-three
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        # Cooperate on the first move
        if not opponent.history:
            return C
        # Defects if two consecutive D in the opponent's last three moves
        history_string = "".join(opponent.history[-3:])
        if 'DD' in history_string:
            return D
        # Otherwise cooperates
        return C


class OmegaTFT(Player):
    """OmegaTFT modifies Tit For Tat in two ways:
       - checks for deadlock loops of alternating rounds of (C, D) and (D, C),
       and attempting to break them
       - uses a more sophisticated retaliation mechanism that is noise tolerant.

       Names:

       - OmegaTFT: [Slany2007]_
    """

    name = "Omega TFT"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self, deadlock_threshold=3, randomness_threshold=8):
        Player.__init__(self)
        self.deadlock_threshold = deadlock_threshold
        self.randomness_threshold = randomness_threshold
        self.randomness_counter = 0
        self.deadlock_counter = 0

    def strategy(self, opponent):
        # Cooperate on the first move
        if len(self.history) == 0:
            return C
        # TFT on round 2
        if len(self.history) == 1:
            return D if opponent.history[-1:] == [D] else C

        # Are we deadlocked? (in a CD -> DC loop)
        if (self.deadlock_counter >= self.deadlock_threshold):
            self.move = C
            if self.deadlock_counter == self.deadlock_threshold:
                self.deadlock_counter = self.deadlock_threshold + 1
            else:
                self.deadlock_counter = 0
        else:
            # Update counters
            if opponent.history[-2:] == [C, C]:
                self.randomness_counter -= 1
            # If the opponent's move changed, increase the counter
            if opponent.history[-2] != opponent.history[-1]:
                self.randomness_counter += 1
            # If the opponent's last move differed from mine, increase the counter
            if self.history[-1] == opponent.history[-1]:
                self.randomness_counter+= 1
            # Compare counts to thresholds
            # If randomness_counter exceeds Y, Defect for the remainder
            if self.randomness_counter >= 8:
                self.move = D
            else:
                # TFT
                self.move = D if opponent.history[-1:] == [D] else C
                # Check for deadlock
                if opponent.history[-2] != opponent.history[-1]:
                    self.deadlock_counter += 1
                else:
                    self.deadlock_counter = 0
        return self.move

    def reset(self):
        Player.reset(self)
        self.randomness_counter = 0
        self.deadlock_counter = 0


class Gradual(Player):
    """
    A player that punishes defections with a growing number of defections
    but after punishing enters a calming state and cooperates no matter what
    the opponent does for two rounds.

    Names:

    - Gradual: [Beaufils1997]_
     """

    name = "Gradual"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):

        Player.__init__(self)
        self.calming = False
        self.punishing = False
        self.punishment_count = 0
        self.punishment_limit = 0

    def strategy(self, opponent):

        if self.calming:
            self.calming = False
            return C

        if self.punishing:
            if self.punishment_count < self.punishment_limit:
                self.punishment_count += 1
                return D
            else:
                self.calming = True
                self.punishing = False
                self.punishment_count = 0
                return C

        if D in opponent.history[-1:]:
            self.punishing = True
            self.punishment_count += 1
            self.punishment_limit += 1
            return D

        return C

    def reset(self):
        Player.reset(self)
        self.calming = False
        self.punishing = False
        self.punishment_count = 0
        self.punishment_limit = 0


@TrackHistoryTransformer(name_prefix=None)
class ContriteTitForTat(Player):
    """
    A player that corresponds to Tit For Tat if there is no noise. In the case
    of a noisy match: if the opponent defects as a result of a noisy defection
    then ContriteTitForTat will become 'contrite' until it successfully
    cooperates.

    Names:

    - Contrite Tit For Tat: [Axelrod1995]_
    """

    name = "Contrite Tit For Tat"
    classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }
    contrite = False

    def strategy(self, opponent):

        if not opponent.history:
            return C

        # If contrite but managed to cooperate: apologise.
        if self.contrite and self.history[-1] == C:
            self.contrite = False
            return C

        # Check if noise provoked opponent
        if self._recorded_history[-1] != self.history[-1]:  # Check if noise
            if self.history[-1] == D and opponent.history[-1] == C:
                self.contrite = True

        return opponent.history[-1]

    def reset(self):
        Player.reset(self)
        self.contrite = False
        self._recorded_history = []


class SlowTitForTwoTats(Player):
    """
    A player plays C twice, then if the opponent plays the same move twice,
    plays that move.

    """

    name = 'Slow Tit For Two Tats'
    classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):

        # Start with two cooperations
        if len(self.history) < 2:
            return C

        # Mimic if opponent plays the same move twice
        if opponent.history[-2] == opponent.history[-1]:
            return opponent.history[-1]

        # Otherwise cooperate
        return C

class AdaptiveTitForTat(Player):
    """ATFT - Adaptive Tit For Tat (Basic Model)

    Algorithm

    if (opponent played C in the last cycle) then
    world = world + r*(1-world)
    else
    world = world + r*(0-world)
    If (world >= 0.5) play C, else play D

    Attributes

    world : float [0.0, 1.0], set to 0.5
        continuous variable representing the world's image
        1.0 - total cooperation
        0.0 - total defection
        other values - something in between of the above
        updated every round, starting value shouldn't matter as long as
        it's >= 0.5

    Parameters

    rate : float [0.0, 1.0], default=0.5
        adaptation rate - r in Algorithm above
        smaller value means more gradual and robust
        to perturbations behaviour

    Names:

    - Adaptive Tit For Tat: [Tzafestas2000]_
    """

    name = 'Adaptive Tit For Tat'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }
    world = 0.5

    @init_args
    def __init__(self, rate=0.5):

        Player.__init__(self)
        self.rate, self.starting_rate = rate, rate

    def strategy(self, opponent):

        if len(opponent.history) == 0:
            return C

        if opponent.history[-1] == C:
            self.world += self.rate * (1. - self.world)
        else:
            self.world -= self.rate * self.world

        if self.world >= 0.5:
            return C

        return D

    def reset(self):

        Player.reset(self)
        self.world = 0.5
        self.rate = self.starting_rate

    def __repr__(self):

        return "%s: %s" % (self.name, round(self.rate, 2))
