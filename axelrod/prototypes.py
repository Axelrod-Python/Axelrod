"""Prototypes for the various game components."""

from enum import Enum
from typing import Tuple, Union

from .action import Action

Position = Enum
Score = Union[float, int]


class BasePlayer(object):
    def strategy(self, opponent: "BasePlayer") -> Action:
        raise NotImplementedError()  # pragma: no cover


class BaseScorer(object):
    def score(self, actions: Tuple[Action, ...]) -> Tuple[Score, ...]:
        raise NotImplementedError()  # pragma: no cover
