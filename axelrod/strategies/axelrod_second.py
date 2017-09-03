"""
Additional strategies from Axelrod's second tournament.
"""

import random

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
        'makes_use_of': set(["length"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        current_round = len(self.history)
        expected_length = self.match_attributes['length']
        # Cooperate for the first 1/20-th of the game
        if current_round == 0:
            return C
        if current_round < expected_length / 20:
            return C
        # Mirror partner for the next phase
        if current_round < expected_length * 5 / 40:
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
