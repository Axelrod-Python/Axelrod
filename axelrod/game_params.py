"""Implements GameParams and other classes.

The GameParams class defines all everything a program should need to understand
how to play a game.  This class includes:

 -  game_type: A name specifying the game type (e.g. IPD or Ultimatum)
 -  generate_play_params: A function that takes a list of players and an integer
    representing the number of turns, yields PlayParams for rounds of play for
    as long as a match should last.
 -  play_round: A function that given a PlayParams and a Game object will play a
    single round of the game, and returns the Outcome object.
 -  result : A function that translates an Outcome object to a result that the
    match's play method returns.  By default, this is a pass-through.

GameParams gets passed into Match, Tournament, and Moran processes, so a
canonical instance of this class should get defined for each new game type.
However some game types may have more than one GameParams.  For example,
Ultimatum may generate rounds by keeping roles the same or by alternating roles;
so Ultimatum has two distinct GameParams.

Additionally includes some generic functionality for generate_play_params and
for play_round, that can be shared among any "symmetric" 2-player game.
("Symmetric" means that the roles are all the same, as with IPD.)
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

from .prototypes import BasePlayer, BaseScorer, Outcome, Position


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
    # TODO(5.0): This should be called generate_round, since the user won't know
    #  what PlayParams are.
    generate_play_params: Callable[
        [List[BasePlayer], int], Generator[PlayParams, None, None]
    ] = attr.ib()
    play_round: Callable[[PlayParams, BaseScorer], Outcome] = attr.ib()
    result: Callable[[Outcome], Any] = attr.ib(default=lambda x: x)


# TODO(5.0): Consider moving these Symm2p functions to a new file, and update
#  file-level docstrings.
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
