"""Prototypes for the various game components.

This is used for type annotations and deriving functions.
"""

from enum import Enum
from typing import Tuple, Union

from .action import Action

Position = Enum
Score = Union[float, int]


# TODO(5.0): Explore what functions should be shared for all players / all
#  scorers.
class BasePlayer(object):
    """A player for any game.  No gauranteed functionality."""
    pass


class BaseScorer(object):
    """Scorer function for any game.  Should at least include a score
    function."""
    def score(self, actions: Tuple[Action, ...]) -> Tuple[Score, ...]:
        """Taking player actions in some understood order, returns the scores
        in this round for the player taking that action (in the same order)."""
        raise NotImplementedError()  # pragma: no cover


@attr.s
class Outcome(object):
    """Describes the outcome of a single round of play.

    Attributes
    ----------
    actions : Dict[Position, Any]
        The chosen action for each player, keyed by the player's position.
    scores : Dict[Position, Score]
        The resulting score for the player, keyed by the player's position.
    position : Position
        An Outcome object will contain info about each position's action and
        score, but may also have a perspective indicating a single position.
        For example, when Outcome is stored to a player's history, position
        indicates which position that player played as on that turn.
    """

    # TODO(5.0): Change Any to Action, creating an ultimatum action.
    actions: Dict[Position, Any] = attr.ib()
    scores: Dict[Position, Score] = attr.ib()
    position: Optional[Position] = attr.ib(default=None)
