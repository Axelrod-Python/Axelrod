"""
Additional strategies from Axelrod's second tournament.
"""

import random
import numpy as np
from typing import List

from axelrod.action import Action
from axelrod.player import Player
from axelrod.random_ import random_choice
from axelrod.strategies.finite_state_machines import FSMPlayer

from axelrod.interaction_utils import compute_final_score


C, D = Action.C, Action.D


class Champion(Player):
    """
    Strategy submitted to Axelrod's second tournament by Danny Champion.

    This player cooperates on the first 10 moves and plays Tit for Tat for the
    next 15 more moves. After 25 moves, the program cooperates unless all the
    following are true: the other player defected on the previous move, the
    other player cooperated less than 60% and the random number between 0 and 1
    is greater that the other player's cooperation rate.

    Names:

    - Champion: [Axelrod1980b]_
    """

    name = "Champion"
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
        current_round = len(self.history)
        # Cooperate for the first 10 turns
        if current_round == 0:
            return C
        if current_round < 10:
            return C
        # Mirror partner for the next phase
        if current_round < 25:
            return opponent.history[-1]
        # Now cooperate unless all of the necessary conditions are true
        defection_prop = opponent.defections / len(opponent.history)
        if opponent.history[-1] == D:
            r = random.random()
            if defection_prop >= max(0.4, r):
                return D
        return C


class Eatherley(Player):
    """
    Strategy submitted to Axelrod's second tournament by Graham Eatherley.

    A player that keeps track of how many times in the game the other player
    defected. After the other player defects, it defects with a probability
    equal to the ratio of the other's total defections to the total moves to
    that point.

    Names:

    - Eatherley: [Axelrod1980b]_
    """

    name = "Eatherley"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        # Cooperate on the first move
        if not len(opponent.history):
            return C
        # Reciprocate cooperation
        if opponent.history[-1] == C:
            return C
        # Respond to defections with probability equal to opponent's total
        # proportion of defections
        defection_prop = opponent.defections / len(opponent.history)
        return random_choice(1 - defection_prop)


class Tester(Player):
    """
    Submitted to Axelrod's second tournament by David Gladstein.

    This strategy is a TFT variant that attempts to exploit certain strategies. It
    defects on the first move. If the opponent ever defects, TESTER 'apologies' by
    cooperating and then plays TFT for the rest of the game. Otherwise TESTER
    alternates cooperation and defection.

    This strategy came 46th in Axelrod's second tournament.

    Names:

    - Tester: [Axelrod1980b]_
    """

    name = "Tester"
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
        self.is_TFT = False

    def strategy(self, opponent: Player) -> Action:
        # Defect on the first move
        if not opponent.history:
            return D
        # Am I TFT?
        if self.is_TFT:
            return D if opponent.history[-1:] == [D] else C
        else:
            # Did opponent defect?
            if opponent.history[-1] == D:
                self.is_TFT = True
                return C
            if len(self.history) in [1, 2]:
                return C
            # Alternate C and D
            return self.history[-1].flip()


class Gladstein(Player):
    """
    Submitted to Axelrod's second tournament by David Gladstein.

    This strategy is also known as Tester and is based on the reverse
    engineering of the Fortran strategies from Axelrod's second tournament.

    This strategy is a TFT variant that defects on the first round in order to
    test the opponent's response. If the opponent ever defects, the strategy
    'apologizes' by cooperating and then plays TFT for the rest of the game.
    Otherwise, it defects as much as possible subject to the constraint that
    the ratio of its defections to moves remains under 0.5, not counting the
    first defection.

    Names:

    - Gladstein: [Axelrod1980b]_
    - Tester: [Axelrod1980b]_
    """

    name = "Gladstein"
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
        # This strategy assumes the opponent is a patsy
        self.patsy = True

    def strategy(self, opponent: Player) -> Action:
        # Defect on the first move
        if not self.history:
            return D
        # Is the opponent a patsy?
        if self.patsy:
            # If the opponent defects, apologize and play TFT.
            if opponent.history[-1] == D:
                self.patsy = False
                return C
            # Cooperate as long as the cooperation ratio is below 0.5
            cooperation_ratio = self.cooperations / len(self.history)
            if cooperation_ratio > 0.5:
                return D
            return C
        else:
            # Play TFT
            return opponent.history[-1]


class Tranquilizer(Player):

    """
    Submitted to Axelrod's second tournament by Craig Feathers

    Description given in Axelrod's "More Effective Choice in the
    Prisoner's Dilemma" paper: The rule normally cooperates but
    is ready to defect if the other player defects too often.
    Thus the rule tends to cooperate for the first dozen or two moves
    if the other player is cooperating, but then it throws in a
    defection. If the other player continues to cooperate, then defections
    become more frequent. But as long as Tranquilizer is maintaining an
    average payoff of at least 2.25 points per move, it will never defect
    twice in succession and it will not defect more than
    one-quarter of the time.

    This implementation is based on the reverse engineering of the
    Fortran strategy K67R from Axelrod's second tournament.
    Reversed engineered by: Owen Campbell, Will Guo and Mansour Hakem.

    The strategy starts by cooperating and has 3 states.

    At the start of the strategy it updates its states:

    - It counts the number of consecutive defections by the opponent.
    - If it was in state 2 it moves to state 0 and calculates the
      following quantities two_turns_after_good_defection_ratio and
      two_turns_after_good_defection_ratio_count.

      Formula for:

      two_turns_after_good_defection_ratio:

      self.two_turns_after_good_defection_ratio = (
      ((self.two_turns_after_good_defection_ratio
      * self.two_turns_after_good_defection_ratio_count)
      + (3 - (3 * self.dict[opponent.history[-1]]))
      + (2 * self.dict[self.history[-1]])
      - ((self.dict[opponent.history[-1]]
      * self.dict[self.history[-1]])))
      / (self.two_turns_after_good_defection_ratio_count + 1)
      )

      two_turns_after_good_defection_ratio_count =
      two_turns_after_good_defection_ratio + 1

    - If it was in state 1 it moves to state 2 and calculates the
      following quantities one_turn_after_good_defection_ratio and
      one_turn_after_good_defection_ratio_count.

      Formula for:

      one_turn_after_good_defection_ratio:

      self.one_turn_after_good_defection_ratio = (
      ((self.one_turn_after_good_defection_ratio
      * self.one_turn_after_good_defection_ratio_count)
      + (3 - (3 * self.dict[opponent.history[-1]]))
      + (2 * self.dict[self.history[-1]])
      - (self.dict[opponent.history[-1]]
      * self.dict[self.history[-1]]))
      / (self.one_turn_after_good_defection_ratio_count + 1)
      )

      one_turn_after_good_defection_ratio_count:

      one_turn_after_good_defection_ratio_count =
      one_turn_after_good_defection_ratio + 1

    If after this it is in state 1 or 2 then it cooperates.

    If it is in state 0 it will potentially perform 1 of the 2
    following stochastic tests:

    1. If average score per turn is greater than 2.25 then it calculates a
    value of probability:

    probability = (
    (.95 - (((self.one_turn_after_good_defection_ratio)
    + (self.two_turns_after_good_defection_ratio) - 5) / 15))
    + (1 / (((len(self.history))+1) ** 2))
    - (self.dict[opponent.history[-1]] / 4)
    )

    and will cooperate if a random sampled number is less than that value of
    probability. If it does not cooperate then the strategy moves to state 1
    and defects.

    2. If average score per turn is greater than 1.75 but less than 2.25
    then it calculates a value of probability:

    probability = (
    (.25 + ((opponent.cooperations + 1) / ((len(self.history)) + 1)))
    - (self.opponent_consecutive_defections * .25)
    + ((current_score[0]
    - current_score[1]) / 100)
    + (4 / ((len(self.history)) + 1))
    )

    and will cooperate if a random sampled number is less than that value of
    probability. If not, it defects.

    If none of the above holds the player simply plays tit for tat.

    Tranquilizer came in 27th place in Axelrod's second torunament.


    Names:

    - Tranquilizer: [Axelrod1980]_
    """

    name = 'Tranquilizer'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': {"game"},
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        super().__init__()
        self.num_turns_after_good_defection = 0 # equal to FD variable
        self.opponent_consecutive_defections = 0 # equal to S variable
        self.one_turn_after_good_defection_ratio= 5 # equal to AD variable
        self.two_turns_after_good_defection_ratio= 0 # equal to NO variable
        self.one_turn_after_good_defection_ratio_count = 1 # equal to AK variable
        self.two_turns_after_good_defection_ratio_count = 1 # equal to NK variable
        # All above variables correspond to those in original Fotran Code
        self.dict = {C: 0, D: 1}


    def update_state(self, opponent):

        """
        Calculates the ratio values for the one_turn_after_good_defection_ratio,
        two_turns_after_good_defection_ratio and the probability values,
        and sets the value of num_turns_after_good_defection.
        """
        if opponent.history[-1] == D:
            self.opponent_consecutive_defections += 1
        else:
            self.opponent_consecutive_defections = 0

        if self.num_turns_after_good_defection == 2:
            self.num_turns_after_good_defection = 0
            self.two_turns_after_good_defection_ratio = (
                ((self.two_turns_after_good_defection_ratio
                * self.two_turns_after_good_defection_ratio_count)
                + (3 - (3 * self.dict[opponent.history[-1]]))
                + (2 * self.dict[self.history[-1]])
                - ((self.dict[opponent.history[-1]]
                * self.dict[self.history[-1]])))
                / (self.two_turns_after_good_defection_ratio_count + 1)
                )
            self.two_turns_after_good_defection_ratio_count += 1
        elif self.num_turns_after_good_defection == 1:
            self.num_turns_after_good_defection = 2
            self.one_turn_after_good_defection_ratio = (
                ((self.one_turn_after_good_defection_ratio
                * self.one_turn_after_good_defection_ratio_count)
                + (3 - (3 * self.dict[opponent.history[-1]]))
                + (2 * self.dict[self.history[-1]])
                - (self.dict[opponent.history[-1]]
                * self.dict[self.history[-1]]))
                / (self.one_turn_after_good_defection_ratio_count + 1)
                )
            self.one_turn_after_good_defection_ratio_count += 1

    def strategy(self, opponent: Player) -> Action:

        if not self.history:
            return C


        self.update_state(opponent)
        if  self.num_turns_after_good_defection in [1, 2]:
            return C

        current_score = compute_final_score(zip(self.history, opponent.history))

        if (current_score[0] / ((len(self.history)) + 1)) >= 2.25:
            probability = (
                (.95 - (((self.one_turn_after_good_defection_ratio)
                + (self.two_turns_after_good_defection_ratio) - 5) / 15))
                + (1 / (((len(self.history))+1) ** 2))
                - (self.dict[opponent.history[-1]] / 4)
                )
            if random.random() <= probability:
                return C
            self.num_turns_after_good_defection = 1
            return D
        if (current_score[0] / ((len(self.history)) + 1)) >= 1.75:
            probability = (
                (.25 + ((opponent.cooperations + 1) / ((len(self.history)) + 1)))
                - (self.opponent_consecutive_defections * .25)
                + ((current_score[0]
                - current_score[1]) / 100)
                + (4 / ((len(self.history)) + 1))
                )
            if random.random() <= probability:
                return C
            return D
        return opponent.history[-1]


class MoreGrofman(Player):
    """
    Submitted to Axelrod's second tournament by Bernard Grofman.

    This strategy has 3 phases:

    1. First it cooperates on the first two rounds
    2. For rounds 3-7 inclusive, it plays the same as the opponent's last move
    3. Thereafter, it applies the following logic, looking at its memory of the
       last 8\* rounds (ignoring the most recent round).

      - If its own previous move was C and the opponent has defected less than
        3 times in the last 8\* rounds, cooperate
      - If its own previous move was C and the opponent has defected 3 or
        more times in the last 8\* rounds, defect
      - If its own previous move was D and the opponent has defected only once
        or not at all in the last 8\* rounds, cooperate
      - If its own previous move was D and the opponent has defected more than
        once in the last 8\* rounds, defect

    \* The code looks at the first 7 of the last 8 rounds, ignoring the most
    recent round.

    Names:
    - Grofman's strategy: [Axelrod1980b]_
    - K86R: [Axelrod1980b]_
    """
    name = "MoreGrofman"
    classifier = {
        'memory_depth': 8,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        # Cooperate on the first two moves
        if len(self.history) < 2:
            return C
        # For rounds 3-7, play the opponent's last move
        elif 2 <= len(self.history) <= 6:
            return opponent.history[-1]
        else:
            # Note: the Fortran code behavior ignores the opponent behavior
            #   in the last round and instead looks at the first 7 of the last
            #   8 rounds.
            opponent_defections_last_8_rounds = opponent.history[-8:-1].count(D)
            if self.history[-1] == C and opponent_defections_last_8_rounds <= 2:
                return C
            if self.history[-1] == D and opponent_defections_last_8_rounds <= 1:
                return C
            return D


class Kluepfel(Player):
    """
    Strategy submitted to Axelrod's second tournament by Charles Kluepfel
    (K32R).

    This player keeps track of the the opponent's responses to own behavior:

    - `cd_count` counts: Opponent cooperates as response to player defecting.
    - `dd_count` counts: Opponent defects as response to player defecting.
    - `cc_count` counts: Opponent cooperates as response to player cooperating.
    - `dc_count` counts: Opponent defects as response to player cooperating.

    After 26 turns, the player then tries to detect a random player.  The
    player decides that the opponent is random if
    cd_counts >= (cd_counts+dd_counts)/2 - 0.75*sqrt(cd_counts+dd_counts) AND
    cc_counts >= (dc_counts+cc_counts)/2 - 0.75*sqrt(dc_counts+cc_counts).
    If the player decides that they are playing against a random player, then
    they will always defect.

    Otherwise respond to recent history using the following set of rules:

    - If opponent's last three choices are the same, then respond in kind.
    - If opponent's last two choices are the same, then respond in kind with
      probability 90%.
    - Otherwise if opponent's last action was to cooperate, then cooperate
      with probability 70%.
    - Otherwise if opponent's last action was to defect, then defect
      with probability 60%.

    Names:

    - Kluepfel: [Axelrod1980b]_
    """

    name = "Kluepfel"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        super().__init__()
        self.cd_counts, self.dd_counts, self.dc_counts, self.cc_counts = 0, 0, 0, 0

    def strategy(self, opponent: Player) -> Action:
        # First update the response matrix.
        if len(self.history) >= 2:
            if self.history[-2] == D:
                if opponent.history[-1] == C:
                    self.cd_counts += 1
                else:
                    self.dd_counts += 1
            else:
                if opponent.history[-1] == C:
                    self.dc_counts += 1
                else:
                    self.cc_counts += 1

        # Check for randomness
        if len(self.history) > 26:
            if self.cd_counts >= (self.cd_counts+self.dd_counts)/2 - 0.75*np.sqrt(self.cd_counts+self.dd_counts) and \
                self.cc_counts >= (self.dc_counts+self.cc_counts)/2 - 0.75*np.sqrt(self.dc_counts+self.cc_counts):
                return D

        # Otherwise respond to recent history

        one_move_ago, two_moves_ago, three_moves_ago = C, C, C
        if len(opponent.history) >= 1:
            one_move_ago = opponent.history[-1]
        if len(opponent.history) >= 2:
            two_moves_ago = opponent.history[-2]
        if len(opponent.history) >= 3:
            three_moves_ago = opponent.history[-3]

        if one_move_ago == two_moves_ago and two_moves_ago == three_moves_ago:
            return one_move_ago

        r = random.random() # Everything following is stochastic
        if one_move_ago == two_moves_ago:
            if r < 0.9:
                return one_move_ago
            else:
                return one_move_ago.flip()
        if one_move_ago == C:
            if r < 0.7:
                return one_move_ago
            else:
                return one_move_ago.flip()
        if one_move_ago == D:
            if r < 0.6:
                return one_move_ago
            else:
                return one_move_ago.flip()


class Borufsen(Player):
    """
    Strategy submitted to Axelrod's second tournament by Otto Borufsen
    (K32R), and came in third in that tournament.

    This player keeps track of the the opponent's responses to own behavior:

    - `cd_count` counts: Opponent cooperates as response to player defecting.
    - `cc_count` counts: Opponent cooperates as response to player cooperating.

    The player has a defect mode and a normal mode.  In defect mode, the
    player will always defect.  In normal mode, the player obeys the following
    ranked rules:

    1. If in the last three turns, both the player/opponent defected, then
       cooperate for a single turn.
    2. If in the last three turns, the player/opponent acted differently from
       each other and they're alternating, then change next defect to
       cooperate.  (Doesn't block third rule.)
    3. Otherwise, do tit-for-tat.

    Start in normal mode, but every 25 turns starting with the 27th turn,
    re-evaluate the mode.  Enter defect mode if any of the following
    conditions hold:

    - Detected random:  Opponent cooperated 7-18 times since last mode
      evaluation (or start) AND less than 70% of opponent cooperation was in
      response to player's cooperation, i.e.
      cc_count / (cc_count+cd_count) < 0.7
    - Detect defective:  Opponent cooperated fewer than 3 times since last mode
      evaluation.

    When switching to defect mode, defect immediately.  The first two rules for
    normal mode require that last three turns were in normal mode.  When starting
    normal mode from defect mode, defect on first move.

    Names:

    - Borufsen: [Axelrod1980b]_
    """

    name = "Borufsen"
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
        super().__init__()
        self.cd_counts, self.cc_counts = 0, 0
        self.mutual_defect_streak = 0
        self.echo_streak = 0
        self.flip_next_defect = False
        self.mode = "Normal"

    def try_return(self, to_return):
        """
        We put the logic here to check for the `flip_next_defect` bit here,
        and proceed like normal otherwise.
        """

        if to_return == C:
            return C
        # Otherwise look for flip bit.
        if self.flip_next_defect:
            self.flip_next_defect = False
            return C
        return D

    def strategy(self, opponent: Player) -> Action:
        turn = len(self.history) + 1

        if turn == 1:
            return C

        # Update the response history.
        if turn >= 3:
            if opponent.history[-1] == C:
                if self.history[-2] == C:
                    self.cc_counts += 1
                else:
                    self.cd_counts += 1

        # Check if it's time for a mode change.
        if turn > 2 and turn % 25 == 2:
            coming_from_defect = False
            if self.mode == "Defect":
                coming_from_defect = True

            self.mode = "Normal"
            coops = self.cd_counts + self.cc_counts

            # Check for a defective strategy
            if coops < 3:
                self.mode = "Defect"

            # Check for a random strategy
            if (coops >= 8 and coops <= 17) and self.cc_counts/coops < 0.7:
                self.mode = "Defect"

            self.cd_counts, self.cc_counts = 0, 0

            # If defect mode, clear flags
            if self.mode == "Defect":
                self.mutual_defect_streak = 0
                self.echo_streak = 0
                self.flip_next_defect = False

            # Check this special case
            if self.mode == "Normal" and coming_from_defect:
                return D

        # Proceed
        if self.mode == "Defect":
            return D
        else:
            assert self.mode == "Normal"

            # Look for mutual defects
            if self.history[-1] == D and opponent.history[-1] == D:
                self.mutual_defect_streak += 1
            else:
                self.mutual_defect_streak = 0
            if self.mutual_defect_streak >= 3:
                self.mutual_defect_streak = 0
                self.echo_streak = 0 # Reset both streaks.
                return self.try_return(C)

            # Look for echoes
            # Fortran code defaults two turns back to C if only second turn
            my_two_back, opp_two_back = C, C
            if turn >= 3:
                my_two_back = self.history[-2]
                opp_two_back = opponent.history[-2]
            if self.history[-1] != opponent.history[-1] and \
                self.history[-1] == opp_two_back and opponent.history[-1] == my_two_back:
                self.echo_streak += 1
            else:
                self.echo_streak = 0
            if self.echo_streak >= 3:
                self.mutual_defect_streak = 0 # Reset both streaks.
                self.echo_streak = 0
                self.flip_next_defect = True

            # Tit-for-tat
            return self.try_return(opponent.history[-1])


class Cave(Player):
    """
    Strategy submitted to Axelrod's second tournament by Rob Cave (K49R), and
    came in fourth in that tournament.

    First look for overly-defective or apparently random opponents, and defect
    if found.  That is any opponent meeting one of:

    - turn > 39 and percent defects > 0.39
    - turn > 29 and percent defects > 0.65
    - turn > 19 and percent defects > 0.79

    Otherwise, respond to cooperation with cooperation.  And respond to defcts
    with either a defect (if opponent has defected at least 18 times) or with
    a random (50/50) choice.  [Cooperate on first.]

    Names:

    - Cave: [Axelrod1980b]_
    """

    name = "Cave"
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
        turn = len(self.history) + 1
        if turn == 1:
            return C

        number_defects = opponent.defections
        perc_defects = number_defects / turn

        # Defect if the opponent has defected often or appears random.
        if turn > 39 and perc_defects > 0.39:
            return D
        if turn > 29 and perc_defects > 0.65:
            return D
        if turn > 19 and perc_defects > 0.79:
            return D

        if opponent.history[-1] == D:
            if number_defects > 17:
                return D
            else:
                return random_choice(0.5)
        else:
            return C


class WmAdams(Player):
    """
    Strategy submitted to Axelrod's second tournament by William Adams (K44R),
    and came in fifth in that tournament.

    Count the number of opponent defections after their first move, call
    `c_defect`.  Defect if c_defect equals 4, 7, or 9.  If c_defect > 9,
    then defect immediately after opponent defects with probability =
    (0.5)^(c_defect-1).  Otherwise cooperate.

    Names:

    - WmAdams: [Axelrod1980b]_
    """

    name = "WmAdams"
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
        if len(self.history) <= 1:
            return C
        number_defects = opponent.defections
        if opponent.history[0] == D:
            number_defects -= 1

        if number_defects in [4, 7, 9]:
            return D
        if number_defects > 9 and opponent.history[-1] == D:
            return random_choice((0.5) ** (number_defects - 9))
        return C


class GraaskampKatzen(Player):
    """
    Strategy submitted to Axelrod's second tournament by Jim Graaskamp and Ken
    Katzen (K60R), and came in sixth in that tournament.

    Play Tit-for-Tat at first, and track own score.  At select checkpoints,
    check for a high score.  Switch to Default Mode if:

    - On move 11, score < 23
    - On move 21, score < 53
    - On move 31, score < 83
    - On move 41, score < 113
    - On move 51, score < 143
    - On move 101, score < 293

    Once in Defect Mode, defect forever.

    Names:

    - GraaskampKatzen: [Axelrod1980b]_
    """

    name = "GraaskampKatzen"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(['game']),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        super().__init__()
        self.own_score = 0
        self.mode = "Normal"

    def update_score(self, opponent: Player):
        game = self.match_attributes["game"]
        last_round = (self.history[-1], opponent.history[-1])
        self.own_score += game.score(last_round)[0]

    def strategy(self, opponent: Player) -> Action:
        if self.mode == "Defect":
            return D

        turn = len(self.history) + 1
        if turn == 1:
            return C

        self.update_score(opponent)

        if turn == 11 and self.own_score < 23 or \
           turn == 21 and self.own_score < 53 or \
           turn == 31 and self.own_score < 83 or \
           turn == 41 and self.own_score < 113 or \
           turn == 51 and self.own_score < 143 or \
           turn == 101 and self.own_score < 293:
            self.mode = "Defect"
            return D

        return opponent.history[-1] # Tit-for-Tat


class Weiner(Player):
    """
    Strategy submitted to Axelrod's second tournament by Herb Weiner (K41R),
    and came in seventh in that tournament.

    Play Tit-for-Tat with a chance for forgiveness and a defective override.

    The chance for forgiveness happens only if `forgive_flag` is raised
    (flag discussed below).  If raised and `turn` is greater than `grudge`,
    then override Tit-for-Tat with Cooperation.  `grudge` is a variable that
    starts at 0 and increments 20 with each forgiven Defect (a Defect that is
    overriden through the forgiveness logic).  `forgive_flag` is lower whether
    logic is overriden or not.

    The variable `defect_padding` increments with each opponent Defect, but
    resets to zero with each opponent Cooperate (or `forgive_flag` lowering) so
    that it roughly counts Defects between Cooperates.  Whenever the opponent
    Cooperates, if `defect_padding` (before reseting) is odd, then we raise
    `forgive_flag` for next turn.

    Finally a defective override is assessed after forgiveness.  If five or
    more of the opponent's last twelve actions are Defects, then Defect.  This
    will overrule a forgiveness, but doesn't undo the lowering of
    `forgiveness_flag`.  Note that "last twelve actions" doesn't count the most
    recent action.  Actually the original code updates history after checking
    for defect override.

    Names:

    - Weiner: [Axelrod1980b]_
    """

    name = "Weiner"
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
        super().__init__()
        self.forgive_flag = False
        self.grudge = 0
        self.defect_padding = 0
        self.last_twelve = [0] * 12
        self.lt_index = 0 # Circles around last_twelve

    def try_return(self, to_return):
        """
        We put the logic here to check for the defective override.
        """

        if np.sum(self.last_twelve) >= 5:
            return D
        return to_return

    def strategy(self, opponent: Player) -> Action:
        if len(opponent.history) == 0:
            return C

        # Update history, lag 1.
        if len(opponent.history) >= 2:
            self.last_twelve[self.lt_index] = 0
            if opponent.history[-2] == D:
                self.last_twelve[self.lt_index] = 1
            self.lt_index = (self.lt_index + 1) % 12

        if self.forgive_flag:
            self.forgive_flag = False
            self.defect_padding = 0
            if self.grudge < len(self.history) + 1 and opponent.history[-1] == D:
                # Then override
                self.grudge += 20
                return self.try_return(C)
            else:
                return self.try_return(opponent.history[-1])
        else:
            # See if forgive_flag should be raised
            if opponent.history[-1] == D:
                self.defect_padding += 1
            else:
                if self.defect_padding % 2 == 1:
                    self.forgive_flag = True
                self.defect_padding = 0

            return self.try_return(opponent.history[-1])


class Harrington(Player):
    """
    Strategy submitted to Axelrod's second tournament by Paul Harrington (K75R)
    and came in eighth in that tournament.

    This strategy has three modes:  Normal, Fair-weather, and Defect.  These
    mode names were not present in Harrington's submission.

    In Normal and Fair-weather modes, the strategy begins by:

    - Update history
    - Try to detect random opponent if turn is multiple of 15 and >=30.
    - Check if `burned` flag should be raised.
    - Check for Fair-weather opponent if turn is 38.

    Updating history means to increment the correct cell of the `move_history`.
    `move_history` is a matrix where the columns are the opponent's previous
    move and the rows are indexed by the combo of this player's and the
    opponent's moves two turns ago.  [The upper-left cell must be all
    Cooperations, but otherwise order doesn't matter.]  After we enter Defect
    mode, `move_history` won't be used again.

    If the turn is a multiple of 15 and >=30, then attempt to detect random.
    If random is detected, enter Defect mode and defect immediately.  If the
    player was previously in Defect mode, then do not re-enter.  The random
    detection logic is a modified Pearson's Chi Squared test, with some
    additional checks.  [More details in `detect_random` docstrings.]

    Some of this player's moves are marked as "generous."  If this player made
    a generous move two turns ago and the opponent replied with a Defect, then
    raise the `burned` flag.  This will stop certain generous moves later.

    The player mostly plays Tit-for-Tat for the first 36 moves, then defects on
    the 37th move.  If the opponent cooperates on the first 36 moves, and
    defects on the 37th move also, then enter Fair-weather mode and cooperate
    this turn.  Entering Fair-weather mode is extremely rare, since this can
    only happen if the opponent cooperates for the first 36 then defects
    unprovoked on the 37th.  (That is, this player's first 36 moves are also
    Cooperations, so there's nothing really to trigger an opponent Defection.)

    Next in Normal Mode:

    1. Check for defect and parity streaks.
    2. Check if cooperations are scheduled.
    3. Otherwise,

    - If turn < 37, Tit-for-Tat.
    - If turn = 37, defect, mark this move as generous, and schedule two
      more cooperations**.
    - If turn > 37, then if `burned` flag is raised, then Tit-for-Tat.
      Otherwise, Tit-for-Tat with probability 1 - `prob`.  And with
      probability `prob`, defect, schedule two cooperations, mark this move
      as generous, and increase `prob` by 5%.

    ** Scheduling two cooperations means to set `more_coop` flag to two.  If in
    Normal mode and no streaks are detected, then the player will cooperate and
    lower this flag, until hitting zero.  It's possible that the flag can be
    overwritten.  Notable on the 37th turn defect, this is set to two, but the
    38th turn Fair-weather check will set this.

    If the opponent's last twenty moves were defections, then defect this turn.
    Then check for a parity streak, by flipping the parity bit (there are two
    streaks that get tracked which are something like odd and even turns, but
    this flip bit logic doesn't get run every turn), then incrementing the
    parity streak that we're pointing to.  If the parity streak that we're
    pointing to is then greater than `parity_limit` then reset the streak and
    cooperate immediately.  `parity_limit` is initially set to five, but after
    it has been hit eight times, it decreases to three.  The parity streak that
    we're pointing to also gets incremented if in normal mode and we defect but
    not on turn 38, unless we are defecting as the result of a defect streak.
    Note that the parity streaks resets but the defect streak doesn't.

    If `more_coop` >= 1, then we cooperate and lower that flag here, in Normal
    mode after checking streaks.  Still lower this flag if cooperating as the
    result of a parity streak or in Fair-weather mode.

    Then use the logic based on turn from above.

    In Fair-Weather mode after running the code from above, check if opponent
    defected last turn.  If so, exit Fair-Weather mode, and proceed THIS TURN
    with Normal mode.  Otherwise cooperate.

    In Defect mode, update the `exit_defect_meter` (originally zero) by
    incrementing if opponent defected last turn and decreasing by three
    otherwise.  If `exit_defect_meter` is then 11, then set mode to Normal (for
    future turns), cooperate and schedule two more cooperations.  [Note that
    this move is not marked generous.]

    Names:

    - Harrington: [Axelrod1980b]_
    """

    name = "Harrington"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        super().__init__()
        self.mode = "Normal"
        self.recorded_defects = 0  # Count opponent defects after turn 1
        self.exit_defect_meter = 0  # When >= 11, then exit defect mode.
        self.coops_in_first_36 = None  # On turn 37, count cooperations in first 36
        self.was_defective = False  # Previously in Defect mode

        self.prob = 0.25  # After turn 37, probability that we'll defect

        self.move_history = np.zeros([4, 2])

        self.more_coop = 0  # This schedules cooperation for future turns
        # Initial last_generous_n_turns_ago to 3 because this counts up and
        # triggers a strategy change at 2.
        self.last_generous_n_turns_ago = 3  # How many tuns ago was a "generous" move
        self.burned = False

        self.defect_streak = 0
        self.parity_streak = [0, 0]  # Counters that get (almost) alternatively incremented.
        self.parity_bit = 0  # Which parity_streak to increment
        self.parity_limit = 5  # When a parity streak hits this limit, alter strategy.
        self.parity_hits = 0  # Counts how many times a parity_limit was hit.
        # After hitting parity_hits 8 times, lower parity_limit to 3.

    def try_return(self, to_return, lower_flags=True, inc_parity=False):
        """
        This will return to_return, with some end-of-turn logic.
        """

        if lower_flags and to_return == C:
            # In most cases when Cooperating, we want to reduce the number that
            # are scheduled.
            self.more_coop -= 1
            self.last_generous_n_turns_ago += 1

        if inc_parity and to_return == D:
            # In some cases we increment the `parity_streak` that we're on when
            # we return a Defection.  In detect_parity_streak, `parity_streak`
            # counts opponent's Defections.
            self.parity_streak[self.parity_bit] += 1

        return to_return

    def calculate_chi_squared(self, turn):
        """
        Pearson's Chi Squared statistic = sum[ (E_i-O_i)^2 / E_i ], where O_i
        are the observed matrix values, and E_i is calculated as number (of
        defects) in the row times the number in the column over (total number
        in the matrix minus 1).  Equivalently, we expect we expect (for an
        independent distribution) the total number of recorded turns times the
        portion in that row times the portion in that column.

        In this function, the statistic is non-standard in that it excludes
        summands where E_i <= 1.
        """

        denom = turn - 2

        expected_matrix = np.outer(self.move_history.sum(axis=1),
                                   self.move_history.sum(axis=0)) / denom

        chi_squared = 0.0
        for i in range(4):
            for j in range(2):
                expect = expected_matrix[i, j]
                if expect > 1.0:
                    chi_squared += (expect - self.move_history[i, j]) ** 2 / expect

        return chi_squared

    def detect_random(self, turn):
        """
        We check if the top-left cell of the matrix (corresponding to all
        Cooperations) has over 80% of the turns.  In which case, we label
        non-random.

        Then we check if over 75% or under 25% of the opponent's turns are
        Defections.  If so, then we label as non-random.

        Otherwise we calculates a modified Pearson's Chi Squared statistic on
        self.history, and returns True (is random) if and only if the statistic
        is less than or equal to 3.
        """

        denom = turn - 2

        if self.move_history[0, 0] / denom >= 0.8:
            return False
        if self.recorded_defects / denom < 0.25 or self.recorded_defects / denom > 0.75:
            return False

        if self.calculate_chi_squared(turn) > 3:
            return False
        return True

    def detect_streak(self, last_move):
        """
        Return true if and only if the opponent's last twenty moves are defects.
        """

        if last_move == D:
            self.defect_streak += 1
        else:
            self.defect_streak = 0
        if self.defect_streak >= 20:
            return True
        return False

    def detect_parity_streak(self, last_move):
        """
        Switch which `parity_streak` we're pointing to and incerement if the
        opponent's last move was a Defection.  Otherwise reset the flag.  Then
        return true if and only if the `parity_streak` is at least
        `parity_limit`.

        This is similar to detect_streak with alternating streaks, except that
        these streaks get incremented elsewhere as well.
        """

        self.parity_bit = 1 - self.parity_bit  # Flip bit
        if last_move == D:
            self.parity_streak[self.parity_bit] += 1
        else:
            self.parity_streak[self.parity_bit] = 0
        if self.parity_streak[self.parity_bit] >= self.parity_limit:
            return True

    def strategy(self, opponent: Player) -> Action:
        turn = len(self.history) + 1

        if turn == 1:
            return C

        if self.mode == "Defect":
            # There's a chance to exit Defect mode.
            if opponent.history[-1] == D:
                self.exit_defect_meter += 1
            else:
                self.exit_defect_meter -= 3
            # If opponent has been mostly defecting.
            if self.exit_defect_meter >= 11:
                self.mode = "Normal"
                self.was_defective = True
                self.more_coop = 2
                return self.try_return(to_return=C, lower_flags=False)

            return self.try_return(D)


        # If not Defect mode, proceed to update history and check for random,
        # check if burned, and check if opponent's fairweather.

        # If we haven't yet entered Defect mode
        if not self.was_defective:
            if turn > 2:
                if opponent.history[-1] == D:
                    self.recorded_defects += 1

                # Column decided by opponent's last turn
                history_col = 1 if opponent.history[-1] == D else 0
                # Row is decided by opponent's move two turns ago and our move
                # two turns ago.
                history_row = 1 if opponent.history[-2] == D else 0
                if self.history[-2] == D:
                    history_row += 2
                self.move_history[history_row, history_col] += 1

            # Try to detect random opponent
            if turn % 15 == 0 and turn > 15:
                if self.detect_random(turn):
                    self.mode = "Defect"
                    return self.try_return(D, lower_flags=False)  # Lower_flags not used here.

        # If generous 2 turns ago and opponent defected last turn
        if self.last_generous_n_turns_ago == 2 and opponent.history[-1] == D:
            self.burned = True

        # Only enter Fair-weather mode if the opponent Cooperated the first 37
        # turns then Defected on the 38th.
        if turn == 38 and opponent.history[-1] == D and opponent.cooperations == 36:
            self.mode = "Fair-weather"
            return self.try_return(to_return=C, lower_flags=False)


        if self.mode == "Fair-weather":
            if opponent.history[-1] == D:
                self.mode = "Normal"  # Post-Defect is not possible
                # Proceed with Normal mode this turn.
            else:
                # Never defect against a fair-weather opponent
                return self.try_return(C)

        # Continue with Normal mode

        # Check for streaks
        if self.detect_streak(opponent.history[-1]):
            return self.try_return(D, inc_parity=True)
        if self.detect_parity_streak(opponent.history[-1]):
            self.parity_streak[self.parity_bit] = 0  # Reset `parity_streak` when we hit the limit.
            self.parity_hits += 1  # Keep track of how many times we hit the limit.
            if self.parity_hits >= 8:  # After 8 times, lower the limit.
                self.parity_limit = 3
            return self.try_return(C, inc_parity=True)  # Inc parity won't get used here.

        # If we have Cooperations scheduled, then Cooperate here.
        if self.more_coop >= 1:
            return self.try_return(C, lower_flags=True, inc_parity=True)

        if turn < 37:
            # Tit-for-Tat
            return self.try_return(opponent.history[-1], inc_parity=True)
        if turn == 37:
            # Defect once on turn 37 (if no streaks)
            self.more_coop, self.last_generous_n_turns_ago = 2, 1
            return self.try_return(D, lower_flags=False)
        if self.burned or random.random() > self.prob:
            # Tit-for-Tat with probability 1-`prob`
            return self.try_return(opponent.history[-1], inc_parity=True)

        # Otherwise Defect, Cooperate, Cooperate, and increase `prob`
        self.prob += 0.05
        self.more_coop, self.last_generous_n_turns_ago = 2, 1
        return self.try_return(D, lower_flags=False)


class MoreTidemanAndChieruzzi(Player):
    """
    Strategy submitted to Axelrod's second tournament by T. Nicolaus Tideman
    and Paula Chieruzzi (K84R) and came in ninth in that tournament.

    This strategy Cooperates if this player's score exceeds the opponent's
    score by at least `score_to_beat`.  `score_to_beat` starts at zero and
    increases by `score_to_beat_inc` every time the opponent's last two moves
    are a Cooperation and Defection in that order.  `score_to_beat_inc` itself
    increase by 5 every time the opponent's last two moves are a Cooperation
    and Defection in that order.

    Additionally, the strategy executes a "fresh start" if the following hold:

    - The strategy would Defect by score (difference less than `score_to_beat`)
    - The opponent did not Cooperate and Defect (in order) in the last two
      turns.
    - It's been at least 10 turns since the last fresh start.  Or since the
      match started if there hasn't been a fresh start yet.

    A "fresh start" entails two Cooperations and resetting scores,
    `scores_to_beat` and `scores_to_beat_inc`.

    Names:

    - MoreTidemanAndChieruzzi: [Axelrod1980b]_
    """

    name = 'More Tideman and Chieruzzi'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': {"game"},
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        self.current_score = 0
        self.opponent_score = 0
        self.last_fresh_start = 0
        self.fresh_start = False
        self.score_to_beat = 0
        self.score_to_beat_inc = 0

    def _fresh_start(self):
        """Give the opponent a fresh start by forgetting the past"""
        self.current_score = 0
        self.opponent_score = 0
        self.score_to_beat = 0
        self.score_to_beat_inc = 0

    def _score_last_round(self, opponent: Player):
        """Updates the scores for each player."""
        # Load the default game if not supplied by a tournament.
        game = self.match_attributes["game"]
        last_round = (self.history[-1], opponent.history[-1])
        scores = game.score(last_round)
        self.current_score += scores[0]
        self.opponent_score += scores[1]

    def strategy(self, opponent: Player) -> Action:
        current_round = len(self.history) + 1

        if current_round == 1:
            return C

        # Calculate the scores.
        self._score_last_round(opponent)

        # Check if we have recently given the strategy a fresh start.
        if self.fresh_start:
            self._fresh_start()
            self.last_fresh_start = current_round
            self.fresh_start = False
            return C  # Second cooperation

        opponent_CDd = False

        opponent_two_turns_ago = C # Default value for second turn.
        if len(opponent.history) >= 2:
            opponent_two_turns_ago = opponent.history[-2]
        # If opponent's last two turns are C and D in that order.
        if opponent_two_turns_ago == C and opponent.history[-1] == D:
            opponent_CDd = True
            self.score_to_beat += self.score_to_beat_inc
            self.score_to_beat_inc += 5

        # Cooperate if we're beating opponent by at least `score_to_beat`
        if self.current_score - self.opponent_score >= self.score_to_beat:
            return C

        # Wait at least ten turns for another fresh start.
        if (not opponent_CDd) and current_round - self.last_fresh_start >= 10:
            # 50-50 split is based off the binomial distribution.
            N = opponent.cooperations + opponent.defections
            # std_dev = sqrt(N*p*(1-p)) where p is 1 / 2.
            std_deviation = (N ** (1 / 2)) / 2
            lower = N / 2 - 3 * std_deviation
            upper = N / 2 + 3 * std_deviation
            if opponent.defections <= lower or opponent.defections >= upper:
                # Opponent deserves a fresh start
                self.fresh_start = True
                return C  # First cooperation

        return D


class Getzler(Player):
    """
    Strategy submitted to Axelrod's second tournament by Abraham Getzler (K35R)
    and came in eleventh in that tournament.

    Strategy Defects with probability `flack`, where `flack` is calculated as
    the sum over opponent Defections of 0.5 ^ (turns ago Defection happened).

    Names:

    - Getzler: [Axelrod1980b]_
    """

    name = 'Getzler'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        self.flack = 0.0  # The relative untrustworthiness of opponent

    def strategy(self, opponent: Player) -> Action:
        if not opponent.history:
            return C

        self.flack += 1 if opponent.history[-1] == D else 0
        self.flack *= 0.5  # Defections have half-life of one round

        return random_choice(1.0 - self.flack)


class Leyvraz(Player):
    """
    Strategy submitted to Axelrod's second tournament by Fransois Leyvraz
    (K68R) and came in twelfth in that tournament.

    The strategy uses the opponent's last three moves to decide on an action
    based on the following ordered rules.

    1. If opponent Defected last two turns, then Defect with prob 75%.
    2. If opponent Defected three turns ago, then Cooperate.
    3. If opponent Defected two turns ago, then Defect.
    4. If opponent Defected last turn, then Defect with prob 50%.
    5. Otherwise (all Cooperations), then Cooperate.

    Names:

    - Leyvraz: [Axelrod1980b]_
    """

    name = 'Leyvraz'
    classifier = {
        'memory_depth': 3,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        self.prob_coop = {
            (C, C, C): 1.0,
            (C, C, D): 0.5,  # Rule 4
            (C, D, C): 0.0,  # Rule 3
            (C, D, D): 0.25,  # Rule 1
            (D, C, C): 1.0,  # Rule 2
            (D, C, D): 1.0,  # Rule 2
            (D, D, C): 1.0,  # Rule 2
            (D, D, D): 0.25  # Rule 1
        }

    def strategy(self, opponent: Player) -> Action:
        recent_history = [C, C, C]  # Default to C.
        for go_back in range(1, 4):
            if len(opponent.history) >= go_back:
                recent_history[-go_back] = opponent.history[-go_back]

        return random_choice(self.prob_coop[(recent_history[-3],
                                             recent_history[-2],
                                             recent_history[-1])])


class White(Player):
    """
    Strategy submitted to Axelrod's second tournament by Edward C White (K72R)
    and came in thirteenth in that tournament.

    * If the opponent Cooperated last turn or in the first ten turns, then
      Cooperate.
    * Otherwise Defect if and only if:
        floor(log(turn)) * opponent Defections >= turn

    Names:

    - White: [Axelrod1980b]_
    """

    name = 'White'
    classifier = {
        'memory_depth': float("inf"),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        turn = len(self.history) + 1

        if turn <= 10 or opponent.history[-1] == C:
            return C

        if np.floor(np.log(turn)) * opponent.defections >= turn:
            return D
        return C


class Black(Player):
    """
    Strategy submitted to Axelrod's second tournament by Paul E Black (K83R)
    and came in fifteenth in that tournament.

    The strategy Cooperates for the first five turns.  Then it calculates the
    number of opponent defects in the last five moves and Cooperates with
    probability `prob_coop`[`number_defects`], where:

    prob_coop[number_defects] = 1 - (number_defects^ 2 - 1) / 25

    Names:

    - Black: [Axelrod1980b]_
    """

    name = 'Black'
    classifier = {
        'memory_depth': 5,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        # Maps number of opponent defects from last five moves to own
        # Cooperation probability
        self.prob_coop = {
            0: 1.0,
            1: 1.0,
            2: 0.88,
            3: 0.68,
            4: 0.4,
            5: 0.04
        }

    def strategy(self, opponent: Player) -> Action:
        if len(opponent.history) < 5:
            return C

        recent_history = opponent.history[-5:]

        did_d = np.vectorize(lambda action: int(action == D))
        number_defects = np.sum(did_d(recent_history))

        return random_choice(self.prob_coop[number_defects])


class RichardHufford(Player):
    """
    Strategy submitted to Axelrod's second tournament by Richard Hufford (K47R)
    and came in sixteenth in that tournament.

    The strategy tracks opponent "agreements", that is whenever the opponent's
    previous move is the some as this player's move two turns ago.  If the
    opponent's first move is a Defection, this is counted as a disagreement,
    and otherwise an agreement.  From the agreement counts, two measures are
    calculated:

    - `proportion_agree`:  This is the number of agreements (through opponent's
      last turn) + 2 divided by the current turn number.
    - `last_four_num`:  The number of agreements in the last four turns.  If
      there have been fewer than four previous turns, then this is number of
      agreement + (4 - number of past turns).

    We then use these measures to decide how to play, using these rules:

    1. If `proportion_agree` > 0.9 and `last_four_num` >= 4, then Cooperate.
    2. Otherwise if `proportion_agree` >= 0.625 and `last_four_num` >= 2, then
       Tit-for-Tat.
    3. Otherwise, Defect.

    However, if the opponent has Cooperated the last `streak_needed` turns,
    then the strategy deviates from the usual strategy, and instead Defects.
    (We call such deviation an "aberration".)  In the turn immediately after an
    aberration, the strategy doesn't override, even if there's a streak of
    Cooperations.  Two turns after an aberration, the strategy:  Restarts the
    Cooperation streak (never looking before this turn); Cooperates; and
    changes `streak_needed` to:

    floor(20.0 * `num_abb_def` / `num_abb_coop`) + 1

    Here `num_abb_def` is 2 + the number of times that the opponent Defected in
    the turn after an aberration, and `num_abb_coop` is 2 + the number of times
    that the opponent Cooperated in response to an aberration.

    Names:

    - RichardHufford: [Axelrod1980b]_
    """

    name = 'RichardHufford'
    classifier = {
        'memory_depth': float("inf"),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        self.num_agreements = 2
        self.last_four_agreements = [1] * 4
        self.last_four_index = 0

        self.streak_needed = 21
        self.current_streak = 2
        self.last_aberration = float("inf")
        self.coop_after_ab_count = 2
        self.def_after_ab_count = 2

    def strategy(self, opponent: Player) -> Action:
        turn = len(self.history) + 1
        if turn == 1:
            return C

        # Check if opponent agreed with us.
        self.last_four_index = (self.last_four_index + 1) % 4
        me_two_moves_ago = C
        if turn > 2:
            me_two_moves_ago = self.history[-2]
        if me_two_moves_ago == opponent.history[-1]:
            self.num_agreements += 1
            self.last_four_agreements[self.last_four_index] = 1
        else:
            self.last_four_agreements[self.last_four_index] = 0

        # Check if last_aberration is infinite.
        # i.e Not an aberration in last two turns.
        if turn < self.last_aberration:
            if opponent.history[-1] == C:
                self.current_streak += 1
            else:
                self.current_streak = 0
            if self.current_streak >= self.streak_needed:
                self.last_aberration = turn
                if self.current_streak == self.streak_needed:
                    return D
        elif turn == self.last_aberration + 2:
            self.last_aberration = float("inf")
            if opponent.history[-1] == C:
                self.coop_after_ab_count += 1
            else:
                self.def_after_ab_count += 1
            self.streak_needed = np.floor(20.0 * self.def_after_ab_count / self.coop_after_ab_count) + 1
            self.current_streak = 0
            return C

        proportion_agree = self.num_agreements / turn
        last_four_num = np.sum(self.last_four_agreements)
        if proportion_agree > 0.9 and last_four_num >= 4:
            return C
        elif proportion_agree >= 0.625 and last_four_num >= 2:
            return opponent.history[-1]
        return D


class Yamachi(Player):
    """
    Strategy submitted to Axelrod's second tournament by Brian Yamachi (K64R)
    and came in seventeenth in that tournament.

    The strategy keeps track of play history through a variable called
    `count_them_us_them`, which is a dict indexed by (X, Y, Z), where X is an
    opponent's move and Y and Z are the following moves by this player and the
    opponent, respectively.  Each turn, we look at our opponent's move two
    turns ago, call X, and our move last turn, call Y.  If (X, Y, C) has
    occurred more often (or as often) as (X, Y, D), then Cooperate.  Otherwise
    Defect.  [Note that this reflects likelihood of Cooperations or Defections
    in opponent's previous move; we don't update `count_them_us_them` with
    previous move until next turn.]

    Starting with the 41st turn, there's a possibility to override this
    behavior.  If `portion_defect` is between 45% and 55% (exclusive), then
    Defect, where `portion_defect` equals number of opponent defects plus 0.5
    divided by the turn number (indexed by 1).  When overriding this way, still
    record `count_them_us_them` as though the strategy didn't override.

    Names:

    - Yamachi: [Axelrod1980b]_
    """

    name = 'Yamachi'
    classifier = {
        'memory_depth': float("inf"),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        self.count_them_us_them = {(C, C, C): 0,
                                   (C, C, D): 0,
                                   (C, D, C): 0,
                                   (C, D, D): 0,
                                   (D, C, C): 0,
                                   (D, C, D): 0,
                                   (D, D, C): 0,
                                   (D, D, D): 0}
        self.mod_history = list() # type: List[Action]

    def try_return(self, to_return, opp_def):
        """
        Return `to_return`, unless the turn is greater than 40 AND
        `portion_defect` is between 45% and 55%.

        In this case, still record the history as `to_return` so that the
        modified behavior doesn't affect the calculation of `count_us_them_us`.
        """
        turn = len(self.history) + 1

        self.mod_history.append(to_return)

        # In later turns, check if the opponent is close to 50/50
        # If so, then override
        if turn > 40:
            portion_defect = (opp_def + 0.5) / turn
            if 0.45 < portion_defect and portion_defect < 0.55:
                return D

        return to_return

    def strategy(self, opponent: Player) -> Action:
        turn = len(self.history) + 1
        if turn == 1:
            return self.try_return(C, 0)

        us_last = self.mod_history[-1]
        them_two_ago, us_two_ago, them_three_ago = C, C, C
        if turn >= 3:
            them_two_ago = opponent.history[-2]
            us_two_ago = self.mod_history[-2]
        if turn >= 4:
            them_three_ago = opponent.history[-3]

        # Update history
        if turn >= 3:
            self.count_them_us_them[(them_three_ago, us_two_ago, them_two_ago)] += 1

        if self.count_them_us_them[(them_two_ago, us_last, C)] >= \
           self.count_them_us_them[(them_two_ago, us_last, D)]:
            return self.try_return(C, opponent.defections)
        return self.try_return(D, opponent.defections)


class Colbert(FSMPlayer):
    """
    Strategy submitted to Axelrod's second tournament by William Colbert (K51R)
    and came in eighteenth in that tournament.

    In the first eight turns, this strategy Coopearates on all but the sixth
    turn, in which it Defects.  After that, the strategy responds to an
    opponent Cooperation with a single Cooperation, and responds to a Defection
    with a chain of responses:  Defect, Defect, Cooperate, Cooperate.  During
    this chain, the strategy ignores opponent's moves.

    Names:

    - Colbert: [Axelrod1980b]_
    """

    name = "Colbert"
    classifier = {
        'memory_depth': 4,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (0, C, 1, C), (0, D, 1, C),  # First 8 turns are special
            (1, C, 2, C), (1, D, 2, C),
            (2, C, 3, C), (2, D, 3, C),
            (3, C, 4, C), (3, D, 4, C),
            (4, C, 5, D), (4, D, 5, D),  # Defect on 6th turn.
            (5, C, 6, C), (5, D, 6, C),
            (6, C, 7, C), (6, D, 7, C),

            (7, C, 7, C), (7, D, 8, D),
            (8, C, 9, D), (8, D, 9, D),
            (9, C, 10, C), (9, D, 10, C),
            (10, C, 7, C), (10, D, 7, C)
        )

        super().__init__(transitions=transitions, initial_state=0,
                         initial_action=C)


class Mikkelson(FSMPlayer):
    """
    Strategy submitted to Axelrod's second tournament by Ray Mikkelson (K66R)
    and came in twentieth in that tournament.

    The strategy keeps track of a variable called `credit`, which determines if
    the strategy will Cooperate, in the sense that if `credit` is positive,
    then the strategy Cooperates.  `credit` is initialized to 7.  After the
    first turn, `credit` increments if the opponent Cooperated last turn, and
    decreases by two otherwise.  `credit` is capped above by 8 and below by -7.
    [`credit` is assessed as postive or negative, after increasing based on
    opponent's last turn.]

    If `credit` is non-positive within the first ten turns, then the strategy
    Defects and `credit` is set to 4.  If `credit` is non-positive later, then
    the strategy Defects if and only if (total # opponent Defections) / (turn#)
    is at least 15%.  [Turn # starts at 1.]

    Names:

    - Mikkelson: [Axelrod1980b]_
    """

    name = 'Mikkelson'
    classifier = {
        'memory_depth': float("inf"),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        self.credit = 7

    def strategy(self, opponent: Player) -> Action:
        turn = len(self.history) + 1
        if turn == 1:
            return C

        if opponent.history[-1] == C:
            self.credit += 1
            if self.credit > 8:
                self.credit = 8
        else:
            self.credit -= 2
            if self.credit < -7:
                self.credit = -7

        if turn == 2:
            return C
        if self.credit > 0:
            return C
        if turn <= 10:
            self.credit = 4
            return D
        if opponent.defections / turn >= 0.15:
            return D
        return C
