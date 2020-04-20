from axelrod.ipd.action import Action
from axelrod.ipd.player import IpdPlayer

C, D = Action.C, Action.D


class Defector(IpdPlayer):
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
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    @staticmethod
    def strategy(opponent: IpdPlayer) -> Action:
        return D


class TrickyDefector(IpdPlayer):
    """A defector that is trying to be tricky.

    Names:

    - Tricky Defector: Original name by Karol Langner
    """

    name = "Tricky Defector"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: IpdPlayer) -> Action:
        """Almost always defects, but will try to trick the opponent into
        cooperating.

        Defect if opponent has cooperated at least once in the past and has
        defected for the last 3 turns in a row.
        """
        if opponent.history.cooperations > 0 and opponent.history[-3:] == [D] * 3:
            return C
        return D
