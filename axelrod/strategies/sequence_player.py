from axelrod.actions import Actions, Action
from axelrod.player import Player
from axelrod._strategy_utils import thue_morse_generator

from types import FunctionType
from typing import Tuple

C, D = Actions.C, Actions.D


class SequencePlayer(Player):
    """Abstract base class for players that use a generated sequence to
    determine their plays.

    Names:

    - Sequence Player: Original name by Marc Harper
    """

    def __init__(self, generator_function: FunctionType,
                 generator_args: Tuple = ()) -> None:
        super().__init__()
        # Initialize the sequence generator
        self.generator_function = generator_function
        self.generator_args = generator_args
        self.sequence_generator = self.generator_function(*self.generator_args)

    def meta_strategy(self, value: int) -> None:
        """Determines how to map the sequence value to cooperate or defect.
        By default, treat values like python truth values. Override in child
        classes for alternate behaviors."""
        if value == 0:
            return Actions.D
        else:
            return Actions.C

    def strategy(self, opponent: Player) -> Action:
        # Iterate through the sequence and apply the meta strategy
        for s in self.sequence_generator:
            return self.meta_strategy(s)

    def reset(self):
        # Be sure to reset the sequence generator
        super().reset()
        self.sequence_generator = self.generator_function(*self.generator_args)


class ThueMorse(SequencePlayer):
    """
    A player who cooperates or defects according to the Thue-Morse sequence.
    The first few terms of the Thue-Morse sequence are:
    0 1 1 0 1 0 0 1 1 0 0 1 0 1 1 0 . . .

    Thue-Morse sequence: http://mathworld.wolfram.com/Thue-MorseSequence.html

    Names:

    - Thue Morse: Original name by Geraint Palmer
    """

    name = 'ThueMorse'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__(thue_morse_generator, (0,))


class ThueMorseInverse(ThueMorse):
    """ A player who plays the inverse of the Thue-Morse sequence.

    Names:

    - Inverse Thue Morse: Original name by Geraint Palmer
    """

    name = 'ThueMorseInverse'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super(ThueMorse, self).__init__(thue_morse_generator, (0,))

    def meta_strategy(self, value: int) -> Action:
        # Switch the default cooperate and defect action on 0 or 1
        if value == 0:
            return C
        else:
            return D
