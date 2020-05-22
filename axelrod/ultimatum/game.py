from typing import Tuple

from axelrod.prototypes import BaseScorer, Score


class UltimatumScorer(BaseScorer):
    def __init__(self):
        super().__init__()

    def score(self, offer_decision: Tuple) -> Tuple[Score, Score]:
        """Given offer and decision, returns the score to the offerer and
        decider, resp."""
        offer, decision = offer_decision
        if decision:
            return 1.0 - offer, offer
        return 0.0, 0.0
