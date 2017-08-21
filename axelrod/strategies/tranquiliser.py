import axelrod as axl
import numpy
from axelrod.action import Action
from axelrod.player import Player
from axelrod.interaction_utils import compute_final_score
import random

C, D = Action.C, Action.D

dict = {C: 0, D: 1}


class Tranquiliser(Player):
    '''
A player that uses two ratios (which are dependent on the number of cooperations
defections of player and the opponent) to decide the next move to play.
The player can be present in three states(denoted FD): 0, 1 or 2 each causing a different outcome
dependent on the value of FD. Value of FD is dependent on the aforementioned ratios.
'''

    name = 'Tranquiliser'
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
        self.ratio_FD1_count = 0
        self.ratio_FD2_count = 0
        self.score = None
        self.P = 1.1
        self.current_score = 0

    def update_stateFD(self,
                       opponent):  # Calculates the ratioFD values and P values, as well as sets the states of FD at the start of each turn

        self.current_score = compute_final_score(zip(self.history, opponent.history))

        if self.FD == 2:
            self.FD = 0
            self.ratio_FD2 = ((self.ratio_FD2 * self.ratio_FD2_count + 3 - 3 * dict[opponent.history[-1]]) + 2 * dict[
                self.history[-1]] - dict[opponent.history[-1]] * dict[self.history[-1]]) / (self.ratio_FD2_count + 1)
            self.ratio_FD2_count += 1
        elif self.FD == 1:
            self.FD = 2
            self.ratio_FD1 = ((self.ratio_FD1 * self.ratio_FD1_count + 3 - 3 * dict[opponent.history[-1]]) + 2 * dict[
                self.history[-1]] - dict[opponent.history[-1]] * dict[self.history[-1]]) / (self.ratio_FD1_count + 1)
            self.ratio_FD1_count += 1
        else:
            if (self.current_score[0] / (len(self.history))) >= 2.25:
                self.P = .95 - ((self.ratio_FD1) + (self.ratio_FD2) - 5) / 15 + 1 / (len(self.history) + 1) ** 2 - (
                dict[opponent.history[-1]] / 4)
                self.score = "good"
            elif (self.current_score[0] / (len(self.history))) >= 1.75:
                self.P = .25 + opponent.cooperations / (len(self.history)) - (self.consecutive_defections * .25) + (
                                                                                                                  self.current_score[
                                                                                                                      0] -
                                                                                                                  self.current_score[
                                                                                                                      1]) / 100 + (
                         4 / (len(self.history) + 1))
                self.score = "average"

    def strategy(self, opponent: Player) -> Action:

        randomValue = random.random()  # Random float between 0 and 1 to decide whether the player should defect or not

        current_score = compute_final_score(zip(self.history, opponent.history))  # Calculates current score

        print(self.FD, self.P)

        if len(self.history) == 0:  # Assumes opponent will cooperate, hence, Tranquiliser cooperates
            return C
        else:  # If round number != 0, exectue the stateFD(self, opponent) function
            Tranquiliser.update_stateFD(self, opponent)
        if opponent.history[-1] == D:  # Calculates number of consecutive defections
            self.consecutive_defections += 1
        else:
            self.consecutive_defections = 0

        if self.FD != 0:  # If FD != 0, then return value dependant on number of consecutive defections
            if self.consecutive_defections == 0:
                return C
            else:
                return D
        elif (self.current_score[0] / (len(self.history))) < 1.75:  # If score is too low, copy opponent
            return opponent.history[-1]  # "If you can't beat them join'em"
        else:
            if (randomValue < self.P):  # Comapares randomValue to that of the calculated variable 'P'
                if self.consecutive_defections == 0:  # Decides what to return (based on previous move), give randomValue < 'P'
                    return C
                else:
                    return self.history[-1]
            else:
                if self.score == "good":  # If score is above 2.25 && randomValue > P, set FD = 1, and defect
                    self.FD = 1
                else:  # If score is greater than 1.75, but lower than 2.25 while randomValue > P, defect
                    pass
                return D

