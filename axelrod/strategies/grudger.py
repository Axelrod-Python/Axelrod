from axelrod import Player


class Grudger(Player):
    """A player starts by cooperating however will defect if at any point the opponent has defected."""

    name = 'Grudger'
    memoryone = False  # Long memory

    def strategy(self, opponent):
        """Begins by playing C, then plays D for the remaining rounds if the opponent ever plays D."""
        if 'D' in opponent.history:
            return 'D'
        return 'C'


class ForgetfulGrudger(Player):
    """A player starts by cooperating however will defect if at any point the
    opponent has defected, but forgets after meme_length matches."""

    name = 'Forgetful Grudger'
    memoryone = False  # Long memory

    def __init__(self):
        """Initialised the player."""
        super(ForgetfulGrudger, self).__init__()
        self.history = []
        self.score = 0
        self.mem_length = 10
        self.grudged = False
        self.grudge_memory = 0

    def strategy(self, opponent):
        """Begins by playing C, then plays D for mem_length rounds if the opponent ever plays D."""
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
        """Resets scores and history."""
        self.history = []
        self.grudged = False
        self.grudge_memory = 0


class OppositeGrudger(Player):
    """A player starts by defecting however will cooperate if at any point the opponent has cooperated."""

    name = 'Opposite Grudger'
    memoryone = False  # Long memory

    def strategy(self, opponent):
        """Begins by playing D, then plays C for the remaining rounds if the opponent ever plays C."""
        if 'C' in opponent.history:
            return 'C'
        return 'D'

class Davis(Player):
    """A player starts by cooperating for 10 rounds then plays Grudger,
    defecting if at any point the opponent has defected."""

    name = 'Davis'
    memoryone = False  # Long memory

    def __init__(self, rounds_to_cooperate=10):
        Player.__init__(self)
        self._rounds_to_cooperate = rounds_to_cooperate

    def strategy(self, opponent):
        """Begins by playing C, then plays D for the remaining rounds if the
        opponent ever plays D."""
        if len(self.history) < self._rounds_to_cooperate:
            return 'C'
        if 'D' in opponent.history:
            return 'D'
        return 'C'
