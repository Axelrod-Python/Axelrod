"""This is an adapter for historical API on Player, Game, Match, and Tournament

For each of these classes, we keep a copy of the Ipd version of them as an
element, and translate the historical API to the current API on the Ipd version.
This keeps legacy code working as the internal API shifts to accommodate a more
general class of games.
"""

import copy
import inspect
from typing import Dict, List, Tuple, Union

import axelrod as axl

Score = Union[int, float]


class Player(axl.IpdPlayer):
    """Legacy players derive from this adapter."""

    def __new__(cls, *args, **kwargs):
        """Caches arguments for IpdPlayer cloning."""
        obj = super().__new__(cls)
        obj.init_kwargs = cls.init_params(*args, **kwargs)
        return obj

    @classmethod
    def init_params(cls, *args, **kwargs):
        """
        Return a dictionary containing the init parameters of a strategy
        (without 'self').
        Use *args and *kwargs as value if specified
        and complete the rest with the default values.
        """
        sig = inspect.signature(cls.__init__)
        # The 'self' parameter needs to be removed or the first *args will be
        # assigned to it
        self_param = sig.parameters.get("self")
        new_params = list(sig.parameters.values())
        new_params.remove(self_param)
        sig = sig.replace(parameters=new_params)
        boundargs = sig.bind_partial(*args, **kwargs)
        boundargs.apply_defaults()
        return boundargs.arguments

    def __init__(self):
        self._player = axl.IpdPlayer()

    def strategy(self, opponent: axl.IpdPlayer) -> axl.Action:
        """We expect the derived class to set this behavior."""
        raise NotImplementedError()

    def play(
        self, opponent: axl.IpdPlayer, noise: float = 0
    ) -> Tuple[axl.Action, axl.Action]:
        # We have to provide _player.play a copy of this strategy, which will
        # have an overwritten strategy, and possibly saved state and helper
        # methods.
        return self._player.play(opponent, noise, strategy_holder=self)

    def clone(self) -> 'Player':
        """Clones the player without history, reapplying configuration
        parameters as necessary."""

        # You may be tempted to re-implement using the `copy` module
        # Note that this would require a deepcopy in some cases and there may
        # be significant changes required throughout the library.
        # Consider overriding in special cases only if necessary
        cls = self.__class__
        new_player = cls(**self.init_kwargs)
        new_player._player.match_attributes = copy.copy(self.match_attributes)
        return new_player

    def reset(self):
        self._player.reset()

    def set_match_attributes(self, length: int = -1, game: 'Game' = None,
                             noise: float = 0) -> None:
        self._player.set_match_attributes(length, game, noise)

    def update_history(self, play: axl.Action, coplay: axl.Action) -> None:
        self._player.update_history(play, coplay)

    @property
    def history(self):
        return self._player.history

    @property
    def match_attributes(self):
        return self._player.match_attributes

    @match_attributes.setter
    def match_attributes(self, match_attributes):
        self._player.match_attributes = match_attributes

    @property
    def cooperations(self):
        return self._player.cooperations

    @property
    def defections(self):
        return self._player.defections

    @property
    def name(self):
        return self._player.name

    @name.setter
    def name(self, name):
        self._player.name = name

    @property
    def classifier(self):
        return self._player.classifier

    @classifier.setter
    def classifier(self, classifier):
        self._player.classifier = classifier

    @property
    def state_distribution(self):
        return self._player.state_distribution

    def __eq__(self, other: 'Player') -> bool:
        if not isinstance(other, Player):
            return False
        return self._player == other._player


class Game(object):
    def __init__(self, r: Score = 3, s: Score = 0, t: Score = 5, p: Score = 1):
        self._game = axl.IpdGame(r, s, t, p)

    def score(self, pair: Tuple[axl.Action, axl.Action]) -> Tuple[Score, Score]:
        return self._game.score(pair)

    def RPST(self) -> Tuple[Score, Score, Score, Score]:
        return self._game.RPST()

    @property
    def scores(self):
        return self._game.scores

    @scores.setter
    def scores(self, scores):
        self._game.scores = scores

    def __repr__(self) -> str:
        return repr(self._game)

    def __eq__(self, other: 'Game') -> bool:
        if not isinstance(other, Game):
            return False
        return self._game == other._game


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

    @property
    def result(self):
        return self._match.result

    @result.setter
    def result(self, result):
        self._match.result = result

    @property
    def noise(self):
        return self._match.noise

    @noise.setter
    def noise(self, noise):
        self._match.noise = noise

    @property
    def game(self):
        return self._match.game

    @game.setter
    def game(self, game):
        self._match.game = game

    @property
    def _cache(self):
        return self._match._cache

    @_cache.setter
    def _cache(self, _cache):
        self._match._cache = _cache

    @property
    def _cache_update_required(self):
        return self._match._cache_update_required

    @property
    def _stochastic(self):
        return self._match._stochastic

    @property
    def prob_end(self):
        return self._match.prob_end

    @prob_end.setter
    def prob_end(self, prob_end):
        self._match.prob_end = prob_end

    @property
    def turns(self):
        return self._match.turns

    @turns.setter
    def turns(self, turns):
        self._match.turns = turns

    @property
    def reset(self):
        return self._match.reset

    @reset.setter
    def reset(self, reset):
        self._match.reset = reset

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

    @property
    def players(self):
        return self._tournament.players

    @players.setter
    def players(self, players):
        self._tournament.players = players

    @property
    def game(self):
        return self._tournament.game

    @game.setter
    def game(self, game):
        self._tournament.game = game

    @property
    def turns(self):
        return self._tournament.turns

    @turns.setter
    def turns(self, turns):
        self._tournament.turns = turns

    @property
    def repetitions(self):
        return self._tournament.repetitions

    @repetitions.setter
    def repetitions(self, repetitions):
        self._tournament.repetitions = repetitions

    @property
    def name(self):
        return self._tournament.name

    @name.setter
    def name(self, name):
        self._tournament.name = name

    @property
    def _logger(self):
        return self._tournament._logger

    @property
    def noise(self):
        return self._tournament.noise

    @noise.setter
    def noise(self, noise):
        self._tournament.noise = noise

    @property
    def match_generator(self):
        return self._tournament.match_generator

    @match_generator.setter
    def match_generator(self, match_generator):
        self._tournament.match_generator = match_generator

    @property
    def _temp_file_descriptor(self):
        return self._tournament._temp_file_descriptor

    @property
    def num_interactions(self):
        return self._tournament.num_interactions

    @num_interactions.setter
    def num_interactions(self, num_interactions):
        self._tournament.num_interactions = num_interactions

    @property
    def use_progress_bar(self):
        return self._tournament.use_progress_bar

    @use_progress_bar.setter
    def use_progress_bar(self, use_progress_bar):
        self._tournament.use_progress_bar = use_progress_bar

    @property
    def filename(self):
        return self._tournament.filename

    @filename.setter
    def filename(self, filename):
        self._tournament.filename = filename

    @property
    def edges(self):
        return self._tournament.edges

    @edges.setter
    def edges(self, edges):
        self._tournament.edges = edges

    @property
    def prob_end(self):
        return self._tournament.prob_end

    @prob_end.setter
    def prob_end(self, prob_end):
        self._tournament.prob_end = prob_end
