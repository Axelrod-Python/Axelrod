"""
Additional strategies from Axelrod's second tournament.
"""

import random
import numpy as np

from axelrod.action import Action
from axelrod.player import Player
from axelrod.random_ import random_choice

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
        if turn == 1: return C

        number_defects = opponent.defections
        # Size of numerator is smaller than denomator -- How it was in the Fortran.
        perc_defects = number_defects / turn
        
        # If overly defect or appears random
        if turn > 39 and perc_defects > 0.39: return D
        if turn > 29 and perc_defects > 0.65: return D
        if turn > 19 and perc_defects > 0.79: return D

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

        if number_defects in [4, 7, 9]: return D
        if number_defects > 9 and opponent.history[-1] == D:
            return random_choice((0.5) ** (number_defects - 9))
        return C
