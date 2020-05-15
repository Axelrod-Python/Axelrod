"""
Ultimatum Game.
"""

from collections import abc
from enum import Enum
from typing import List, Optional, Tuple

import attr
from scipy import stats


class PlayerPosition(Enum):
    OFFERER = 1
    DECIDER = 2


@attr.s
class Outcome(object):
    position: PlayerPosition = attr.ib()
    offer: float = attr.ib()
    decision: bool = attr.ib()
    scores: Tuple[float, float] = attr.ib()


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
        """Append the given outcome to the history list, and to a sublist based
        on position of the outcome."""
        self._history.append(outcome)
        if outcome.position == PlayerPosition.OFFERER:
            self._offer_history.append(outcome)
        if outcome.position == PlayerPosition.DECIDER:
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


class UltimatumPlayer(object):
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

    def last_offer(self) -> Optional[Outcome]:
        """Look for most recent Outcome in which this player was the offerer.
        Returns None if no such Outcome exists."""
        for hist in reversed(self.history):
            if hist.position == PlayerPosition.OFFERER:
                return hist

    def symmetric_play(
        self, coplayer: "UltimatumPlayer", noise: Optional[float] = None
    ) -> Tuple[Tuple[Outcome, Outcome], Tuple[Outcome, Outcome]]:
        """Play two games agianst the passed coplayer.  In the first, this
        player will be the offerer and the coplayer will be the decider.  In
        the second, the roles will be switched."""
        player_outcome_1, coplayer_outcome_1 = self.play(coplayer, noise=noise)
        coplayer_outcome_2, player_outcome_2 = coplayer.play(self, noise=noise)
        return (
            (player_outcome_1, player_outcome_2),
            (coplayer_outcome_1, coplayer_outcome_2),
        )

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
        outcome = Outcome(
            position=PlayerPosition.OFFERER,
            offer=offer,
            decision=decision,
            scores=scores,
        )
        coplayer_outcome = Outcome(
            position=PlayerPosition.DECIDER,
            offer=offer,
            decision=decision,
            scores=list(reversed(scores)),
        )
        self.history.append(outcome)
        coplayer.history.append(coplayer_outcome)
        return outcome, coplayer_outcome


class ConsiderThresholdPlayer(object):
    """Creates the consider function of an ultimatum player that only accepts
    offer in the provided thresholds."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lower_threshold, self.upper_threshold = None, None

    def set_thresholds(self, lower: float, upper: float = 1.0) -> None:
        self.lower_threshold, self.upper_threshold = lower, upper

    def consider(self, offer: float) -> bool:
        assert self.lower_threshold is not None
        return self.lower_threshold <= offer <= self.upper_threshold


class SimpleThresholdPlayer(ConsiderThresholdPlayer, UltimatumPlayer):
    """A simple Ultimatum game player with a fixed acceptance threshold and
    offer proportion.

    Source: Axelrod library
    """

    name = "Simple Threshold Player"

    def __init__(
        self, offer_proportion: float = 0.5, lower_threshold: float = 0.5
    ):
        super().__init__()
        self.offer_proportion = offer_proportion
        self.set_thresholds(lower_threshold)

    def __repr__(self) -> str:
        return "SimpleThresholdPlayer ({} | {})".format(
            self.offer_proportion, self.lower_threshold
        )

    def offer(self) -> float:
        return self.offer_proportion


class AcceptanceThresholdPlayer(ConsiderThresholdPlayer, UltimatumPlayer):
    """A simple Ultimatum game player with fixed acceptance thresholds (upper
    and lower) and a fixed offer proportion.

    Source: Axelrod library
    """

    name = "Acceptance Threshold Player"

    def __init__(
        self,
        offer_proportion: float = 0.5,
        lower_threshold: float = 0.5,
        upper_threshold: float = 0.5,
    ):
        super().__init__()
        self.offer_proportion = offer_proportion
        self.set_thresholds(lower_threshold, upper_threshold)

    def __repr__(self) -> str:
        return "AcceptanceThresholdPlayer ({} | [{}, {}])".format(
            self.offer_proportion, self.lower_threshold, self.upper_threshold
        )

    def offer(self) -> float:
        return self.offer_proportion


class DoubleThresholdsPlayer(ConsiderThresholdPlayer, UltimatumPlayer):
    """A simple Ultimatum game player with fixed acceptance thresholds (upper
    and lower) and a fixed offer proportion.

    Source: Axelrod library
    """

    name = "Double Thresholds Player"

    classifier = dict(stochastic=True)

    def __init__(
        self,
        lower_offer: float = 0.4,
        upper_offer: float = 0.6,
        lower_accept: float = 0.4,
        upper_accept: float = 0.6,
    ):
        super().__init__()
        self.lower_offer = lower_offer
        self.upper_offer = upper_offer
        self.set_thresholds(lower_accept, upper_accept)
        self.offer_distribution = stats.uniform(
            loc=lower_offer, scale=upper_offer - lower_offer
        )
        self.init_kwargs = dict(
            lower_offer=lower_offer,
            upper_offer=upper_offer,
            lower_accept=lower_accept,
            upper_accept=upper_accept,
        )

    def __repr__(self) -> str:
        return "DoubleThresholdsPlayer ({}, {} | [{}, {}])".format(
            self.lower_offer,
            self.upper_offer,
            self.init_kwargs["lower_accept"],
            self.init_kwargs["upper_accept"],
        )

    def offer(self) -> float:
        # print(self.lower_offer, self.upper_offer)
        return self.offer_distribution.rvs()


class DistributionPlayer(UltimatumPlayer):
    """A stochastic player of the ultimatum game.

    Source: Axelrod library
    """

    name = "Distribution Player"

    def __init__(
        self,
        offer_distribution: Optional[stats.distributions.rv_continuous] = None,
        acceptance_distribution: Optional[
            stats.distributions.rv_continuous
        ] = None,
    ):
        super().__init__()
        if not offer_distribution:
            offer_distribution = stats.norm(0.5, 0.1)  # pragma: no cover
        if not acceptance_distribution:
            acceptance_distribution = stats.norm(0.5, 0.1)  # pragma: no cover
        self.offer_distribution = offer_distribution
        self.acceptance_distribution = acceptance_distribution

    def __repr__(self) -> str:
        return "DistributionThresholdPlayer"

    def offer(self) -> float:
        return self.offer_distribution.rvs()

    def consider(self, offer: float) -> bool:
        return self.acceptance_distribution.rvs() <= offer


class BinarySearchOfferPlayer(ConsiderThresholdPlayer, UltimatumPlayer):
    """Adjusts offers in a binary search fashion to try to find a lowest-
    acceptable offer.  Considers offers similar to DoubleThresholdsPlayer.

    Source: Axelrod library
    """

    name = "Binary Search Offers Player"

    def __init__(
        self, lower_threshold: float = 0.5, upper_threshold: float = 1.0,
    ):
        super().__init__()
        self.set_thresholds(lower_threshold, upper_threshold)
        self.offer_size = 0.5
        self.step_size = 0.25

    def __repr__(self) -> str:
        return "BinarySearchOfferPlayer [{}, {}]".format(
            self.lower_threshold, self.upper_threshold
        )

    def offer(self) -> float:
        if self.history.offers:
            # If prior offer was accepted offer less; otherwise more
            delta = self.step_size * (
                -1 if self.history.offers[-1].decision else 1
            )
            self.offer_size += delta
            self.step_size *= 0.5

        return self.offer_size
