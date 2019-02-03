"""
Ultimatum Game .
"""

from collections import namedtuple
from enum import Enum
from scipy import stats


class PlayerPosition(Enum):
    OFFERER = 1
    DECIDER = 2


# Python 3.7 dataclass would be nice here
Outcome = namedtuple('Outcome', ['position', 'offer', 'decision', 'scores'])


class UltimatumPlayer(object):
    """A generic abstract player of the ultimatum game."""

    name = "Ultimatum Player"

    # Possibly not always true, but set for now to prevent caching
    classifier = dict(stochastic=True)

    def __init__(self):
        self.history = []

    def set_match_attributes(self, *args, **kwargs):
        pass

    def reset(self):
        self.history = []

    def offer(self) -> float:
        """Returns a value between 0 and 1 for the proportion offered to the
        coplayer."""
        raise NotImplementedError

    def consider(self, offer: float) -> bool:
        """Decision rule for whether to accept the offer."""
        raise NotImplementedError

    def play(self, coplayer, noise=None):
        offer = self.offer()
        decision = coplayer.consider(offer)
        # If the offer is accepted, return the split. Otherwise both players
        # receive nothing.
        if decision:
            scores = 1. - offer, offer
        else:
            scores = 0., 0.
        outcome = Outcome(
            position=PlayerPosition.OFFERER,
            offer=offer,
            decision=decision,
            scores=scores
        )
        coplayer_outcome = Outcome(
            position=PlayerPosition.DECIDER,
            offer=offer,
            decision=decision,
            scores=list(reversed(scores))
        )
        self.history.append(outcome)
        coplayer.history.append(coplayer_outcome)
        return outcome, coplayer_outcome


class SimpleThresholdPlayer(UltimatumPlayer):
    """A simple Ultimatum game player with a fixed acceptance threshold and
    offer proportion."""

    name = "Simple Threshold Player"

    def __init__(self, offer_proportion=0.5, lower_threshold=0.5):
        self.offer_proportion = offer_proportion
        self.lower_threshold = lower_threshold

    def __repr__(self) -> str:
        return "SimpleThresholdPlayer ({} | {})".format(
            self.offer_proportion, self.lower_threshold)

    def offer(self) -> float:
        return self.offer_proportion

    def consider(self, offer: float) -> bool:
        return offer >= self.lower_threshold


class AcceptanceThresholdPlayer(UltimatumPlayer):
    """A simple Ultimatum game player with fixed acceptance thresholds (upper
    and lower) and a fixed offer proportion."""

    name = "Double Threshold Player"

    def __init__(self, offer_proportion, lower_threshold, upper_threshold):
        self.offer_proportion = offer_proportion
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

    def __repr__(self) -> str:
        return "DoubleThresholdPlayer ({} | [{}, {}])".format(
            self.offer_proportion,
            self.lower_threshold,
            self.upper_threshold)

    def offer(self) -> float:
        return self.offer_proportion

    def consider(self, offer: float) -> bool:
        return (offer >= self.lower_threshold) and (
            offer <= self.upper_threshold)


class DoubleThresholdsPlayer(UltimatumPlayer):
    """A simple Ultimatum game player with fixed acceptance thresholds (upper
    and lower) and a fixed offer proportion."""

    name = "Double Thresholds Player"

    classifier = dict(stochastic=True)

    def __init__(self, lower_offer, upper_offer, lower_accept, upper_accept):
        self.lower_offer = lower_offer
        self.upper_offer = upper_offer
        self.lower_accept = lower_accept
        self.upper_accept = upper_accept
        self.offer_distribution = stats.uniform(
            loc=lower_offer, scale=upper_offer - lower_offer)

    def __repr__(self) -> str:
        return "DoubleThresholdsPlayer ({}, {} | [{}, {}])".format(
            self.lower_offer,
            self.upper_offer,
            self.lower_accept,
            self.upper_accept
        )

    def offer(self) -> float:
        return self.offer_distribution.rvs()

    def consider(self, offer: float) -> bool:
        return (offer >= self.lower_accept) and (
            offer <= self.upper_accept)


# class DistributionPlayer(UltimatumPlayer):
#     """A stochastic player of the ultimatum game."""
#
#     name = "Distribution Player"
#
#     def __init__(self, offer_distribution: None, acceptance_distribution=None):
#         if not offer_distribution:
#             offer_distribution = stats.norm(0.5, 0.1)
#         if not acceptance_distribution:
#             acceptance_distribution = stats.norm(0.5, 0.1)
#         self.offer_distribution = offer_distribution
#         self.acceptance_distribution = acceptance_distribution
#
#     def __repr__(self) -> str:
#         return "DistributionThresholdPlayer"
#
#     def offer(self) -> float:
#         return self.offer_distribution.rvs()
#
#     def consider(self, offer: float) -> bool:
#         return self.acceptance_distribution.rvs() <= offer


