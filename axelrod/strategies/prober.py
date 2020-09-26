from typing import List

from axelrod.action import Action
from axelrod.player import Player

Vector = List[float]


C, D = Action.C, Action.D


class CollectiveStrategy(Player):
    """Defined in [Li2009]_. 'It always cooperates in the first move and defects
    in the second move. If the opponent also cooperates in the first move and
    defects in the second move, CS will cooperate until the opponent defects.
    Otherwise, CS will always defect.'

    Names:

    - Collective Strategy: [Li2009]_

    """

    name = "CollectiveStrategy"

    classifier = {
        "stochastic": False,
        "memory_depth": float("inf"),  # Long memory
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        turn = len(self.history)
        if turn == 0:
            return C
        if turn == 1:
            return D
        if opponent.defections > 1:
            return D
        if opponent.history[0:2] == [C, D]:
            return C
        return D


class Detective(Player):
    """
    Starts with C, D, C, C, or with the given sequence of actions.
    If the opponent defects at least once in the first fixed rounds,
    play as TFT forever, else defect forever.

    Names:

    - Detective: [NC2019]_
    """

    name = "Detective"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, initial_actions: List[Action] = None) -> None:
        super().__init__()
        if initial_actions is None:
            self.initial_actions = [C, D, C, C]
        else:
            self.initial_actions = initial_actions

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        hist_size = len(self.history)
        init_size = len(self.initial_actions)
        if hist_size < init_size:
            return self.initial_actions[hist_size]
        if D not in opponent.history[:init_size]:
            return D
        return opponent.history[-1]  # TFT


class Prober(Player):
    """
    Plays D, C, C initially. Defects forever if opponent cooperated in moves 2
    and 3. Otherwise plays TFT.

    Names:

    - Prober: [Li2011]_
    """

    name = "Prober"
    classifier = {
        "stochastic": False,
        "memory_depth": float("inf"),  # Long memory
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        turn = len(self.history)
        if turn == 0:
            return D
        if turn == 1:
            return C
        if turn == 2:
            return C
        if turn > 2:
            if opponent.history[1:3] == [C, C]:
                return D
            else:
                # TFT
                return D if opponent.history[-1:] == [D] else C


class Prober2(Player):
    """
    Plays D, C, C initially. Cooperates forever if opponent played D then C
    in moves 2 and 3. Otherwise plays TFT.

    Names:

    - Prober 2: [Prison1998]_
    """

    name = "Prober 2"
    classifier = {
        "stochastic": False,
        "memory_depth": float("inf"),  # Long memory
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        turn = len(self.history)
        if turn == 0:
            return D
        if turn == 1:
            return C
        if turn == 2:
            return C
        if turn > 2:
            if opponent.history[1:3] == [D, C]:
                return C
            else:
                # TFT
                return D if opponent.history[-1:] == [D] else C


class Prober3(Player):
    """
    Plays D, C initially. Defects forever if opponent played C in moves 2.
    Otherwise plays TFT.

    Names:

    - Prober 3: [Prison1998]_
    """

    name = "Prober 3"
    classifier = {
        "stochastic": False,
        "memory_depth": float("inf"),  # Long memory
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        turn = len(self.history)
        if turn == 0:
            return D
        if turn == 1:
            return C
        if turn > 1:
            if opponent.history[1] == C:
                return D
            else:
                # TFT
                return D if opponent.history[-1:] == [D] else C


class Prober4(Player):
    """
    Plays C, C, D, C, D, D, D, C, C, D, C, D, C, C, D, C, D, D, C, D initially.
    Counts retaliating and provocative defections of the opponent.
    If the absolute difference between the counts is smaller or equal to 2,
    defects forever.
    Otherwise plays C for the next 5 turns and TFT for the rest of the game.

    Names:

    - Prober 4: [Prison1998]_
    """

    name = "Prober 4"
    classifier = {
        "stochastic": False,
        "memory_depth": float("inf"),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        super().__init__()
        self.init_sequence = [
            C,
            C,
            D,
            C,
            D,
            D,
            D,
            C,
            C,
            D,
            C,
            D,
            C,
            C,
            D,
            C,
            D,
            D,
            C,
            D,
        ]
        self.just_Ds = 0
        self.unjust_Ds = 0
        self.turned_defector = False

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        if not self.history:
            return self.init_sequence[0]
        turn = len(self.history)
        if turn < len(self.init_sequence):
            if opponent.history[-1] == D:
                if self.history[-1] == D:
                    self.just_Ds += 1
                if self.history[-1] == C:
                    self.unjust_Ds += 1
            return self.init_sequence[turn]
        if turn == len(self.init_sequence):
            diff_in_Ds = abs(self.just_Ds - self.unjust_Ds)
            self.turned_defector = diff_in_Ds <= 2
        if self.turned_defector:
            return D
        if not self.turned_defector:
            if turn < len(self.init_sequence) + 5:
                return C
            return D if opponent.history[-1] == D else C


class HardProber(Player):
    """
    Plays D, D, C, C initially. Defects forever if opponent cooperated in moves
    2 and 3. Otherwise plays TFT.

    Names:

    - Hard Prober: [Prison1998]_
    """

    name = "Hard Prober"
    classifier = {
        "stochastic": False,
        "memory_depth": float("inf"),  # Long memory
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        turn = len(self.history)
        if turn == 0:
            return D
        if turn == 1:
            return D
        if turn == 2:
            return C
        if turn == 3:
            return C
        if turn > 3:
            if opponent.history[1:3] == [C, C]:
                return D
            else:
                # TFT
                return D if opponent.history[-1:] == [D] else C


class NaiveProber(Player):
    """
    Like tit-for-tat, but it occasionally defects with a small probability.

    Names:

    - Naive Prober: [Li2011]_
    """

    name = "Naive Prober"
    classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, p: float = 0.1) -> None:
        """
        Parameters
        ----------
        p, float
            The probability to defect randomly
        """
        super().__init__()
        self.p = p
        if (self.p == 0) or (self.p == 1):
            self.classifier["stochastic"] = False

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        # First move
        if len(self.history) == 0:
            return C
        # React to the opponent's last move
        if opponent.history[-1] == D:
            return D
        # Otherwise cooperate, defect with probability 1 - self.p
        if self.p == 0:
            return C
        if self.p == 1:
            return D
        choice = self._random.random_choice(1 - self.p)
        return choice


class RemorsefulProber(NaiveProber):
    """
    Like Naive Prober, but it remembers if the opponent responds to a random
    defection with a defection by being remorseful and cooperating.

    For reference see: [Li2011]_. A more complete description is given in "The
    Selfish Gene" (https://books.google.co.uk/books?id=ekonDAAAQBAJ):

    "Remorseful Prober remembers whether it has just spontaneously defected, and
    whether the result was prompt retaliation. If so, it 'remorsefully' allows
    its opponent 'one free hit' without retaliating."

    Names:

    - Remorseful Prober: [Li2011]_
    """

    name = "Remorseful Prober"
    classifier = {
        "memory_depth": 2,  # It remembers if its previous move was random
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, p: float = 0.1) -> None:
        super().__init__(p)
        self.probing = False

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        # First move
        if len(self.history) == 0:
            return C
        # React to the opponent's last move
        if opponent.history[-1] == D:
            if self.probing:
                self.probing = False
                return C
            return D

        # Otherwise cooperate with probability 1 - self.p
        if self.p == 1:
            self.probing = True
            return D
        elif self.p == 0 or self._random.random() < 1 - self.p:
            self.probing = False
            return C

        self.probing = True
        return D
