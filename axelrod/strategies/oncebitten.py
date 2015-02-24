from axelrod import Player

class OnceBitten(Player):
    """
    Co-operates once when the opponent defects, but if they defect twice in a row defaults to forgetful grudger for 10 turns defecting
    """

    name = 'Once Bitten'

    def __init__(self):
        """
        Initialised the player
        """
        super(OnceBitten, self).__init__()
        self.history = []
        self.score = 0
        self.mem_length = 10
        self.grudged = False
        self.grudge_memory = 0

    def strategy(self, opponent):
        """
        Begins by playing C, then plays D for mem_length rounds if the opponent ever plays D twice in a row
        """
        if self.grudge_memory >= self.mem_length:
            self.grudge_memory = 0
            self.grudged = False

        if self.grudged:
            self.grudge_memory += 1
            return 'D'
        elif not ('C' in opponent.history[-2:]):
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
