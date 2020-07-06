"""Prototypes for the various game components.

This is used for type annotations and deriving functions.
"""

from collections import abc
import copy
from enum import Enum
from typing import Any, Dict, List, Optional, Text, Tuple, Union

import attr

PlayerName = Text
Position = Enum
Score = Union[float, int]

# TODO(5.0): Need to build this out.
BaseAction = Any


@attr.s
class Outcome(object):
    """Describes the outcome of a single round of play.

    Attributes
    ----------
    actions : Dict[Position, Any]
        The chosen action for each player, keyed by the player's position.
    scores : Optional[Dict[Position, Score]]
        The resulting score for the player, keyed by the player's position.
    position : Optional[Position]
        An Outcome object will contain info about each position's action and
        score, but may also have a perspective indicating a single position.
        For example, when Outcome is stored to a player's history, position
        indicates which position that player played as on that turn.
    """

    # TODO(5.0): Change Any to Action, creating an ultimatum action, throughout.
    actions: Dict[Position, Any] = attr.ib()
    scores: Optional[Dict[Position, Score]] = attr.ib(default=None)
    position: Optional[Position] = attr.ib(default=None)

    def play(self) -> Any:
        if not self.position:
            raise ValueError("No position set.")
        return self.actions[self.position]

    def coplay(self) -> Any:
        if not self.position:
            raise ValueError("No position set.")
        if len(self.actions) != 2:
            raise RuntimeError("Coplay not defined for multiplayer.")
        for k, v in self.actions.items():
            if k != self.position:
                return v


# TODO(5.0): Explore what functions should be shared for all players / all
#  scorers, and all histories.  Probably most of it.
class BaseHistory(abc.Sequence):
    """A class representing a player's history.

    The base class maintains a basic sequence of Outcomes.  The class can be
    derived to expand or change the behavior.
    """

    def __init__(self):
        self._history: List[Outcome] = list()

    def __getitem__(self, index):
        return self._history[index]

    def __len__(self) -> int:
        return len(self._history)

    def append(self, outcome: Outcome) -> None:
        """Append the given Outcome to the history list."""
        self._history.append(outcome)


class BasePlayer(object):
    """A player for any game."""

    classifier = dict()

    def __init__(self):
        if "game_params" not in self.__dict__:
            raise RuntimeError(  # pragma: no cover
                "game_params must be set before initializing parent."
            )
        self._history = self.history_factory()
        self.classifier = copy.deepcopy(self.classifier)

    def history_factory(self):
        """Generates a history class.

        Must be overwritten for each derived Player class.
        """
        return BaseHistory()

    def reset(self) -> None:
        self._history = self.history_factory()

    def update_outcome_history(self, outcome):
        """Updates history using an outcome."""
        self._history.append_outcome(outcome)

    # TODO(5.0): Will need to think about how to generalize to three players.
    def play(self, coplayer, noise=0):
        """This pits two players against each other."""
        # Get one round of play
        round_params = next(
            self.game_params.generate_play_params([self, coplayer], 1)
        )
        # TODO(5.0): I'd like to provide a scorer here.  Need to rethink
        #  makes_use_of["game"].  Otherwise should remove score from Outcome,
        #  which isn't being used.
        actions = self.game_params.get_actions(round_params, noise=noise)
        outcome = Outcome(actions=actions)

        # Update histories
        for pos, player in round_params.player_positions.items():
            outcome_copy = copy.copy(outcome)
            outcome_copy.position = pos
            player.update_outcome_history(outcome_copy)
            if player is self:
                result = outcome_copy

        return self.game_params.result(result)

    @property
    def history(self):
        return self._history


class BaseScorer(object):
    """Scorer function for any game.  Should at least include a score
    function."""

    def score(self, actions: Tuple[BaseAction, ...]) -> Tuple[Score, ...]:
        """Taking player actions in some understood order, returns the scores
        in this round for the player taking that action (in the same order).

        Parameters
        ----------
        actions: tuple(Action, BaseAction)
            A pair actions for two players, for example (C, C).

        Returns
        -------
        tuple of int or float
            Scores for two player resulting from their actions.
        """
        raise NotImplementedError()  # pragma: no cover
