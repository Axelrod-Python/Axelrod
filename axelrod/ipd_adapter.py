"""This is an adapter for historical API on Player, Game, Match, and Tournament

For each of these classes, we keep a copy of the Ipd version of them as an
element, and translate the historical API to the current API on the Ipd version.
This keeps legacy code working as the internal API shifts to accommodate a more
general class of games.
"""

from typing import Dict, List, Tuple, Union

import axelrod as axl

Score = Union[int, float]


class Player(object):
    """Legacy players derive from this adapter."""

    def __init__(self):
        """The derived class should call super().__init__().  At that point,
        name and clasifiers on the derived class will be set, so we copy that to
        player."""
        self._player = axl.IpdPlayer()
        if self.name:
            self._player.name = self.name
        if self.classifier:
            self._player.classifier = self.classifier

    def strategy(self, opponent: "BasePlayer") -> axl.Action:
        """We expect the derived class to set this behavior."""
        raise NotImplementedError()

    def play(
        self, opponent: "BasePlayer", noise: float = 0
    ) -> Tuple[axl.Action, axl.Action]:
        # We have to provide _player.play a copy of this strategy, which will
        # have an overwritten strategy, and possibly saved state and helper
        # methods.
        self._player.play(opponent, noise, strategy_holder=self)

    def clone(self) -> "Player":
        new_player = Player()
        new_player._player = self._player.clone()
        return new_player

    def reset(self):
        self._player.reset()


class Game(object):
    def __init__(self, r: Score = 3, s: Score = 0, t: Score = 5, p: Score = 1):
        self._game = axl.IpdGame(r, s, t, p)

    def score(self, pair: Tuple[axl.Action, axl.Action]) -> Tuple[Score, Score]:
        return self._game.score(pair)


class Match(object):
    def __init__(
        self,
        players: Tuple[axl.IpdPlayer],
        turns: int = None,
        prob_end: float = None,
        game: axl.IpdGame = None,
        deterministic_cache: axl.DeterministicCache = None,
        noise: float = 0,
        match_attributes: Dict = None,
        reset: bool = True,
    ):
        self._match = axl.IpdMatch(
            players,
            turns,
            prob_end,
            game,
            deterministic_cache,
            noise,
            match_attributes,
            reset,
        )

    @property
    def players(self) -> Tuple[axl.IpdPlayer]:
        return self._match.players

    @players.setter
    def players(self, players: Tuple[axl.IpdPlayer]):
        self._match.players = players

    def play(self) -> List[Tuple[axl.Action]]:
        return self._match.play()

    def scores(self) -> List[Score]:
        return self._match.scores()

    def final_score(self) -> Score:
        return self._match.final_score()

    def final_score_per_turn(self) -> Score:
        return self._match.final_score_per_turn()

    def winner(self) -> axl.IpdPlayer:
        return self._match.winner()

    def cooperation(self):
        return self._match.cooperation()

    def normalised_cooperation(self):
        return self._match.normalised_cooperation()

    def state_distribution(self):
        return self._match.state_distribution()

    def normalised_state_distribution(self):
        return self._match.normalised_state_distribution()

    def sparklines(self, c_symbol="█", d_symbol=" "):
        return self._match.sparklines(c_symbol=c_symbol, d_symbol=d_symbol)

    def __len__(self):
        return len(self._match)


class Tournament(object):
    def __init__(
        self,
        players: List[axl.IpdPlayer],
        name: str = "axelrod",
        game: axl.IpdGame = None,
        turns: int = None,
        prob_end: float = None,
        repetitions: int = 10,
        noise: float = 0,
        edges: List[Tuple] = None,
        match_attributes: dict = None,
    ) -> None:
        self._tournament = axl.IpdTournament(
            players,
            name,
            game,
            turns,
            prob_end,
            repetitions,
            noise,
            edges,
            match_attributes,
        )

    def setup_output(self, filename=None) -> None:
        self._tournament.setup_output(filename)

    def play(
        self,
        build_results: bool = True,
        filename: str = None,
        processes: int = None,
        progress_bar: bool = True,
    ) -> axl.ResultSet:
        return self._tournament.play(
            build_results, filename, processes, progress_bar
        )
