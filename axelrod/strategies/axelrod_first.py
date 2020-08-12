"""
Strategies submitted to Axelrod's first tournament. All strategies in this
module are prefixed by `FirstBy` to indicate that they were submitted in
Axelrod's First tournament by the given author.

Note that these strategies are implemented from the descriptions presented
in:

Axelrod, R. (1980). Effective Choice in the Prisoner’s Dilemma.
Journal of Conflict Resolution, 24(1), 3–25.

These descriptions are not always clear and/or precise and when assumptions have
been made they are explained in the strategy docstrings.
"""

from typing import Dict, List, Optional, Tuple

from axelrod.action import Action
from axelrod.player import Player
from axelrod.strategy_transformers import FinalTransformer
from scipy.stats import chisquare

from .memoryone import MemoryOnePlayer

C, D = Action.C, Action.D


class FirstByDavis(Player):
    """
    Submitted to Axelrod's first tournament by Morton Davis.

    The description written in [Axelrod1980]_ is:

    > "A player starts by cooperating for 10 rounds then plays Grudger,
    > defecting if at any point the opponent has defected."

    This strategy came 8th in Axelrod's original tournament.

    Names:

    - Davis: [Axelrod1980]_
    """

    name = "First by Davis"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
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
        if opponent.defections > 0:  # Implement Grudger
            return D
        return C


class FirstByDowning(Player):
    """
    Submitted to Axelrod's first tournament by Downing

    The description written in [Axelrod1980]_ is:

    > "This rule selects its choice to maximize its own longterm expected payoff on
    > the assumption that the other rule cooperates with a fixed probability which
    > depends only on whether the other player cooperated or defected on the previous
    > move. These two probabilities estimates are continuously updated as the game
    > progresses. Initially, they are both assumed to be .5, which amounts to the
    > pessimistic assumption that the other player is not responsive. This rule is
    > based on an outcome maximization interpretation of human performances proposed
    > by Downing (1975)."

    The Downing (1975) paper is "The Prisoner's Dilemma Game as a
    Problem-Solving Phenomenon" [Downing1975]_ and this is used to implement the
    strategy.

    There are a number of specific points in this paper, on page 371:

    > "[...] In these strategies, O's [the opponent's] response on trial N is in
    some way dependent or contingent on S's [the subject's] response on trial N-
    1. All varieties of these lag-one matching strategies can be defined by two
    parameters: the conditional probability that O will choose C following C by
    S, P(C_o | C_s) and the conditional probability that O will choose C
    following D by S, P(C_o, D_s)."

    Throughout the paper the strategy (S) assumes that the opponent (O) is
    playing a reactive strategy defined by these two conditional probabilities.

    The strategy aims to maximise the long run utility against such a strategy
    and the mechanism for this is described in Appendix A (more on this later).

    One final point from the main text is, on page 372:

    > "For the various lag-one matching strategies of O, the maximizing
    strategies of S will be 100% C, or 100% D, or for some strategies all S
    strategies will be functionally equivalent."

    This implies that the strategy S will either always cooperate or always
    defect (or be indifferent) dependent on the opponent's defining
    probabilities.

    To understand the particular mechanism that describes the strategy S, we
    refer to Appendix A of the paper on page 389.

    The stated goal of the strategy is to maximize (using the notation of the
    paper):

        EV_TOT = #CC(EV_CC) + #CD(EV_CD) + #DC(EV_DC) + #DD(EV_DD)

    This differs from the more modern literature where #CC, #CD, #DC and #DD
    would imply that counts of both players playing C and C, or the first
    playing C and the second D etc...
    In this case the author uses an argument based on the sequence of plays by
    the player (S) so #CC denotes the number of times the player plays C twice
    in a row.

    On the second page of the appendix, figure 4 (page 390)
    identifies an expression for EV_TOT.
    A specific term is made to disappear in
    the case of T - R = P - S (which is not the case for the standard
    (R, P, S, T) = (3, 1, 0, 5)):

    > "Where (t - r) = (p - s), EV_TOT will be a function of alpha, beta, t, r,
    p, s and N are known and V which is unknown.

    V is the total number of cooperations of the player S (this is noted earlier
    in the abstract) and as such the final expression (with only V as unknown)
    can be used to decide if V should indicate that S always cooperates or not.

    This final expression is used to show that EV_TOT is linear in the number of
    cooperations by the player thus justifying the fact that the player will
    always cooperate or defect.

    All of the above details are used to give the following interpretation of
    the strategy:

    1. On any given turn, the strategy will estimate alpha = P(C_o | C_s) and
    beta = P(C_o | D_s).
    2. The strategy will calculate the expected utility of always playing C OR
    always playing D against the estimated probabilities. This corresponds to:

        a. In the case of the player always cooperating:

           P_CC = alpha and P_CD = 1 - alpha

        b. In the case of the player always defecting:

           P_DC = beta and P_DD = 1 - beta


    Using this we have:

        E_C = alpha R + (1 - alpha) S
        E_D = beta T + (1 - beta) P

    Thus at every turn, the strategy will calculate those two values and
    cooperate if E_C > E_D and will defect if E_C < E_D.

    In the case of E_C = E_D, the player will alternate from their previous
    move. This is based on specific sentence from Axelrod's original paper:

    > "Under certain circumstances, DOWNING will even determine that the best
    > strategy is to alternate cooperation and defection."

    One final important point is the early game behaviour of the strategy. It
    has been noted that this strategy was implemented in a way that assumed that
    alpha and beta were both 1/2:

    > "Initially, they are both assumed to be .5, which amounts to the
    > pessimistic assumption that the other player is not responsive."

    Note that if alpha = beta = 1 / 2 then:

        E_C = alpha R + alpha S
        E_D = alpha T + alpha P

    And from the defining properties of the Prisoner's Dilemma (T > R > P > S)
    this gives: E_D > E_C.
    Thus, the player opens with a defection in the first two rounds. Note that
    from the Axelrod publications alone there is nothing to indicate defections
    on the first two rounds, although a defection in the opening round is clear.
    However there is a presentation available at
    http://www.sci.brooklyn.cuny.edu/~sklar/teaching/f05/alife/notes/azhar-ipd-Oct19th.pdf
    That clearly states that Downing defected in the first two rounds, thus this
    is assumed to be the behaviour. Interestingly, in future tournaments this
    strategy was revised to not defect on the opening two rounds.

    It is assumed that these first two rounds are used to create initial
    estimates of
    beta = P(C_o | D_s) and we will use the opening play of the player to
    estimate alpha = P(C_o | C_s).
    Thus we assume that the opponents first play is a response to a cooperation
    "before the match starts".

    So for example, if the plays are:

    [(D, C), (D, C)]

    Then the opponent's first cooperation counts as a cooperation in response to
    the non existent cooperation of round 0. The total number of cooperations in
    response to a cooperation is 1. We need to take in to account that extra
    phantom cooperation to estimate the probability alpha=P(C_o | C_s) as 1 / 1
    = 1.

    This is an assumption with no clear indication from the literature.

    --
    This strategy came 10th in Axelrod's original tournament.

    Names:

    - Downing: [Axelrod1980]_
    """

    name = "First by Downing"

    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        super().__init__()
        self.number_opponent_cooperations_in_response_to_C = 0
        self.number_opponent_cooperations_in_response_to_D = 0

    def strategy(self, opponent: Player) -> Action:
        round_number = len(self.history) + 1

        if round_number == 1:
            return D
        if round_number == 2:
            if opponent.history[-1] == C:
                self.number_opponent_cooperations_in_response_to_C += 1
            return D

        if self.history[-2] == C and opponent.history[-1] == C:
            self.number_opponent_cooperations_in_response_to_C += 1
        if self.history[-2] == D and opponent.history[-1] == C:
            self.number_opponent_cooperations_in_response_to_D += 1

        # Adding 1 to cooperations for assumption that first opponent move
        # being a response to a cooperation. See docstring for more
        # information.
        alpha = (self.number_opponent_cooperations_in_response_to_C /
                 (self.cooperations + 1))
        # Adding 2 to defections on the assumption that the first two
        # moves are defections, which may not be true in a noisy match
        beta = (self.number_opponent_cooperations_in_response_to_D /
                 max(self.defections, 2))

        R, P, S, T = self.match_attributes["game"].RPST()
        expected_value_of_cooperating = alpha * R + (1 - alpha) * S
        expected_value_of_defecting = beta * T + (1 - beta) * P

        if expected_value_of_cooperating > expected_value_of_defecting:
            return C
        if expected_value_of_cooperating < expected_value_of_defecting:
            return D
        return self.history[-1].flip()


class FirstByFeld(Player):
    """
    Submitted to Axelrod's first tournament by Scott Feld.

    The description written in [Axelrod1980]_ is:

    > "This rule starts with tit for tat and gradually lowers its probability of
    > cooperation following the other's cooperation to .5 by the two hundredth
    > move. It always defects after a defection by the other."

    This strategy plays Tit For Tat, always defecting if the opponent defects but
    cooperating when the opponent cooperates with a gradually decreasing probability
    until it is only .5. Note that the description does not clearly indicate how
    the cooperation probability should drop. This implements a linear decreasing
    function.

    This strategy came 11th in Axelrod's original tournament.

    Names:

    - Feld: [Axelrod1980]_
    """

    name = "First by Feld"
    classifier = {
        "memory_depth": 200,  # Varies actually, eventually becomes depth 1
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(
        self,
        start_coop_prob: float = 1.0,
        end_coop_prob: float = 0.5,
        rounds_of_decay: int = 200,
    ) -> None:
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
        diff = self._end_coop_prob - self._start_coop_prob
        slope = diff / self._rounds_of_decay
        rounds = len(self.history)
        return max(self._start_coop_prob + slope * rounds, self._end_coop_prob)

    def strategy(self, opponent: Player) -> Action:
        if not opponent.history:
            return C
        if opponent.history[-1] == D:
            return D
        p = self._cooperation_probability()
        return self._random.random_choice(p)


class FirstByGraaskamp(Player):
    """
    Submitted to Axelrod's first tournament by James Graaskamp.

    The description written in [Axelrod1980]_ is:

    > "This rule plays tit for tat for 50 moves, defects on move 51, and then
    > plays 5 more moves of tit for tat. A check is then made to see if the player
    > seems to be RANDOM, in which case it defects from then on. A check is also
    > made to see if the other is TIT FOR TAT, ANALOGY (a program from the
    > preliminary tournament), and its own twin, in which case it plays tit for
    > tat. Otherwise it randomly defects every 5 to 15 moves, hoping that enough
    > trust has been built up so that the other player will not notice these
    > defections.:

    This is implemented as:

    1. Plays Tit For Tat for the first 50 rounds;
    2. Defects on round 51;
    3. Plays 5 further rounds of Tit For Tat;
    4. A check is then made to see if the opponent is playing randomly in which
       case it defects for the rest of the game. This is implemented with a chi
       squared test.
    5. The strategy also checks to see if the opponent is playing Tit For Tat or
       a clone of itself. If
       so it plays Tit For Tat. If not it cooperates and randomly defects every 5
       to 15 moves.

    Note that there is no information about 'Analogy' available thus Step 5 is
    a "best possible" interpretation of the description in the paper.
    Furthermore the test for the clone is implemented as checking that both
    players have played the same moves for the entire game. This is unlikely to
    be the original approach but no further details are available.

    This strategy came 9th in Axelrod’s original tournament.

    Names:

    - Graaskamp: [Axelrod1980]_
    """

    name = "First by Graaskamp"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, alpha: float = 0.05) -> None:
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
        self.next_random_defection_turn = None  # type: Optional[int]

    def strategy(self, opponent: Player) -> Action:
        """This is the actual strategy"""
        # First move
        if not self.history:
            return C
        # React to the opponent's last move
        if len(self.history) < 56:
            if opponent.history[-1] == D or len(self.history) == 50:
                return D
            return C

        # Check if opponent plays randomly, if so, defect for the rest of the game
        p_value = chisquare([opponent.cooperations, opponent.defections]).pvalue
        self.opponent_is_random = (p_value >= self.alpha) or self.opponent_is_random

        if self.opponent_is_random:
            return D
        if all(
            opponent.history[i] == self.history[i - 1]
            for i in range(1, len(self.history))
        ) or opponent.history == self.history:
            # Check if opponent plays Tit for Tat or a clone of itself.
            if opponent.history[-1] == D:
                return D
            return C

        if self.next_random_defection_turn is None:
            self.next_random_defection_turn = self._random.randint(5, 15) + len(self.history)

        if len(self.history) == self.next_random_defection_turn:
            # resample the next defection turn
            self.next_random_defection_turn = self._random.randint(5, 15) + len(self.history)
            return D
        return C


class FirstByGrofman(Player):
    """
    Submitted to Axelrod's first tournament by Bernard Grofman.

    The description written in [Axelrod1980]_ is:

     > "If the players did different things on the previous move, this rule
     > cooperates with probability 2/7. Otherwise this rule always cooperates."

    This strategy came 4th in Axelrod's original tournament.

    Names:

    - Grofman: [Axelrod1980]_
    """

    name = "First by Grofman"
    classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        if len(self.history) == 0 or self.history[-1] == opponent.history[-1]:
            return C
        return self._random.random_choice(2 / 7)


class FirstByJoss(MemoryOnePlayer):
    """
    Submitted to Axelrod's first tournament by Johann Joss.

    The description written in [Axelrod1980]_ is:

    > "This rule cooperates 90% of the time after a cooperation by the other. It
    > always defects after a defection by the other."

    This strategy came 12th in Axelrod's original tournament.

    Names:

    - Joss: [Axelrod1980]_
    - Hard Joss: [Stewart2012]_
    """

    name = "First by Joss"

    def __init__(self, p: float = 0.9) -> None:
        """
        Parameters
        ----------
        p, float
            The probability of cooperating when the previous round was (C, C)
            or (D, C), i.e. the opponent cooperated.
        """
        four_vector = (p, 0, p, 0)
        super().__init__(four_vector)


class FirstByNydegger(Player):
    """
    Submitted to Axelrod's first tournament by Rudy Nydegger.

    The description written in [Axelrod1980]_ is:

    > "The program begins with tit for tat for the first three moves, except
    > that if it was the only one to cooperate on the first move and the only one
    > to defect on the second move, it defects on the third move. After the third
    > move, its choice is determined from the 3 preceding outcomes in the
    > following manner. Let A be the sum formed by counting the other's defection
    > as 2 points and one's own as 1 point, and giving weights of 16, 4, and 1 to
    > the preceding three moves in chronological order. The choice can be
    > described as defecting only when A equals 1, 6, 7, 17, 22, 23, 26, 29, 30,
    > 31, 33, 38, 39, 45, 49, 54, 55, 58, or 61. Thus if all three preceding moves
    > are mutual defection, A = 63 and the rule cooperates.  This rule was
    > designed for use in laboratory experiments as a stooge which had a memory
    > and appeared to be trustworthy, potentially cooperative, but not gullible
    > (Nydegger, 1978)."

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

    name = "First by Nydegger"
    classifier = {
        "memory_depth": 3,
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        self.As = [1, 6, 7, 17, 22, 23, 26, 29, 30, 31, 33, 38, 39, 45, 49, 54, 55, 58, 61]
        self.score_map = {(C, C): 0, (C, D): 2, (D, C): 1, (D, D): 3}
        super().__init__()

    @staticmethod
    def score_history(
        my_history: List[Action],
        opponent_history: List[Action],
        score_map: Dict[Tuple[Action, Action], int],
    ) -> int:

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
            if opponent.history[0:2] == [D, C]:
                return D
            else:
                # TFT
                return D if opponent.history[-1] == D else C
        A = self.score_history(self.history[-3:], opponent.history[-3:], self.score_map)
        if A in self.As:
            return D
        return C


class FirstByShubik(Player):
    """
    Submitted to Axelrod's first tournament by Martin Shubik.

    The description written in [Axelrod1980]_ is:

    > "This rule cooperates until the other defects, and then defects once. If
    > the other defects again after the rule's cooperation is resumed, the rule
    > defects twice. In general, the length of retaliation is increased by one for
    > each departure from mutual cooperation. This rule is described with its
    > strategic implications in Shubik (1970). Further treatment of its is given
    > in Taylor (1976).

    There is some room for interpretation as to how the strategy reacts to a
    defection on the turn where it starts to cooperate once more. In Shubik
    (1970) the strategy is described as:

    > "I will play my move 1 to begin with and will continue to do so, so long
    > as my information shows that the other player has chosen his move 1. If my
    > information tells me he has used move 2, then I will use move 2 for the
    > immediate k subsequent periods, after which I will resume using move 1. If
    > he uses his move 2 again after I have resumed using move 1, then I will
    > switch to move 2 for the k + 1 immediately subsequent periods . . . and so
    > on, increasing my retaliation by an extra period for each departure from the
    > (1, 1) steady state."

    This is interpreted as:

    The player cooperates, if when it is cooperating, the opponent defects it
    defects for k rounds. After k rounds it starts cooperating again and
    increments the value of k if the opponent defects again.

    This strategy came 5th in Axelrod's original tournament.

    Names:

    - Shubik: [Axelrod1980]_
    """

    name = "First by Shubik"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
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

        if self.is_retaliating:
            # Are we retaliating still?
            self._decrease_retaliation_counter()
            return D

        if opponent.history[-1] == D and self.history[-1] == C:
            # "If he uses his move 2 again after I have resumed using move 1,
            # then I will switch to move 2 for the k + 1 immediately subsequent
            # periods"
            self.is_retaliating = True
            self.retaliation_length += 1
            self.retaliation_remaining = self.retaliation_length
            self._decrease_retaliation_counter()
            return D
        return C


class FirstByTullock(Player):
    """
    Submitted to Axelrod's first tournament by Gordon Tullock.

    The description written in [Axelrod1980]_ is:

    > "This rule cooperates on the first eleven moves. It then cooperates 10%
    > less than the other player has cooperated on the preceding ten moves. This
    > rule is based on an idea developed in Overcast and Tullock (1971). Professor
    > Tullock was invited to specify how the idea could be implemented, and he did
    > so out of scientific interest rather than an expectation that it would be a
    > likely winner."

    This is interpreted as:

    Cooperates for the first 11 rounds then randomly cooperates 10% less often
    than the opponent has in the previous 10 rounds.

    This strategy came 13th in Axelrod's original tournament.

    Names:

    - Tullock: [Axelrod1980]_
    """

    name = "First by Tullock"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        super().__init__()
        self._rounds_to_cooperate = 11

    def strategy(self, opponent: Player) -> Action:
        if len(self.history) < self._rounds_to_cooperate:
            return C
        rounds = self._rounds_to_cooperate - 1
        cooperate_count = opponent.history[-rounds:].count(C)
        prop_cooperate = cooperate_count / rounds
        prob_cooperate = max(0, prop_cooperate - 0.10)
        return self._random.random_choice(prob_cooperate)


class FirstByAnonymous(Player):
    """
    Submitted to Axelrod's first tournament by a graduate student whose name was
    withheld.

    The description written in [Axelrod1980]_ is:

    > "This rule has a probability of cooperating, P, which is initially 30% and
    > is updated every 10 moves. P is adjusted if the other player seems random,
    > very cooperative, or very uncooperative. P is also adjusted after move 130
    > if the rule has a lower score than the other player. Unfortunately, the
    > complex process of adjustment frequently left the probability of cooperation
    > in the 30% to 70% range, and therefore the rule appeared random to many
    > other players."

    Given the lack of detail this strategy is implemented based on the final
    sentence of the description which is to have a cooperation probability that
    is uniformly random in the 30 to 70% range.

    Names:

    - (Name withheld): [Axelrod1980]_
    """

    name = "First by Anonymous"
    classifier = {
        "memory_depth": 0,
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        r = self._random.uniform(3, 7) / 10
        return self._random.random_choice(r)


@FinalTransformer((D, D), name_prefix=None)
class FirstBySteinAndRapoport(Player):
    """
    Submitted to Axelrod's first tournament by William Stein and Amnon Rapoport.

    The description written in [Axelrod1980]_ is:

    > "This rule plays tit for tat except that it cooperates on the first four
    > moves, it defects on the last two moves, and every fifteen moves it checks
    > to see if the opponent seems to be playing randomly. This check uses a
    > chi-squared test of the other's transition probabilities and also checks for
    > alternating moves of CD and DC.

    This is implemented as follows:

    1. It cooperates for the first 4 moves.
    2. It defects on the last 2 moves.
    3. Every 15 moves it makes use of a `chi-squared
       test <http://en.wikipedia.org/wiki/Chi-squared_test>`_ to check if the
       opponent is playing randomly. If so it defects.

    This strategy came 6th in Axelrod's original tournament.

    Names:

    - SteinAndRapoport: [Axelrod1980]_
    """

    name = "First by Stein and Rapoport"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, alpha: float = 0.05) -> None:
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
            p_value = chisquare([opponent.cooperations, opponent.defections]).pvalue
            self.opponent_is_random = p_value >= self.alpha

        if self.opponent_is_random:
            # Defect if opponent plays randomly
            return D
        else:  # TitForTat if opponent plays not randomly
            return opponent.history[-1]


@FinalTransformer((D, D), name_prefix=None)
class FirstByTidemanAndChieruzzi(Player):
    """
    Submitted to Axelrod's first tournament by Nicolas Tideman and Paula
    Chieruzzi.

    The description written in [Axelrod1980]_ is:

    > "This rule begins with cooperation and tit for tat. However, when the
    > other player finishes his second run of defec- tions, an extra punishment is
    > instituted, and the number of punishing defections is increased by one with
    > each run of the other's defections. The other player is given a fresh start
    > if he is 10 or more points behind, if he has not just started a run of
    > defections, if it has been at least 20 moves since a fresh start, if there
    > are at least 10 moves remaining, and if the number of defections differs
    > from a 50-50 random generator by at least 3.0 standard deviations. A fresh
    > start involves two cooperations and then play as if the game had just
    > started. The program defects automatically on the last two moves."

    This is interpreted as:

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

    3. The strategy defects on the last two moves.

    This strategy came 2nd in Axelrod’s original tournament.

    Names:

    - TidemanAndChieruzzi: [Axelrod1980]_
    """

    name = "First by Tideman and Chieruzzi"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
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
        self.remembered_number_of_opponent_defectioons = 0

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
        self.remembered_number_of_opponent_defectioons = 0

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

        if opponent.history[-1] == D:
            self.remembered_number_of_opponent_defectioons += 1

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
            valid_rounds = self.match_attributes["length"] - current_round >= 10
            opponent_is_cooperating = opponent.history[-1] == C
            if valid_points and valid_rounds and opponent_is_cooperating:
                # 50-50 split is based off the binomial distribution.
                N = opponent.cooperations + opponent.defections
                # std_dev = sqrt(N*p*(1-p)) where p is 1 / 2.
                std_deviation = (N ** (1 / 2)) / 2
                lower = N / 2 - 3 * std_deviation
                upper = N / 2 + 3 * std_deviation
                if (self.remembered_number_of_opponent_defectioons <= lower or
                    self.remembered_number_of_opponent_defectioons >= upper):
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
