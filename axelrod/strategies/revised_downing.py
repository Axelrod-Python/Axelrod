"""
Revised Downing implemented from the Fortran source code for the second of
Axelrod's tournaments.
"""
from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class RevisedDowning(Player):
    """
    Strategy submitted to Axelrod's second tournament by Leslie Downing.
    (K59R).

    Revised Downing attempts to determine if players are cooperative or not.
    If so, it cooperates with them.

    This strategy is a revision of the strategy submitted by Downing to
    Axelrod's first tournament.


    Names:
    - Revised Downing: [Axelrod1980]_
    """

    name = "Revised Downing"

    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        super().__init__()
        self.good = 1.0
        self.bad = 0.0
        self.nice1 = 0
        self.nice2 = 0
        self.total_C = 0  # note the same as self.cooperations
        self.total_D = 0  # note the same as self.defections

    def strategy(self, opponent: Player) -> Action:
        round_number = len(self.history) + 1

        if round_number == 1:
            return C

        # Update various counts
        if round_number > 2:
            if self.history[-2] == D:
                if opponent.history[-1] == C:
                    self.nice2 += 1
                self.total_D += 1
                self.bad = self.nice2 / self.total_D
            else:
                if opponent.history[-1] == C:
                    self.nice1 += 1
                self.total_C += 1
                self.good = self.nice1 / self.total_C
        # Make a decision based on the accrued counts
        c = 6.0 * self.good - 8.0 * self.bad - 2
        alt = 4.0 * self.good - 5.0 * self.bad - 1
        if c >= 0 and c >= alt:
            move = C
        elif (c >= 0 and c < alt) or (alt >= 0):
            move = self.history[-1].flip()
        else:
            move = D
        return move
