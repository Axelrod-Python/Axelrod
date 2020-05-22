"""Implements GameParams and other classes.

The GameParams class defines all everything a program should need to understand
a game (e.g. IPD or ultimatum).
"""

from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Text,
    Tuple
)

import attr

from .prototypes import BasePlayer, BaseScorer, Position, Score


@attr.s
class PlayParams(object):
    """Parameters controlling a single round of play.

    Attributes
    ----------
    player_positions : Dict[Position, Player]
        Specifies the player that's going to play each of the positions.
    """

    player_positions: Dict[Position, BasePlayer] = attr.ib()


@attr.s
class Outcome(object):
    """Describes the outcome of a single round of play.

    Attributes
    ----------
    actions : Dict[Position, Any]
        The chosen action for each player, keyed by the player's position.
    scores : Dict[Position, Score]
        The resulting score for the player, keyed by the player's position.
    position : Position
        An Outcome object will contain info about each position's action and
        score, but may also have a perspective indicating a single position.
        For example, when Outcome is stored to a player's history, position
        indicates which position that player played as on that turn.
    """

    # TODO: Change Any to Action, creating an ultimatum action.
    actions: Dict[Position, Any] = attr.ib()
    scores: Dict[Position, Score] = attr.ib()
    position: Optional[Position] = attr.ib(default=None)


@attr.s
class GameParams(object):
    """Parameters describing a game type (like IPD or ultimatum).

    Attributes
    ----------
    game_type : Text
        Unique name for the type of game (IPD, Ultimatum, etc.)
    generate_play_params : Callable[
        [List[BasePlayer], int], Generator[PlayParams, None, None]
    ]
        A function that takes a list of players and an integer representing the
        number of turns, yields PlayParams for rounds of play for as long as a
        match should last.
    play_round : Callable[[PlayParams, Game], Outcome]
        A function that given a PlayParams and a Game object will play a single
        round of the game, and returns the Outcome object.
    result : Callable[[Outcome], Any]
        Translates an Outcome object to a result that the match's play method
        returns.  By default, this is a pass-through.
    """

    game_type: Text = attr.ib()
    generate_play_params: Callable[
        [List[BasePlayer], int], Generator[PlayParams, None, None]
    ] = attr.ib()
    play_round: Callable[[PlayParams, BaseScorer], Outcome] = attr.ib()
    result: Callable[[Outcome], Any] = attr.ib(default=lambda x: x)


class Symm2pPosition(Position):
    """A position enum for symmetric 2-player games.

    "Symmetric" means that the positions are interchangeable.
    """

    POS_1 = 1
    POS_2 = 2


def symm2p_generate_play_params(
    players: List[BasePlayer], rounds: int
) -> Generator[PlayParams, None, None]:
    assert len(players) == 2
    player_positions = {
        Symm2pPosition.POS_1: players[0],
        Symm2pPosition.POS_2: players[1],
    }
    for _ in range(rounds):
        yield PlayParams(player_positions=player_positions)


def x_plays_y_round(
    x: Position,
    y: Position,
    params: PlayParams,
    scorer: BaseScorer,
    outcomes_to_actions: Optional[
        Callable[[Outcome, Outcome], Tuple[Any, Any]]
    ] = None,
    noise: Optional[float] = None,
) -> Outcome:
    """Calls play on player in position x, with the player in position y
    passed in."""
    if not outcomes_to_actions:
        def outcomes_to_actions(x, y):
            return x, y

    player_1, player_2 = (
        params.player_positions[x],
        params.player_positions[y],
    )
    outcome_1, outcome_2 = player_1.play(player_2, noise=noise)
    actions = outcomes_to_actions(outcome_1, outcome_2)
    score_1, score_2 = scorer.score(actions)
    scores = {x: score_1, y: score_2}
    return Outcome(actions={x: actions[0], y: actions[1]}, scores=scores)


def symm2p_play_round(
    params: PlayParams, scorer: BaseScorer, noise: Optional[float] = None
) -> Outcome:
    # Either order is fine for a symmetric player
    return x_plays_y_round(
        Symm2pPosition.POS_1, Symm2pPosition.POS_2, params, scorer, noise=noise
    )
