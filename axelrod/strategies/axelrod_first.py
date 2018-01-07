"""
Additional strategies from Axelrod's first tournament.
"""

import random

from axelrod.action import Action
from axelrod.player import Player
from axelrod.random_ import random_choice
from axelrod.strategy_transformers import FinalTransformer
from .memoryone import MemoryOnePlayer

from scipy.stats import chisquare

from typing import List, Dict, Tuple

C, D = Action.C, Action.D


class Davis(Player):
    """
    Submitted to Axelrod's first tournament by Morton Davis.

    A player starts by cooperating for 10 rounds then plays Grudger,
    defecting if at any point the opponent has defected.

    This strategy came 8th in Axelrod's original tournament.

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
    """This strategy attempts to estimate the next move of the opponent by estimating
    the probability of cooperating given that they defected (:math:`p(C|D)`) or
    cooperated on the previous round (:math:`p(C|C)`). These probabilities are
    continuously updated during play and the strategy attempts to maximise the long
    term play. Note that the initial values are :math:`p(C|C)=p(C|D)=.5`.

    Downing is implemented as `RevisedDowning`. Apparently in the first tournament
    the strategy was implemented incorrectly and defected on the first two rounds.
    This can be controlled by setting `revised=True` to prevent the initial defections.

    This strategy came 10th in Axelrod's original tournament but would have won
    if it had been implemented correctly.

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
        self.total_C = 0  # note the same as self.cooperations
        self.total_D = 0  # note the same as self.defections

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
            move = self.history[-1].flip()
        else:
            move = D
        return move


class Feld(Player):
    """
    Submitted to Axelrod's first tournament by Scott Feld.

    This strategy plays Tit For Tat, always defecting if the opponent defects but
    cooperating when the opponent cooperates with a gradually decreasing probability
    until it is only .5.

    This strategy came 11th in Axelrod's original tournament.

    Names:

    - Feld: [Axelrod1980]_
    """

    name = "Feld"
    classifier = {
        'memory_depth': 200,  # Varies actually, eventually becomes depth 1
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

    Cooperate on the first two rounds and
    returns the opponent's last action for the next 5. For the rest of the game
    Grofman cooperates if both players selected the same action in the previous
    round, and otherwise cooperates randomly with probability 2/7.

    This strategy came 4th in Axelrod's original tournament.

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

    This strategy came 12th in Axelrod's original tournament.

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

    .. math::

        A = 16 a_1 + 4 a_2 + a_3

    Where :math:`a_i` is dependent on the outcome of the previous :math:`i` th
    round.  If both strategies defect, :math:`a_i=3`, if the opponent only defects:
    :math:`a_i=2` and finally if it is only this strategy that defects then
    :math:`a_i=1`.

    Finally this strategy defects if and only if:

    .. math::

        A \in \{1, 6, 7, 17, 22, 23, 26, 29, 30, 31, 33, 38, 39, 45, 49, 54, 55, 58, 61\}

    Thus if all three preceding moves are mutual defection, A = 63 and the rule
    cooperates. This rule was designed for use in laboratory experiments as a
    stooge which had a memory and appeared to be trustworthy, potentially
    cooperative, but not gullible.

    This strategy came 3rd in Axelrod's original tournament.

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

    This strategy came 5th in Axelrod's original tournament.

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


class Tullock(Player):
    """
    Submitted to Axelrod's first tournament by Gordon Tullock.

    Cooperates for the first 11 rounds then randomly cooperates 10% less often
    than the opponent has in previous rounds.

    This strategy came 13th in Axelrod's original tournament.

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
    """This strategy plays a modification of Tit For Tat.

    1. It cooperates for the first 4 moves.
    2. It defects on the last 2 moves.
    3. Every 15 moves it makes use of a `chi-squared
       test <http://en.wikipedia.org/wiki/Chi-squared_test>`_ to check if the
       opponent is playing randomly.

    This strategy came 6th in Axelrod's original tournament.

    Names:

    - SteinAndRapoport: [Axelrod1980]_
    """

    name = 'Stein and Rapoport'
    classifier = {
        'memory_depth': float("inf"),
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
        alpha: float
            The significant level of p-value from chi-squared test with
            alpha == 0.05 by default.
        """
        super().__init__()
        self.alpha = alpha
        self.opponent_is_random = False

    def strategy(self, opponent: Player) -> Action:
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
        else:  # TitForTat if opponent plays not randomly
            return opponent.history[-1]


class TidemanAndChieruzzi(Player):
    """
    This strategy begins by playing Tit For Tat and then follows the following
    rules:

    1. Every run of defections played by the opponent increases the number of
    defections that this strategy retaliates with by 1.

    2. The opponent is given a ‘fresh start’ if:
        - it is 10 points behind this strategy
        - and it has not just started a run of defections
        - and it has been at least 20 rounds since the last ‘fresh start’
        - and there are more than 10 rounds remaining in the match
        - and the total number of defections differs from a 50-50 random sample
          by at least 3.0 standard deviations.

    A ‘fresh start’ is a sequence of two cooperations followed by an assumption
    that the game has just started (everything is forgotten).

    This strategy came 2nd in Axelrod’s original tournament.

    Names:

    - TidemanAndChieruzzi: [Axelrod1980]_
    """

    name = 'Tideman and Chieruzzi'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': {"game", "length"},
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
        self.current_score = 0
        self.opponent_score = 0
        self.last_fresh_start = 0
        self.fresh_start = False

    def _decrease_retaliation_counter(self):
        """Lower the remaining owed retaliation count and flip to non-retaliate
        if the count drops to zero."""
        if self.is_retaliating:
            self.retaliation_remaining -= 1
            if self.retaliation_remaining == 0:
                self.is_retaliating = False

    def _fresh_start(self):
        """Give the opponent a fresh start by forgetting the past"""
        self.is_retaliating = False
        self.retaliation_length = 0
        self.retaliation_remaining = 0

    def _score_last_round(self, opponent: Player):
        """Updates the scores for each player."""
        # Load the default game if not supplied by a tournament.
        game = self.match_attributes["game"]
        last_round = (self.history[-1], opponent.history[-1])
        scores = game.score(last_round)
        self.current_score += scores[0]
        self.opponent_score += scores[1]

    def strategy(self, opponent: Player) -> Action:
        if not opponent.history:
            return C

        # Calculate the scores.
        self._score_last_round(opponent)

        # Check if we have recently given the strategy a fresh start.
        if self.fresh_start:
            self.fresh_start = False
            return C  # Second cooperation

        # Check conditions to give opponent a fresh start.
        current_round = len(self.history) + 1
        if self.last_fresh_start == 0:
            valid_fresh_start = True
        # There needs to be at least 20 rounds before the next fresh start
        else:
            valid_fresh_start = current_round - self.last_fresh_start >= 20

        if valid_fresh_start:
            valid_points = self.current_score - self.opponent_score >= 10
            valid_rounds = self.match_attributes['length'] - current_round >= 10
            opponent_is_cooperating = opponent.history[-1] == C
            if valid_points and valid_rounds and opponent_is_cooperating:
                # 50-50 split is based off the binomial distribution.
                N = opponent.cooperations + opponent.defections
                # std_dev = sqrt(N*p*(1-p)) where p is 1 / 2.
                std_deviation = (N ** (1 / 2)) / 2
                lower = N / 2 - 3 * std_deviation
                upper = N / 2 + 3 * std_deviation
                if opponent.defections <= lower or opponent.defections >= upper:
                    # Opponent deserves a fresh start
                    self.last_fresh_start = current_round
                    self._fresh_start()
                    self.fresh_start = True
                    return C  # First cooperation

        if self.is_retaliating:
            # Are we retaliating still?
            self._decrease_retaliation_counter()
            return D

        if opponent.history[-1] == D:
            self.is_retaliating = True
            self.retaliation_length += 1
            self.retaliation_remaining = self.retaliation_length
            self._decrease_retaliation_counter()
            return D

        return C
