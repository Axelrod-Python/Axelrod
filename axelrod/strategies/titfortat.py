from axelrod.action import Action, actions_to_str
from axelrod.player import Player
from axelrod.random_ import random_choice
from axelrod.strategy_transformers import (
    TrackHistoryTransformer, FinalTransformer)

C, D = Action.C, Action.D


class TitForTat(Player):
    """
    A player starts by cooperating and then mimics the previous action of the
    opponent.

    This strategy was referred to as the *'simplest'* strategy submitted to
    Axelrod's first tournament. It came first.

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

    def strategy(self, opponent: Player) -> Action:
        """This is the actual strategy"""
        # First move
        if not self.history:
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
    - Slow tit for two tats: Original name by Ranjini Das
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
    def strategy(opponent: Player) -> Action:
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
    def strategy(opponent: Player) -> Action:
        return D if D in opponent.history[-2:] else C


class DynamicTwoTitsForTat(Player):
    """
    A player starts by cooperating and then punishes its opponent's
    defections with defections, but with a dynamic bias towards cooperating
    based on the opponent's ratio of cooperations to total moves
    (so their current probability of cooperating regardless of the
    opponent's move (aka: forgiveness)).

    Names:

     - Dynamic Two Tits For Tat: Original name by Grant Garrett-Grossman.
    """

    name = 'Dynamic Two Tits For Tat'
    classifier = {
        'memory_depth': float("inf"),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        # First move
        if not opponent.history:
            # Make sure we cooperate first turn
            return C
        if D in opponent.history[-2:]:
            # Probability of cooperating regardless
            return random_choice(opponent.cooperations / len(opponent.history))
        else:
            return C


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
    def strategy(opponent: Player) -> Action:
        return C if opponent.history[-1:] == [D] else D


class SneakyTitForTat(Player):
    """Tries defecting once and repents if punished.

    Names:

    - Sneaky Tit For Tat: Original name by Karol Langner
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

    def strategy(self, opponent: Player) -> Action:
        if len(self.history) < 2:
            return C
        if D not in opponent.history:
            return D
        if opponent.history[-1] == D and self.history[-2] == D:
            return C
        return opponent.history[-1]


class SuspiciousTitForTat(Player):
    """A variant of Tit For Tat that starts off with a defection.

    Names:

    - Suspicious Tit For Tat: [Hilbe2013]_
    - Mistrust: [Beaufils1997]_
    """

    name = "Suspicious Tit For Tat"
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
    def strategy(opponent: Player) -> Action:
        return C if opponent.history[-1:] == [C] else D


class AntiTitForTat(Player):
    """A strategy that plays the opposite of the opponents previous move.
    This is similar to Bully, except that the first move is cooperation.

    Names:

    - Anti Tit For Tat: [Hilbe2013]_
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
    def strategy(opponent: Player) -> Action:
        return D if opponent.history[-1:] == [C] else C


class HardTitForTat(Player):
    """A variant of Tit For Tat that uses a longer history for retaliation.

    Names:

    - Hard Tit For Tat: [PD2017]_
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
    def strategy(opponent: Player) -> Action:
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

    - Hard Tit For Two Tats: [Stewart2012]_
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
    def strategy(opponent: Player) -> Action:
        # Cooperate on the first move
        if not opponent.history:
            return C
        # Defects if two consecutive D in the opponent's last three moves
        history_string = actions_to_str(opponent.history[-3:])
        if 'DD' in history_string:
            return D
        # Otherwise cooperates
        return C


class OmegaTFT(Player):
    """OmegaTFT modifies Tit For Tat in two ways:
       - checks for deadlock loops of alternating rounds of (C, D) and (D, C),
       and attempting to break them
       - uses a more sophisticated retaliation mechanism that is noise tolerant

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

    def __init__(self, deadlock_threshold: int = 3, randomness_threshold: int = 8) -> None:
        super().__init__()
        self.deadlock_threshold = deadlock_threshold
        self.randomness_threshold = randomness_threshold
        self.randomness_counter = 0
        self.deadlock_counter = 0

    def strategy(self, opponent: Player) -> Action:
        # Cooperate on the first move
        if not self.history:
            return C
        # TFT on round 2
        if len(self.history) == 1:
            return opponent.history[-1]

        # Are we deadlocked? (in a CD -> DC loop)
        if self.deadlock_counter >= self.deadlock_threshold:
            move = C
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
            # If the opponent's last move differed from mine,
            # increase the counter
            if self.history[-1] != opponent.history[-1]:
                self.randomness_counter += 1
            # Compare counts to thresholds
            # If randomness_counter exceeds Y, Defect for the remainder
            if self.randomness_counter >= self.randomness_threshold:
                move = D
            else:
                # TFT
                move = opponent.history[-1]
                # Check for deadlock
                if opponent.history[-2] != opponent.history[-1]:
                    self.deadlock_counter += 1
                else:
                    self.deadlock_counter = 0
        return move



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

    def __init__(self) -> None:

        super().__init__()
        self.calming = False
        self.punishing = False
        self.punishment_count = 0
        self.punishment_limit = 0

    def strategy(self, opponent: Player) -> Action:

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

    def __init__(self):
        super().__init__()
        self.contrite = False
        self._recorded_history = []

    def strategy(self, opponent: Player) -> Action:

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

    def __init__(self, rate: float = 0.5) -> None:
        super().__init__()
        self.rate = rate
        self.world = rate

    def strategy(self, opponent: Player) -> Action:

        if len(opponent.history) == 0:
            return C

        if opponent.history[-1] == C:
            self.world += self.rate * (1. - self.world)
        else:
            self.world -= self.rate * self.world

        if self.world >= 0.5:
            return C

        return D


class SpitefulTitForTat(Player):
    """
    A player starts by cooperating and then mimics the previous action of the
    opponent until opponent defects twice in a row, at which point player
    always defects

    Names:

    - Spiteful Tit For Tat: [Prison1998]_
    """

    name = 'Spiteful Tit For Tat'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        self.retaliating = False

    def strategy(self, opponent: Player) -> Action:
        # First move
        if not self.history:
            return C

        if opponent.history[-2:] == [D, D]:
            self.retaliating = True

        if self.retaliating:
            return D
        else:
            # React to the opponent's last move
            if opponent.history[-1] == D:
                return D
            return C


class SlowTitForTwoTats2(Player):
    """
    A player plays C twice, then if the opponent plays the same move twice,
    plays that move, otherwise plays previous move.

    Names:

    - Slow Tit For Tat: [Prison1998]_
    """

    name = 'Slow Tit For Two Tats 2'
    classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:

        # Start with two cooperations
        if len(self.history) < 2:
            return C

        # Mimic if opponent plays the same move twice
        if opponent.history[-2] == opponent.history[-1]:
            return opponent.history[-1]

        # Otherwise play previous move
        return self.history[-1]


@FinalTransformer((D,), name_prefix=None)
class Alexei(Player):
    """
    Plays similar to Tit-for-Tat, but always defect on last turn.

    Names:

    - Alexei: [LessWrong2011]_
    """

    name = 'Alexei'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': {'length'},
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        if not self.history:
            return C
        if opponent.history[-1] == D:
            return D
        return C


@FinalTransformer((D,), name_prefix=None)
class EugineNier(Player):
    """
    Plays similar to Tit-for-Tat, but with two conditions:
    1) Always Defect on Last Move
    2) If other player defects five times, switch to all defects.

    Names:

    - Eugine Nier: [LessWrong2011]_
    """

    name = 'EugineNier'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': {'length'},
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        super().__init__()
        self.is_defector = False

    def strategy(self, opponent: Player) -> Action:
        if not self.history:
            return C
        if not (self.is_defector) and opponent.defections >= 5:
            self.is_defector = True
        if self.is_defector:
            return D
        return opponent.history[-1]


class NTitsForMTats(Player):
    """
    A parameterizable Tit-for-Tat,
    The arguments are:
    1) M: the number of defection before retaliation
    2) N: the number of retaliations

    Names:

    - N Tit(s) For M Tat(s): Original name by Marc Harper
    """

    name = 'N Tit(s) For M Tat(s)'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, N: int=3, M: int=2) -> None:
        """
        Parameters
        ----------
        N: int
            Number of retaliations
        M: int
            Number of defection before retaliation

        Special Cases
        -------------
        NTitsForMTats(1,1) is equivalent to TitForTat
        NTitsForMTats(1,2) is equivalent to TitFor2Tats
        NTitsForMTats(2,1) is equivalent to TwoTitsForTat
        NTitsForMTats(0,*) is equivalent to Cooperator
        NTitsForMTats(*,0) is equivalent to Defector
        """
        super().__init__()
        self.N = N
        self.M = M
        self.classifier['memory_depth'] = max([M, N])
        self.retaliate_count = 0

    def strategy(self, opponent: Player) -> Action:
        # if opponent defected consecutively M times, start the retaliation
        if not self.M or opponent.history[-self.M:].count(D) == self.M:
            self.retaliate_count = self.N
        if self.retaliate_count:
            self.retaliate_count -= 1
            return D
        return C


@FinalTransformer((D,), name_prefix=None)
class Michaelos(Player):
    """
    Plays similar to Tit-for-Tat with two exceptions:
    1) Defect on last turn.
    2) After own defection and opponent's cooperation, 50 percent of the time,
    cooperate. The other 50 percent of the time, always defect for the rest of
    the game.

    Names:

    - Michaelos: [LessWrong2011]_
    """

    name = 'Michaelos'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': {'length'},
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        super().__init__()
        self.is_defector = False

    def strategy(self, opponent: Player) -> Action:
        if not self.history:
            return C
        if self.is_defector:
            return D
        if self.history[-1] == D and opponent.history[-1] == C:
            decision = random_choice()
            if decision == C:
                return C
            else:
                self.is_defector = True
                return D

        return opponent.history[-1]


class RandomTitForTat(Player):
    """
    A player starts by cooperating and then follows by copying its
    opponent (tit for tat style).  From then on the player
    will switch between copying its opponent and randomly
    responding every other iteration.

    Name:

    - Random TitForTat: Original name by Zachary M. Taylor
    """

    # These are various properties for the strategy
    name = 'Random Tit for Tat'
    classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }


    def __init__(self, p: float=0.5) -> None:
        """
        Parameters
        ----------
        p, float
            The probability to cooperate
        """
        super().__init__()
        self.p = p
        self.act_random = False
        if p in [0, 1]:
            self.classifier['stochastic'] = False


    def strategy(self, opponent: Player) -> Action:
        """This is the actual strategy"""
        if not self.history:
            return C

        if self.act_random:
            self.act_random = False
            return random_choice(self.p)

        self.act_random = True
        return opponent.history[-1]
