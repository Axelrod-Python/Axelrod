from typing import Any, Dict, Tuple

from axelrod.prototypes import BaseScorer, Score
from .position import UltimatumPosition


class UltimatumScorer(BaseScorer):
    def __init__(self):
        super().__init__()

    def score(self, offer_decision: Tuple) -> Tuple[Score, Score]:
        """Expects actions as offer first, then decision."""
        offer, decision = offer_decision
        if decision:
            return 1.0 - offer, offer
        return 0.0, 0.0
