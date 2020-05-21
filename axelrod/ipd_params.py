"""Implements ipd_params."""

from typing import Tuple

from .action import Action
from .game_params import GameParams, Outcome, Symm2pPosition, symm2p_generate_play_params, symm2p_play_round


def ipd_result(outcome: Outcome) -> Tuple[Action, Action]:
    return (
        outcome.actions[Symm2pPosition.POS_1],
        outcome.actions[Symm2pPosition.POS_2],
    )


ipd_params = GameParams(
    game_type="IPD",
    generate_play_params=symm2p_generate_play_params,
    play_round=symm2p_play_round,
    result=ipd_result,
)
