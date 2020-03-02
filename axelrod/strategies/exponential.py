from axelrod.action import Action
from axelrod.player import Player


C, D = Action.C, Action.D


class Exponential(Player):
    """
    
    Player cooperates as long as Opponent does the same. If Opponent defects,
    Player increments a grudges variable by one, computes the current value of 
    grudges raised to its own power and adds the output to a retaliations 
    variable. 

    As long as retaliations > 0, player will defect on every turn. After each 
    defection by Player, retaliations is decremented by one. Player won't 
    resume cooperating until retaliations == 0.

    If Opponent defects while Player is still retaliating, Player increments 
    retaliations by the new value of grudges raised to its own power.

    Names:

    Exponential: Original name by Ian Thomas

    """

    name = "Exponential"

    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self):
        super().__init__()

        self.grudges = 0
        self.retaliations = 0

    def strategy(self, opponent: player):
        if not opponent.history:
            return C

        if opponent.history[-1] == C:
            if self._retaliations == 0:
                return C
            self._retaliations -= 1
            return D

        if opponent.history[-1] == D:
            self._grudges += 1
            self._retaliations += self._grudges ** self._grudges - 1
            return D




