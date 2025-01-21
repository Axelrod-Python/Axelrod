from axelrod.action import Action
from axelrod.player import Player
import statistics

C, D = Action.C, Action.D


class Defector(Player):
    """A player who only ever defects.

    Names:

    - Defector: [Axelrod1984]_
    - ALLD: [Press2012]_
    - Always defect: [Mittal2009]_
    """

    name = "Defector"
    classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        return D


class TrickyDefector(Player):
    """A defector that is trying to be tricky.

    Names:

    - Tricky Defector: Original name by Karol Langner
    """

    name = "Tricky Defector"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        """Almost always defects, but will try to trick the opponent into
        cooperating.

        Defect if opponent has cooperated at least once in the past and has
        defected for the last 3 turns in a row.
        """
        if (
            opponent.history.cooperations > 0
            and opponent.history[-3:] == [D] * 3
        ):
            return C
        return D


class ModalDefector(Player):
    """
    A player starts by Defecting and then analyses the history of the opponent. If the opponent Cooperated in the
    last round, they are returned with a Defection. If the opponent chose to Defect in the previous round,
    then this strategy will return with the mode of the previous opponent responses.
    """

    # These are various properties for the strategy
    name = "Modal Defector"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        """This is the actual strategy"""
        # First move
        if not self.history:
            return D
        # React to the opponent's historical moves
        if opponent.history[-1] == C:
            return D
        else:
            # returns with the mode of the opponent's history.
            return statistics.mode(opponent.history)

