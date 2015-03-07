from axelrod import Player


class Punisher(Player):
    """
    A player starts by cooperating however will defect if at any point the opponent has defected,
    but forgets after meme_length matches, with 1<=mem_length<=20 proportional to the amount
    of time the opponent has played 'D', punishing that player for playing 'D' too often
    """

    name = 'Punisher'

    def __init__(self):
        """
        Initialised the player
        """
        super(Punisher, self).__init__()
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


class InversePunisher(Player):
    """
    A player starts by cooperating however will defect if at any point the opponent has defected,
    but forgets after meme_length matches, with 1<=mem_length<=20 proportional to the amount
    of time the opponent has played 'C'. The inverse of Punisher
    """

    name = 'Inverse Punisher'

    def __init__(self):
        """
        Initialised the player
        """
        super(InversePunisher, self).__init__()
        self.history = []
        self.score = 0
        self.mem_length = 1
        self.grudged = False
        self.grudge_memory = 1

    def strategy(self, opponent):
        """
        Begins by playing C, then plays D for an amount of rounds proportional to the opponents historical '%' of playing 'C' if the opponent ever plays D
        """

        if self.grudge_memory >= self.mem_length:
            self.grudge_memory = 0
            self.grudged = False

        if self.grudged:
            self.grudge_memory += 1
            return 'D'
        elif 'D' in opponent.history[-1:]:
            self.mem_length = ((sum([i == 'C' for i in opponent.history]))*20)/len(opponent.history)
            if self.mem_length == 0:
                self.mem_length += 1
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
