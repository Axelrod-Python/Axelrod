"""Implements two GameParams for Ultimatum:  One for matches where the players
alternate roles, and one for matches where the players keep roles.

In both cases, playing a round involves having the Offerer extend an offer to
the Decider.
"""

from copy import copy
from typing import Any, Dict, Generator, List, Optional, Tuple

from axelrod.game_params import GameParams, PlayParams, x_plays_y_round
from axelrod.prototypes import BaseAction, BaseScorer, Outcome
from .history import UltimatumHistory
from .position import UltimatumPosition


def ultimatum_alternating_turns(
    players: List["UltimatumPlayer"], rounds: int
) -> Generator[PlayParams, None, None]:
    """Alternate roles between two players, with the first player offering
    first."""
    assert len(players) == 2
    player_positions = {
        UltimatumPosition.OFFERER: players[0],
        UltimatumPosition.DECIDER: players[1],
    }
    for _ in range(rounds):
        yield PlayParams(player_positions=player_positions)
        player_positions = {
            UltimatumPosition.OFFERER: player_positions[
                UltimatumPosition.DECIDER
            ],
            UltimatumPosition.DECIDER: player_positions[
                UltimatumPosition.OFFERER
            ],
        }


def ultimatum_static_turns(
    players: List["UltimatumPlayer"], rounds: int
) -> Generator[PlayParams, None, None]:
    """First player offers, and second play decides.  No role change."""
    assert len(players) == 2
    player_positions = {
        UltimatumPosition.OFFERER: players[0],
        UltimatumPosition.DECIDER: players[1],
    }
    for _ in range(rounds):
        yield PlayParams(player_positions=player_positions)


def ultimatum_play_round(
    params: PlayParams,
    scorer: Optional[BaseScorer] = None,
    noise: Optional[float] = None,
) -> Outcome:
    # TODO(5.0): There is a probably a cleaner way to implement.
    def outcomes_to_actions(
        outcome_1: Outcome, outcome_2: Outcome
    ) -> Tuple[Any]:
        action_1 = outcome_1.actions[outcome_1.position]
        action_2 = outcome_2.actions[outcome_2.position]
        return action_1, action_2

    # Offerer plays against decider.
    return x_plays_y_round(
        UltimatumPosition.OFFERER,
        UltimatumPosition.DECIDER,
        params,
        scorer=scorer,
        outcomes_to_actions=outcomes_to_actions,
        noise=noise,
    )


def ultimatum_get_actions(
    params: PlayParams, noise: Optional[float] = None
) -> Dict[UltimatumPosition, BaseAction]:
    offerer, decider = (
        params.player_positions[UltimatumPosition.OFFERER],
        params.player_positions[UltimatumPosition.DECIDER],
    )
    offer = offerer.offer()
    decision = decider.consider(offer)
    return {
        UltimatumPosition.OFFERER: offer,
        UltimatumPosition.DECIDER: decision,
    }


def ultimatum_result(outcome: Outcome) -> Tuple[Outcome, Outcome]:
    second_outcome = copy(outcome)
    second_outcome.position = (
        UltimatumPosition.OFFERER
        if outcome.position == UltimatumPosition.DECIDER
        else UltimatumPosition.DECIDER
    )
    return outcome, second_outcome


ultimatum_alternating_params = GameParams(
    game_type="Ultimatum",
    generate_play_params=ultimatum_alternating_turns,
    play_round=ultimatum_play_round,
    get_actions=ultimatum_get_actions,
    result=ultimatum_result,
)


ultimatum_static_params = GameParams(
    game_type="Ultimatum",
    generate_play_params=ultimatum_static_turns,
    play_round=ultimatum_play_round,
    get_actions=ultimatum_get_actions,
    result=ultimatum_result,
)
