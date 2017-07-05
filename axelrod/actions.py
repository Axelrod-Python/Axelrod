"""
Defines the core actions for the Prisoner's Dilemma:
* Cooperate
* Defect

Uses the enumeration, Action.C and Action.D. For convenience you can use:

from axelrod import Action
C, D = Action.C, Action.D
"""

from enum import Enum
from typing import Iterable


class UnknownActionError(ValueError):
    def __init__(self, *args):
        super(UnknownActionError, self).__init__(*args)


class Action(Enum):

    C = 1
    D = 0

    def __bool__(self):
        return bool(self.value)

    def __repr__(self):
        return '{}'.format(self.name)

    def __str__(self):
        return '{}'.format(self.name)

    def flip(self):
        """Returns the opposite Action. """
        if self == Action.C:
            return Action.D
        if self == Action.D:
            return Action.C

    @classmethod
    def from_char(cls, character):
        """Converts a single character into an Action. `Action.from_char('C')`
        returns `Action.C`. `Action.from_char('CC')` raises an error. Use
        `str_to_actions` instead."""
        if character == 'C':
            return cls.C
        elif character == 'D':
            return cls.D
        else:
            raise UnknownActionError('Character must be "C" or "D".')


def str_to_actions(actions: str) -> tuple:
    """Takes a string like 'CCDD' and returns a tuple of the appropriate
    actions."""
    return tuple(Action.from_char(element) for element in actions)


def actions_to_str(actions: Iterable[Action]) -> str:
    """Takes any iterable of Action and returns a string of 'C's
    and 'D's.  ex: (D, D, C) -> 'DDC' """
    return "".join(map(repr, actions))
