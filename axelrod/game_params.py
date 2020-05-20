"""Implements GameParams and other classes.

The GameParams class defines all everything a program should need to understand
a game (e.g. IPD or ultimatum).
"""

from enum import Enum
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union

import attr

from axelrod.action import Action
from axelrod.game import Game
from axelrod.player import Player, PlayerName

Position = Enum
Score = Union[float, int]


@attr.s
class PlayParams(object):
    """Parameters controlling a single round of play.

    Attributes
    ----------
    player_positions : Dict[Position, Player]
        Specifies the player that's going to play each of the positions.
    """
    player_positions: Dict[Position, Player] = attr.ib()


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
    generate_play_params : Callable[
        [List[Player], int], Generator[PlayParams, None, None]
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
    generate_play_params: Callable[
        [List[Player], int], Generator[PlayParams, None, None]
    ] = attr.ib()
    play_round: Callable[[PlayParams, Game], Outcome] = attr.ib()
    result: Callable[[Outcome], Any] = attr.ib(default=lambda x: x)


class Symm2pPosition(Position):
    """A position enum for symmetric 2-player games.

    "Symmetric" means that the positions are interchangeable.
    """
    POS_1 = 1
    POS_2 = 2


def symm2p_generate_play_params(
    players: List[Player], rounds: int
) -> Generator[PlayParams, None, None]:
    assert len(players) == 2
    player_positions = {
        Symm2pPosition.POS_1: players[0],
        Symm2pPosition.POS_2: players[1],
    }
    for _ in range(rounds):
        yield PlayParams(player_positions=player_positions)


def symm2p_play_round(
    params: PlayParams, game: Game, noise: Optional[float] = None
) -> Outcome:
    player_1, player_2 = (
        params.player_positions[Symm2pPosition.POS_1],
        params.player_positions[Symm2pPosition.POS_2],
    )
    action_1, action_2 = player_1.play(player_2, noise=noise)
    actions = {
        Symm2pPosition.POS_1: action_1,
        Symm2pPosition.POS_2: action_2,
    }
    score_1, score_2 = game.score((action_1, action_2))
    scores = {
        Symm2pPosition.POS_1: score_1,
        Symm2pPosition.POS_2: score_2,
    }
    return Outcome(actions=actions, scores=scores)


def ipd_result(outcome: Outcome) -> Tuple[Action, Action]:
    return (
        outcome.actions[Symm2pPosition.POS_1],
        outcome.actions[Symm2pPosition.POS_2],
    )


ipd_params = GameParams(
    generate_play_params=symm2p_generate_play_params,
    play_round=symm2p_play_round,
    result=ipd_result,
)
