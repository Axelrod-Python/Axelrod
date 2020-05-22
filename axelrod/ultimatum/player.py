"""
Ultimatum Game.
"""

from collections import abc
from typing import List, Optional, Tuple

from axelrod.game_params import Position
from axelrod.prototypes import BasePlayer, Outcome


class UltimatumPosition(Position):
    OFFERER = 1
    DECIDER = 2


class History(abc.Sequence):
    """A history class for ultimatum player.

    Attributes
    ----------
    _history: List[Outcome]
        Outcome history for all previous rounds of play.
    _offer_history: List[Outcome]
        Outcome history for previous rounds of play in which the player was the
        offerer.
    _decide_history: List[Outcome]
        Outcome history for previous rounds of play in which the player was the
        decider.
    """

    def __init__(self):
        self._history: List[Outcome] = list()
        self._offer_history: List[Outcome] = list()
        self._decide_history: List[Outcome] = list()

    def append(self, outcome: Outcome) -> None:
        """Append the given Outcome to the history list, and to a sublist based
        on position of the Outcome."""
        self._history.append(outcome)
        if outcome.position == UltimatumPosition.OFFERER:
            self._offer_history.append(outcome)
        if outcome.position == UltimatumPosition.DECIDER:
            self._decide_history.append(outcome)

    def __getitem__(self, index):
        return self._history[index]

    def __len__(self) -> int:
        return len(self._history)

    @property
    def offers(self) -> List[Outcome]:
        return self._offer_history

    @property
    def decisions(self) -> List[Outcome]:
        return self._decide_history


class UltimatumPlayer(BasePlayer):
    """A generic abstract player of the ultimatum game."""

    name = "Ultimatum Player"

    # Possibly not always true, but set for now to prevent caching
    classifier = dict(stochastic=True)

    def __init__(self):
        self.history = History()

    def reset(self) -> None:
        self.history = History()

    def offer(self) -> float:
        """Returns a value between 0 and 1 for the proportion offered to the
        coplayer."""
        raise NotImplementedError

    def consider(self, offer: float) -> bool:
        """Decision rule for whether to accept the offer."""
        raise NotImplementedError

    def set_match_attributes(self, **match_attributes):
        pass

    def play(
        self, coplayer: "UltimatumPlayer", noise: Optional[float] = None
    ) -> Tuple[Outcome, Outcome]:
        """Play a game with this player as the offerer and the passed coplayer
        as the decider.  Appends Outcomes with offer decision and scores to the
        player's and coplayer's history, and returns."""
        offer = self.offer()
        decision = coplayer.consider(offer)
        # If the offer is accepted, return the split. Otherwise both players
        # receive nothing.
        if decision:
            scores = 1.0 - offer, offer
        else:
            scores = 0.0, 0.0

        actions = {
            UltimatumPosition.OFFERER: offer,
            UltimatumPosition.DECIDER: decision,
        }
        scores = {
            UltimatumPosition.OFFERER: scores[0],
            UltimatumPosition.DECIDER: scores[1],
        }
        outcome = Outcome(
            actions=actions, scores=scores, position=UltimatumPosition.OFFERER
        )
        coplayer_outcome = Outcome(
            actions=actions, scores=scores, position=UltimatumPosition.DECIDER
        )
        self.history.append(outcome)
        coplayer.history.append(coplayer_outcome)
        return outcome, coplayer_outcome
