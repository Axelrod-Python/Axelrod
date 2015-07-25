from axelrod import Player


class BackStabber(Player):
    """
    Forgives the first 3 defections but on the fourth
    will defect forever. Defects after the 198th round unconditionally.
    """

    name = 'BackStabber'
    memory_depth = float('inf')  # Long memory

    def __init__(self):
        """
        Initialised the player
        """
        super(BackStabber, self).__init__()
        self.D_count = 0
        self._initial = 'C'
        self.stochastic = False

    def strategy(self, opponent):
        if len(opponent.history) > 197:
            return 'D'
        if not opponent.history:
            return self._initial
        if opponent.history[-1] == 'D':
            self.D_count += 1
        if self.D_count > 3:
            return 'D'
        return 'C'

    def reset(self):
        self.D_count = 0
        self.history = []
