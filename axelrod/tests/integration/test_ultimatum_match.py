import unittest

import axelrod as axl
from axelrod.prototypes import Outcome
from axelrod.ultimatum.game import UltimatumScorer
from axelrod.ultimatum.game_params import ultimatum_alternating_params
from axelrod.ultimatum.player import UltimatumPosition
from axelrod.ultimatum.strategies import SimpleThresholdPlayer


class TestUltimatumMatch(unittest.TestCase):
    def _build_outcome(self, offer, decision, offer_score, decision_score):
        return Outcome(
            actions={
                UltimatumPosition.OFFERER: offer,
                UltimatumPosition.DECIDER: decision,
            },
            scores={
                UltimatumPosition.OFFERER: offer_score,
                UltimatumPosition.DECIDER: decision_score,
            },
        )

    def test_match_of_simple_threshold_players(self):
        generous = SimpleThresholdPlayer(1.0)
        stingy = SimpleThresholdPlayer(0.0)

        # TODO(5.0): Hack to keep deterministic cache from running.  Doesn't
        # work with ultimatum yet.
        generous.classifier["stochastic"] = True

        match = axl.Match(
            players=[generous, stingy],
            turns=2,
            game=UltimatumScorer(),
            game_params=ultimatum_alternating_params,
        )

        # TODO(5.0): Other match functions for reporting don't work.  List of
        # Outcomes is hard to parse.
        self.assertListEqual(
            match.play(),
            [
                self._build_outcome(1.0, True, 0.0, 1.0),
                self._build_outcome(0.0, False, 0.0, 0.0),
            ],
        )
