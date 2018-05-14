from axelrod.action import Action
from axelrod.player import Player

from typing import List

C, D = Action.C, Action.D


class Punisher(Player):
    """
    A player starts by cooperating however will defect if at any point the
    opponent has defected, but forgets after meme_length matches, with
    1<=mem_length<=20 proportional to the amount of time the opponent has
    played D, punishing that player for playing D too often.

    Names:

    - Punisher: Original name by Geraint Palmer
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

    def __init__(self) -> None:
        """
        Initialised the player
        """
        super().__init__()
        self.mem_length = 1
        self.grudged = False
        self.grudge_memory = 1

    def strategy(self, opponent: Player) -> Action:
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


class InversePunisher(Player):
    """
    An inverted version of Punisher. The player starts by cooperating however
    will defect if at any point the opponent has defected, and forgets after
    mem_length matches, with 1 <= mem_length <= 20. This time mem_length is
    proportional to the amount of time the opponent has played C.

    Names:

    - Inverse Punisher: Original name by Geraint Palmer
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

    def __init__(self) -> None:
        super().__init__()
        self.history = [] # type: List[Action]
        self.mem_length = 1
        self.grudged = False
        self.grudge_memory = 1

    def strategy(self, opponent: Player) -> Action:
        """
        Begins by playing C, then plays D for an amount of rounds proportional
        to the opponents historical '%' of playing C if the opponent ever plays
        D.
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


class LevelPunisher(Player):
    """
    A player starts by cooperating however, after 10 rounds
    will defect if at any point the number of defections
    by an opponent is greater than 20%.

    Names:

    - Level Punisher: [Eckhart2015]_
    """

    name = 'Level Punisher'
    classifier = {
        'memory_depth': float('inf'), # Long Memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        if len(opponent.history) < 10:
            return C
        elif (len(opponent.history) - opponent.cooperations) / len(opponent.history) > 0.2:
            return D
        else:
            return C


class TrickyLevelPunisher(Player):
    """
    A player starts by cooperating however, after 10, 50 and 100 rounds
    will defect if at any point the percentage of defections
    by an opponent is greater than 20%, 10% and 5% respectively.

    Names:

    - Tricky Level Punisher: [Eckhart2015]_
    """

    name = 'Tricky Level Punisher'
    classifier = {
        'memory_depth': float('inf'), # Long Memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        if len(opponent.history) == 0:
            return C
        if len(opponent.history) < 10:
            if opponent.defections / len(opponent.history) > 0.2:
                return D
        if len(opponent.history) < 50:
            if opponent.defections / len(opponent.history) > 0.1:
                return D
        if len(opponent.history) < 100:
            if opponent.defections / len(opponent.history) > 0.05:
                return D
        return C
