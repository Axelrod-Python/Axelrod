from axelrod import Player


class BackStabber(Player):
    """
    Forgives the first 3 defections but on the fourth
    will defect forever. Defects on the last 2 rounds unconditionally.
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
        if len(opponent.history) > (self.tournament_length - 3):
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


class DoubleCrosser(Player):
    """
    Forgives the first 3 defections but on the fourth
    will defect forever. If the opponent did not defect
    in the first 6 rounds the player will cooperate until
    the 180th round. Defects on the last 2 rounds unconditionally.
    """

    name = 'DoubleCrosser'
    memory_depth = float('inf')  # Long memory

    def __init__(self):
        """
        Initialised the player
        """
        super(DoubleCrosser, self).__init__()
        self.D_count = 0
        self._initial = 'C'
        self.stochastic = False

    def strategy(self, opponent):
        cutoff = 6
        if len(opponent.history) > (self.tournament_length - 3):
            return 'D'
        if not opponent.history:
            return self._initial
        if opponent.history[-1] == 'D':
            self.D_count += 1
        if len(opponent.history) < 180:
            if len(opponent.history) > (cutoff):
                if 'D' not in opponent.history[:cutoff + 1]:
                    if opponent.history[-2:] != ['D', 'D']:  # Fail safe
                        return 'C'
        if self.D_count > 3:
            return 'D'
        return 'C'

    def reset(self):
        self.D_count = 0
        self.history = []
