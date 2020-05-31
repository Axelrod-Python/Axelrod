import unittest

import axelrod as axl
from axelrod.prototypes import Outcome
from axelrod.ultimatum.game import UltimatumScorer
from axelrod.ultimatum.game_params import ultimatum_alternating_params
from axelrod.ultimatum import SimpleThresholdPlayer, UltimatumPosition


class TestUltimatumMatch(unittest.TestCase):
    def test_match_of_simple_threshold_players(self):
        generous = SimpleThresholdPlayer(1.0)
        stingy = SimpleThresholdPlayer(0.0)

        # TODO(5.0): Hack to keep deterministic cache from running.  Doesn't
        #  work with ultimatum yet.
        generous.classifier["stochastic"] = True

        match = axl.Match(
            players=[generous, stingy],
            turns=2,
            game=UltimatumScorer(),
            game_params=ultimatum_alternating_params,
        )

        results = match.play()

        # TODO(5.0): Other match functions for reporting don't work.  List of
        #  Outcomes is hard to parse.
        for i in [0, 1]:
            self.assertDictEqual(
                results[0][i].actions,
                {
                    UltimatumPosition.OFFERER: 1.0,
                    UltimatumPosition.DECIDER: True,
                },
            )
            self.assertDictEqual(
                results[1][i].actions,
                {
                    UltimatumPosition.OFFERER: 0.0,
                    UltimatumPosition.DECIDER: False,
                },
            )
