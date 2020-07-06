"""Implements ipd_params, a single IPD instance of GameParams.

Because IPD is a symmetric 2-player game, we can use the round generator and
round player defined for general Symm2p games.  Additionally we define a
"result" function that translates Outcome into a pair of Actions to make this
backwards compatible with Match, which saves Match results as a pair of Actions.
"""

from typing import Tuple

from .action import Action
from .game_params import (
    GameParams,
    Symm2pPosition,
    symm2p_get_actions,
    symm2p_generate_play_params,
    symm2p_play_round
)
from .history import History
from .prototypes import Outcome


def ipd_result(outcome: Outcome) -> Tuple[Action, Action]:
    return (
        outcome.actions[Symm2pPosition.POS_1],
        outcome.actions[Symm2pPosition.POS_2],
    )


ipd_params = GameParams(
    game_type="IPD",
    generate_play_params=symm2p_generate_play_params,
    play_round=symm2p_play_round,
    get_actions=symm2p_get_actions,
    result=ipd_result,
)
