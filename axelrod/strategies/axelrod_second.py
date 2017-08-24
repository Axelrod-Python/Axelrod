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

    This strategy is based on the reverse engineering of the 
    Fortran strategy K67R from Axelrod's second tournament.
    Reversed engineered by: Owen Campbell, Will Guo and Mansour Hakem.


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

    
    - Has a variable, 'FD' which can be 0, 1 or 2. It has an initial value of 0
    - Has a variable 'S', which counts the consecutive number of 
    times the opponent has played D (i.e. it is reset to 0 if the opponent 
    plays C). It has an initial value of 0.
    - Has a variable, 'C', which counts the number of times the opponent Cooperates
    - Has a variable 'AK' which increases each time a move is played whilst in state
    FD = 1. It has an initial value of 1.
    - Has a variable 'NK' which increases each time a move is 
    played whilst in state FD = 2. It has an initial value of 1.
    - Has a variable 'AD' with an initial value of 5
    - Has a variable 'NO with an initial value of 0
    
     Has a variable 'NO with an initial value of 0                                                                                                                                                                                                                       
                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                        
    The strategy follows the following algorithm::                                                                                                                                                                                                                      
                                                                                                                                                                                                                                                                        
        When FD = 0:                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                        
            If the opponent's last move (JA) was Cooperate, increase the value of C by 1                                                                                                                                                                                
            If Score (K) < 1.75 * Move Number (M), play opponent's last move                                                                                                                                                                                            
            If (1.75 * M) <= K < (2.25 * M):                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                        
                Calculate Probability P:                                                                                                                                                                                                                                
                P = 0.25 + C/M - 0.25*S + (K - L)/100 + 4/M                                                                                                                                                                                                             
                Where L is the opponent's score so far                                                                                                                                                                                                                  
                If Random (R) <= P:                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                        
                    Cooperate                                                                                                                                                                                                                                           
                Else:                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                        
                    Defect                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                        
            If K >= (2.25 * M):                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                        
                Calculate probability P:                                                                                                                                                                                                                                
                P = 0.95 - (AD + NO - 5)/15 + 1/M**2 - J/4                                                                                                                                                                                                              
                Where J is the opponent's last move                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                        
                If Random (R) <= P:                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                        
                    Cooperate                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                        
                Else:                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                        
                    Set FD = 1                                                                                                                                                                                                                                          
                    Defect                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                        
        When FD = 1:                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                        
            Set FD = 2                                                                                                                                                                                                                                                  
            Set the variable 'AD':                                                                                                                                                                                                                                      
            AD = ((AD * AK) + 3 - (3 * J) + (2 * JA) - (JA * J)) / (AK + 1)                                                                                                                                                                                             
            Where JA and J are the last moves of the strategy and the opponent (C=0, D=1)                                                                                                                                                                       
            Increase the value of AK by 1                                                                                                                                                                                                                               
            Cooperate                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                        
        When FD = 2:                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                        
            Set FD = 0                                                                                                                                                                                                                                                  
            Set the variable 'NO':                                                                                                                                                                                                                                      
            NO = ((NO * NK) + 3 - (3 * J) + (2 * JA) - (JA * J) / (NK + 1)                                                                                                                                                                                              
            Where JA and J are the last moves of the strategy and the opponent (C=0, D=1)                                                                                                                                                                       
            Increase the value of NK by 1                                                                                                                                                                                                                               
            Cooperate                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                        
    Tranquilizer came in 27th place in Axelrod's second torunament. 
   

    Names:

    - Craig Feathers: [Axelrod1980]_
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

    # Initialised atributes
    def __init__(self):
        super().__init__()
        self.FD = 0
        self.consecutive_defections = 0
        self.ratio_FD1 = 5
        self.ratio_FD2 = 0
        self.ratio_FD1_count = 1
        self.ratio_FD2_count = 1
        self.score = None
        self.P = 1.1
        self.current_score = 0
        self.dict = {C: 0, D: 1}


    def update_stateFD(self, opponent):  
        
        """
        Calculates the ratioFD values and P values, as well as sets the 
        states of FD at the start of each turn
        """
        self.current_score = compute_final_score(zip(self.history, opponent.history))

        if self.FD == 2:
            self.FD = 0
            self.ratio_FD2 = (self.ratio_FD2 * self.ratio_FD2_count)
            self.ratio_FD2 += 3 - (3 * self.dict[opponent.history[-1]]) 
            self.ratio_FD2 += (2 * self.dict[self.history[-1]]) 
            self.ratio_FD2 -= self.dict[opponent.history[-1]] * self.dict[self.history[-1]]
            self.ratio_FD2 /= (self.ratio_FD2_count + 1)
            self.ratio_FD2_count += 1
        elif self.FD == 1:
            self.FD = 2
            self.ratio_FD1 = (self.ratio_FD1 * self.ratio_FD1_count)
            self.ratio_FD1 += (3 - (3 * self.dict[opponent.history[-1]])) 
            self.ratio_FD1 += (2 * self.dict[self.history[-1]]) 
            self.ratio_FD1 -= (self.dict[opponent.history[-1]] * self.dict[self.history[-1]])
            self.ratio_FD1 /= (self.ratio_FD1_count + 1)
            self.ratio_FD1_count += 1
        else:
            if (self.current_score[0] / (len(self.history))) >= 2.25:
                self.P = (.95 - (((self.ratio_FD1) + (self.ratio_FD2) - 5) / 15)) 
                self.P += (1 / ((len(self.history) + 1) ** 2)) 
                self.P -= (self.dict[opponent.history[-1]] / 4)
                self.P = round(self.P, 4)
                self.score = "good"
            elif (self.current_score[0] / (len(self.history))) >= 1.75:
                self.P = .25 + opponent.cooperations / (len(self.history)) 
                self.P -= (self.consecutive_defections * .25) 
                self.P += ((self.current_score[0] - self.current_score[1]) / 100) 
                self.P += (4 / (len(self.history) + 1))
                self.P = round(self.P, 4)
                self.score = "average"

    def strategy(self, opponent: Player) -> Action:

        randomValue = random.random()

        current_score = compute_final_score(zip(self.history, opponent.history))

        if len(self.history) == 0:
            return C
        else: 
            Tranquilizer.update_stateFD(self, opponent)
        if opponent.history[-1] == D: 
            self.consecutive_defections += 1
        else:
            self.consecutive_defections = 0

        if self.FD != 0: 
            if self.consecutive_defections == 0:
                return C
            else:
                return D
        elif (self.current_score[0] / (len(self.history))) < 1.75: 
            return opponent.history[-1]  # "If you can't beat them join'em"
        else:
            if (randomValue < self.P):  
                if self.consecutive_defections == 0:
                    return C
                else:
                    return self.history[-1]
            else:
                if self.score == "good": 
                    self.FD = 1
                else:  
                    pass
                return D
            