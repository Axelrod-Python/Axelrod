from types import FunctionType
from typing import Tuple

from axelrod._strategy_utils import thue_morse_generator
from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class SequencePlayer(Player):
    """Abstract base class for players that use a generated sequence to
    determine their plays.

    Names:

    - Sequence Player: Original name by Marc Harper
    """

    def __init__(
        self, generator_function: FunctionType, generator_args: Tuple = ()
    ) -> None:
        super().__init__()
        self.sequence_generator = generator_function(*generator_args)

    @staticmethod
    def meta_strategy(value: int) -> Action:
        """Determines how to map the sequence value to cooperate or defect.
        By default, treat values like python truth values. Override in child
        classes for alternate behaviors."""
        if value == 0:
            return D
        else:
            return C

    def strategy(self, opponent: Player) -> Action:
        # Iterate through the sequence and apply the meta strategy
        for s in self.sequence_generator:
            return self.meta_strategy(s)

    def __getstate__(self):
        """Generator attributes are not pickleable so we remove and rebuild."""
        return_dict = self.__dict__.copy()
        del return_dict["sequence_generator"]
        return return_dict

    def __setstate__(self, state):
        self.reset()
        self._history = state["_history"]
        self.match_attributes = state["match_attributes"]
        for _ in self.history:
            next(self.sequence_generator)


class ThueMorse(SequencePlayer):
    """
    A player who cooperates or defects according to the Thue-Morse sequence.
    The first few terms of the Thue-Morse sequence are:
    0 1 1 0 1 0 0 1 1 0 0 1 0 1 1 0 . . .

    Thue-Morse sequence: http://mathworld.wolfram.com/Thue-MorseSequence.html

    Names:

    - Thue Morse: Original name by Geraint Palmer
    """

    name = "ThueMorse"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        super().__init__(thue_morse_generator, (0,))


class ThueMorseInverse(ThueMorse):
    """ A player who plays the inverse of the Thue-Morse sequence.

    Names:

    - Inverse Thue Morse: Original name by Geraint Palmer
    """

    name = "ThueMorseInverse"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        super(ThueMorse, self).__init__(thue_morse_generator, (0,))

    @staticmethod
    def meta_strategy(value: int) -> Action:
        # Switch the default cooperate and defect action on 0 or 1
        if value == 0:
            return C
        else:
            return D
