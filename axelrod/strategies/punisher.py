from axelrod import Actions, Player

C, D = Actions.C, Actions.D

class Punisher(Player):
    """
    A player starts by cooperating however will defect if at any point the
    opponent has defected, but forgets after meme_length matches, with
    1<=mem_length<=20 proportional to the amount of time the opponent has
    played D, punishing that player for playing D too often.

    Names:

    - Punisher: Original by Geraint Palmer
    """

    name = 'Punisher'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        """
        Initialised the player
        """
        super(Punisher, self).__init__()
        self.mem_length = 1
        self.grudged = False
        self.grudge_memory = 1

    def strategy(self, opponent):
        """
        Begins by playing C, then plays D for an amount of rounds proportional
        to the opponents historical '%' of playing D if the opponent ever
        plays D
        """

        if self.grudge_memory >= self.mem_length:
            self.grudge_memory = 0
            self.grudged = False

        if self.grudged:
            self.grudge_memory += 1
            return D
        elif D in opponent.history[-1:]:
            self.mem_length = (opponent.defections * 20) // len(opponent.history)
            self.grudged = True
            return D
        return C

    def reset(self):
        """
        Resets scores and history
        """
        Player.reset(self)
        self.grudged = False
        self.grudge_memory = 0
        self.mem_length = 1


class InversePunisher(Player):
    """
    An inverted version of Punisher. Similarly the player starts by cooperating however will defect if at any point the
    opponent has defected, but forgets after mem_length matches, with 1 <= mem_length <= 20. This time mem_length is
    proportional to the amount of time the opponent has played C.

    Names:

    - Inverse Punisher: Original by Geraint Palmer
    """

    name = 'Inverse Punisher'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        super(InversePunisher, self).__init__()
        self.history = []
        self.mem_length = 1
        self.grudged = False
        self.grudge_memory = 1

    def strategy(self, opponent):
        """
        Begins by playing C, then plays D for an amount of rounds proportional to the opponents historical '%' of playing C if the opponent ever plays D
        """

        if self.grudge_memory >= self.mem_length:
            self.grudge_memory = 0
            self.grudged = False

        if self.grudged:
            self.grudge_memory += 1
            return D
        elif D in opponent.history[-1:]:
            self.mem_length = (opponent.cooperations * 20) // len(opponent.history)
            if self.mem_length == 0:
                self.mem_length += 1
            self.grudged = True
            return D
        return C

    def reset(self):
        """Resets internal variables and history"""
        Player.reset(self)
        self.grudged = False
        self.grudge_memory = 0
        self.mem_length = 1

class LevelPunisher(Player):
    """
    Names:

    - Level Punisher: Original by Geraint Palmer
    """

    name = 'Level Punisher'
    classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        if len(opponent.history) <= 10: return D
            else:
                if float(len(opponent.history) - sum(opponent.history)) / len(opponent.history) > 0.2:
                    return C
                else: return D
