import unittest

from axelrod.game_params import PlayParams
from axelrod.ultimatum import SimpleThresholdPlayer
from axelrod.ultimatum.game_params import (
    UltimatumPosition,
    ultimatum_alternating_turns,
    ultimatum_static_turns,
)


class TestUltimatumGameParams(unittest.TestCase):
    def _build_params(self, offerer, decider):
        return PlayParams(
            player_positions={
                UltimatumPosition.OFFERER: offerer,
                UltimatumPosition.DECIDER: decider,
            }
        )

    def test_ultimatum_alternating_turns(self):
        player_1, player_2 = (
            SimpleThresholdPlayer(0.3),
            SimpleThresholdPlayer(0.7),
        )
        actual_turns = [
            x
            for x in ultimatum_alternating_turns([player_1, player_2], rounds=5)
        ]
        expected_turns = [
            self._build_params(player_1, player_2),
            self._build_params(player_2, player_1),
            self._build_params(player_1, player_2),
            self._build_params(player_2, player_1),
            self._build_params(player_1, player_2),
        ]

        self.assertListEqual(actual_turns, expected_turns)

    def test_ultimatum_static_turns(self):
        player_1, player_2 = (
            SimpleThresholdPlayer(0.3),
            SimpleThresholdPlayer(0.7),
        )
        actual_turns = [
            x
            for x in ultimatum_static_turns([player_1, player_2], rounds=3)
        ]
        expected_turns = [
            self._build_params(player_1, player_2),
            self._build_params(player_1, player_2),
            self._build_params(player_1, player_2),
        ]

        self.assertListEqual(actual_turns, expected_turns)
