from axelrod import Player

class ForgetfulGrudger(Player):
    """
    A player starts by cooperating however will defect if at any point the opponent has defected, but forgets after 20 matches
    """

    def __init__(self):
        """
        Initialised the player
        """
        self.history = []
        self.score = 0
        self.mem_length = 10
        self.grudged = False
        self.grudge_memory = 0

    def strategy(self, opponent):
        """
        Begins by playing C, then plays D for mem_length rounds if the opponent ever plays D
        """
        if self.grudge_memory >= self.mem_length:
            self.grudge_memory = 0
            self.grudged = False

        if self.grudged:
            self.grudge_memory += 1
            return 'D'
        elif 'D' in opponent.history[-1:]:
            self.grudged = True
            return 'D'
        return 'C'

    def reset(self):
        """
        Resets scores and history
        """
        self.history = []
        self.grudged = False
        self.grudge_memory = 0

    def __repr__(self):
        """
        The string method for the strategy.
        """
        return 'Forgetful Grudger'
