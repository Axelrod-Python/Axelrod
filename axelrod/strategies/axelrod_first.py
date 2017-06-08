"""
Additional strategies from Axelrod's first tournament.
"""

import random

from axelrod.actions import Actions, flip_action, Action
from axelrod.player import Player
from axelrod.random_ import random_choice
from axelrod.strategy_transformers import FinalTransformer
from .memoryone import MemoryOnePlayer

from scipy.stats import chisquare

from typing import List, Dict, Tuple

C, D = Actions.C, Actions.D


class Davis(Player):
    """
    Submitted to Axelrod's first tournament by Morton Davis.

    A player starts by cooperating for 10 rounds then plays Grudger,
    defecting if at any point the opponent has defected.

    Names:

    - Davis: [Axelrod1980]_
    """

    name = 'Davis'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, rounds_to_cooperate: int = 10) -> None:
        """
        Parameters
        ----------
        rounds_to_cooperate: int, 10
           The number of rounds to cooperate initially
        """
        super().__init__()
        self._rounds_to_cooperate = rounds_to_cooperate

    def strategy(self, opponent: Player) -> Action:
        """Begins by playing C, then plays D for the remaining rounds if the
        opponent ever plays D."""
        if len(self.history) < self._rounds_to_cooperate:
            return C
        if opponent.defections:
            return D
        return C


class RevisedDowning(Player):
    """Revised Downing attempts to determine if players are cooperative or not.
    If so, it cooperates with them. This strategy would have won Axelrod's first
    tournament.

    Names:

    - Revised Downing: [Axelrod1980]_
    """

    name = "Revised Downing"

    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, revised: bool = True) -> None:
        super().__init__()
        self.revised = revised
        self.good = 1.0
        self.bad = 0.0
        self.nice1 = 0
        self.nice2 = 0
        self.total_C = 0 # note the same as self.cooperations
        self.total_D = 0 # note the same as self.defections

    def strategy(self, opponent: Player) -> Action:
        round_number = len(self.history) + 1
        # According to internet sources, the original implementation defected
        # on the first two moves. Otherwise it wins (if this code is removed
        # and the comment restored.
        # http://www.sci.brooklyn.cuny.edu/~sklar/teaching/f05/alife/notes/azhar-ipd-Oct19th.pdf

        if self.revised:
            if round_number == 1:
                return C
        elif not self.revised:
            if round_number <= 2:
                return D

        # Update various counts
        if round_number > 2:
            if self.history[-1] == D:
                if opponent.history[-1] == C:
                    self.nice2 += 1
                self.total_D += 1
                self.bad = self.nice2 / self.total_D
            else:
                if opponent.history[-1] == C:
                    self.nice1 += 1
                self.total_C += 1
                self.good = self.nice1 / self.total_C
        # Make a decision based on the accrued counts
        c = 6.0 * self.good - 8.0 * self.bad - 2
        alt = 4.0 * self.good - 5.0 * self.bad - 1
        if (c >= 0 and c >= alt):
            move = C
        elif (c >= 0 and c < alt) or (alt >= 0):
            move = flip_action(self.history[-1])
        else:
            move = D
        return move

    def reset(self):
        super().reset()
        self.good = 1.0
        self.bad = 0.0
        self.nice1 = 0
        self.nice2 = 0
        self.total_C = 0 # not the same as self.cooperations
        self.total_D = 0 # not the same as self.defections


class Feld(Player):
    """
    Submitted to Axelrod's first tournament by Scott Feld.

    Defects when opponent defects. Cooperates with a probability that decreases
    to 0.5 at round 200.

    Names:

    - Feld: [Axelrod1980]_
    """

    name = "Feld"
    classifier = {
        'memory_depth': 200, # Varies actually, eventually becomes depth 1
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, start_coop_prob: float = 1.0, end_coop_prob: float = 0.5,
                 rounds_of_decay: int = 200) -> None:
        """
        Parameters
        ----------
        start_coop_prob, float
            The initial probability to cooperate
        end_coop_prob, float
            The final probability to cooperate
        rounds_of_decay, int
            The number of rounds to linearly decrease from start_coop_prob
            to end_coop_prob
        """
        super().__init__()
        self._start_coop_prob = start_coop_prob
        self._end_coop_prob = end_coop_prob
        self._rounds_of_decay = rounds_of_decay

    def _cooperation_probability(self) -> float:
        """It's not clear what the interpolating function is, so we'll do
        something simple that decreases monotonically from 1.0 to 0.5 over
        200 rounds."""
        diff = (self._end_coop_prob - self._start_coop_prob)
        slope = diff / self._rounds_of_decay
        rounds = len(self.history)
        return max(self._start_coop_prob + slope * rounds,
                   self._end_coop_prob)

    def strategy(self, opponent: Player) -> Action:
        if not opponent.history:
            return C
        if opponent.history[-1] == D:
            return D
        p = self._cooperation_probability()
        return random_choice(p)


class Grofman(Player):
    """
    Submitted to Axelrod's first tournament by Bernard Grofman.

    Cooperate on the first 2 moves. Return opponent's move for the next 5.
    Then cooperate if the last round's moves were the same, otherwise cooperate
    with probability 2/7.

    Names:

    - Grofman: [Axelrod1980]_
    """

    name = "Grofman"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        round_number = len(self.history) + 1
        if round_number < 3:
            return C
        if round_number < 8:
            return opponent.history[-1]
        if self.history[-1] == opponent.history[-1]:
            return C
        return random_choice(2 / 7)



class Joss(MemoryOnePlayer):
    """
    Submitted to Axelrod's first tournament by Johann Joss.

    Cooperates with probability 0.9 when the opponent cooperates, otherwise
    emulates Tit-For-Tat.

    Names:

    - Joss: [Axelrod1980]_
    - Hard Joss: [Stewart2012]_
    """

    name = "Joss"

    def __init__(self, p: float = 0.9) -> None:
        """
        Parameters
        ----------
        p, float
            The probability of cooperating when the previous round was (C, C)
            or (D, C), i.e. the opponent cooperated.
        """
        four_vector = (p, 0, p, 0)
        self.p = p
        super().__init__(four_vector)


class Nydegger(Player):
    """
    Submitted to Axelrod's first tournament by Rudy Nydegger.

    The program begins with tit for tat for the first three moves, except
    that if it was the only one to cooperate on the first move and the only one
    to defect on the second move, it defects on the third move. After the
    third move, its choice is determined from the 3 preceding outcomes in the
    following manner.

    Let A be the sum formed by counting the other's defection as 2 points and
    one's own as 1 point, and giving weights of 16, 4, and 1 to the preceding
    three moves in chronological order. The choice can be described as defecting
    only when A equals
    1, 6, 7, 17, 22, 23, 26, 29, 30, 31, 33, 38, 39, 45, 49, 54, 55, 58, or 61.

    Thus if all three preceding moves are mutual defection, A = 63 and the rule
    cooperates. This rule was designed for use in laboratory experiments as a
    stooge which had a memory and appeared to be trustworthy, potentially
    cooperative, but not gullible.

    Names:

    - Nydegger: [Axelrod1980]_
    """

    name = "Nydegger"
    classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        self.As = [1, 6, 7, 17, 22, 23, 26, 29, 30, 31, 33, 38, 39, 45, 54, 55,
                   58, 61]
        self.score_map = {(C, C): 0,
                          (C, D): 2,
                          (D, C): 1,
                          (D, D): 3}
        super().__init__()

    @staticmethod
    def score_history(my_history: List[Action], opponent_history: List[Action],
        score_map: Dict[Tuple[Action, Action], int]) -> int:

        """Implements the Nydegger formula A = 16 a_1 + 4 a_2 + a_3"""
        a = 0
        for i, weight in [(-1, 16), (-2, 4), (-3, 1)]:
            plays = (my_history[i], opponent_history[i])
            a += weight * score_map[plays]
        return a

    def strategy(self, opponent: Player) -> Action:
        if len(self.history) == 0:
            return C
        if len(self.history) == 1:
            # TFT
            return D if opponent.history[-1] == D else C
        if len(self.history) == 2:
            if opponent.history[0: 2] == [D, C]:
                return D
            else:
                # TFT
                return D if opponent.history[-1] == D else C
        A = self.score_history(self.history[-3:], opponent.history[-3:],
                               self.score_map)
        if A in self.As:
            return D
        return C


class Shubik(Player):
    """
    Submitted to Axelrod's first tournament by Martin Shubik.

    Plays like Tit-For-Tat with the following modification. After each
    retaliation, the number of rounds that Shubik retaliates increases by 1.

    Names:

    - Shubik: [Axelrod1980]_
    """

    name = 'Shubik'
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
        self.is_retaliating = False
        self.retaliation_length = 0
        self.retaliation_remaining = 0

    def _decrease_retaliation_counter(self):
        """Lower the remaining owed retaliation count and flip to non-retaliate
        if the count drops to zero."""
        if self.is_retaliating:
            self.retaliation_remaining -= 1
            if self.retaliation_remaining == 0:
                self.is_retaliating = False

    def strategy(self, opponent: Player) -> Action:
        if not opponent.history:
            return C
        if opponent.history[-1] == D:
            # Retaliate against defections
            if self.history[-1] == C: # it's on now!
                # Lengthen the retaliation period
                self.is_retaliating = True
                self.retaliation_length += 1
                self.retaliation_remaining = self.retaliation_length
                self._decrease_retaliation_counter()
                return D
            else:
                # Just retaliate
                if self.is_retaliating:
                    self._decrease_retaliation_counter()
                return D
        if self.is_retaliating:
            # Are we retaliating still?
            self._decrease_retaliation_counter()
            return D
        return C

    def reset(self):
        super().reset()
        self.is_retaliating = False
        self.retaliation_length = 0
        self.retaliation_remaining = 0


class Tullock(Player):
    """
    Submitted to Axelrod's first tournament by Gordon Tullock.

    Cooperates for the first 11 rounds then randomly cooperates 10% less often
    than the opponent has in previous rounds.

    Names:

    - Tullock: [Axelrod1980]_
    """

    name = "Tullock"
    classifier = {
        'memory_depth': 11, # long memory, modified by init
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, rounds_to_cooperate: int = 11) -> None:
        """
        Parameters
        ----------
        rounds_to_cooperate: int, 10
           The number of rounds to cooperate initially
        """
        super().__init__()
        self._rounds_to_cooperate = rounds_to_cooperate
        self.memory_depth = rounds_to_cooperate

    def strategy(self, opponent: Player) -> Action:
        rounds = self._rounds_to_cooperate
        if len(self.history) < rounds:
            return C
        cooperate_count = opponent.history[-rounds:].count(C)
        prop_cooperate = cooperate_count / rounds
        prob_cooperate = max(0, prop_cooperate - 0.10)
        return random_choice(prob_cooperate)


class UnnamedStrategy(Player):
    """Apparently written by a grad student in political science whose name was
    withheld, this strategy cooperates with a given probability P. This
    probability (which has initial value .3) is updated every 10 rounds based on
    whether the opponent seems to be random, very cooperative or very
    uncooperative. Furthermore, if after round 130 the strategy is losing then P
    is also adjusted.

    Fourteenth Place with 282.2 points is a 77-line program by a graduate
    student of political science whose dissertation is in game theory. This rule
    has a probability of cooperating, P, which is initially 30% and is updated
    every 10 moves. P is adjusted if the other player seems random, very
    cooperative, or very uncooperative. P is also adjusted after move 130 if the
    rule has a lower score than the other player. Unfortunately, the complex
    process of adjustment frequently left the probability of cooperation in the
    30% to 70% range, and therefore the rule appeared random to many other players.

    Names:

    - Unnamed Strategy: [Axelrod1980]_

    Warning: This strategy is not identical to the original strategy (source
    unavailable) and was written based on published descriptions.
    """

    name = "Unnamed Strategy"
    classifier = {
        'memory_depth': 0,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        r = random.uniform(3, 7) / 10
        return random_choice(r)

@FinalTransformer((D, D), name_prefix=None)
class SteinAndRapoport(Player):
    """
    A player who plays according to statistic methods.
    Begins by playing C for the first four (4) rounds, then it plays
    tit for tat and at the last 2 round it Defects. Every 15 turns it
    runs a chi-squared test to check whether the opponent behaves randomly
    or not. In case the opponent behaves randomly then Stein and Rapoport
    Defects until the next 15 round (where we check again), otherwise it
    still plays TitForTat.0

    Names:

    - SteinAndRapoport: [Axelrod1980]_
    """

    name = 'Stein and Rapoport'
    classifier = {
        'memory_depth': 15,
        'stochastic': False,
        'makes_use_of': {"length"},
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, alpha: float=0.05) -> None:
        """
        Parameters
        ----------
        alpha, float
            The significant level of pvalue from chi-squared test
            0.05 by default according to literature
        """
        super().__init__()
        self.alpha = alpha
        self.opponent_is_random = None

    def strategy(self , opponent: Player) -> Action:
        round_number = len(self.history) + 1

        # First 4 moves
        if round_number < 5:
            return C
        # For first 15 rounds tit for tat as we do not know opponents strategy
        elif round_number < 15:
            return opponent.history[-1]

        if round_number % 15 == 0:
            p_value = chisquare([opponent.cooperations,
                                 opponent.defections]).pvalue
            self.opponent_is_random = p_value >= self.alpha

        if self.opponent_is_random:
            # Defect if opponent plays randomly
            return D
        else: # TitForTatat if opponent plays not randomly
            return opponent.history[-1]

    def reset(self):
        super().reset()
        self.random_opponent = None
