"""Actions for the Prisoner's Dilemma and related utilities.

For convenience in other modules you can alias the actions:

from axelrod import Action
C, D = Action.C, Action.D
"""

from enum import Enum
from functools import total_ordering
from typing import Iterable


class UnknownActionError(ValueError):
    """Error indicating an unknown action was used."""

    def __init__(self, *args):
        super(UnknownActionError, self).__init__(*args)


@total_ordering
class Action(Enum):
    """Core actions in the Prisoner's Dilemna.
    
    There are only two possible actions, namely Cooperate or Defect,
    which are called C and D for convenience.
    """

    C = 1  # Cooperate
    D = 0  # Defect

    def __bool__(self):
        return bool(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return "{}".format(self.name)

    def __str__(self):
        return "{}".format(self.name)

    def flip(self):
        """Returns the opposite Action."""
        if self == Action.C:
            return Action.D
        if self == Action.D:
            return Action.C

    @classmethod
    def from_char(cls, character):
        """Converts a single character into an Action.
        
        Parameters
        ----------
        character: a string of length one

        Returns
        -------
        Action
            The action corresponding to the input character


        Raises
        ------
        UnknownActionError
            If the input string is not 'C' or 'D'
        """
        if character == "C":
            return cls.C
        if character == "D":
            return cls.D
        raise UnknownActionError('Character must be "C" or "D".')


def str_to_actions(actions: str) -> tuple:
    """Converts a string to a tuple of actions.

    Parameters
    ----------
    actions: string consisting of 'C's and 'D's

    Returns
    -------
    tuple
        Each element corresponds to a letter from the input string.
    """
    return tuple(Action.from_char(element) for element in actions)


def actions_to_str(actions: Iterable[Action]) -> str:
    """Converts an iterable of actions into a string.

    Example: (D, D, C) would be converted to 'DDC'

    Paramteters
    -----------
    actions: iterable of Action

    Returns
    -------
    str
        A string of 'C's and 'D's.
    """
    return "".join(map(repr, actions))
