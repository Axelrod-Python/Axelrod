"""..........."""

from typing import List

from axelrod.prototypes import BaseHistory, Outcome
from .position import UltimatumPosition


# TODO(5.0): History and Outcomes have proven to not be that user-friendly.
#  Explore different APIs.
class UltimatumHistory(BaseHistory):
    """A history class for ultimatum player.

    The parent class continues to manage self._history, but this derived class
    adds extra breakdowns.

    Attributes
    ----------
    _offer_history: List[Outcome]
        Outcome history for previous rounds of play in which the player was the
        offerer.
    _decide_history: List[Outcome]
        Outcome history for previous rounds of play in which the player was the
        decider.
    """

    def __init__(self):
        self._offer_history: List[Outcome] = list()
        self._decide_history: List[Outcome] = list()
        super().__init__()

    def append_outcome(self, outcome: Outcome) -> None:
        """Append to a sublist based on position of the Outcome."""
        if outcome.position == UltimatumPosition.OFFERER:
            self._offer_history.append(outcome)
        if outcome.position == UltimatumPosition.DECIDER:
            self._decide_history.append(outcome)
        super().append(outcome)

    @property
    def offers(self) -> List[Outcome]:
        return self._offer_history

    @property
    def decisions(self) -> List[Outcome]:
        return self._decide_history
