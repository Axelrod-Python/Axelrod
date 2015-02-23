from axelrod import Player

class ProportionalGrudger(Player):
    """
    A player starts by cooperating however will defect if at any point the opponent has defected,
    but forgets after meme_length matches, with 1<=mem_length<=20 proportional to the amount
    of time the opponent has played 'D'
    """

    def __init__(self):
        """
        Initialised the player
        """
        self.history = []
        self.score = 0
        self.mem_length = 1
        self.grudged = False
        self.grudge_memory = 1

    def strategy(self, opponent):
        """
        Begins by playing C, then plays D for an amount of rounds proportional to the opponents historical '%' of playing 'D' if the opponent ever plays D
        """

        if self.grudge_memory >= self.mem_length:
            self.grudge_memory = 0
            self.grudged = False

        if self.grudged:
            self.grudge_memory += 1
            return 'D'
        elif 'D' in opponent.history[-1:]:
            self.mem_length = (sum([i == 'D' for i in opponent.history])*20)/len(opponent.history)
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
        self.mem_length = 1

    def __repr__(self):
        """
        The string method for the strategy.
        """
        return 'Proportional Grudger'
