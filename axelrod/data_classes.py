from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple

import axelrod
from axelrod.action import Action


@dataclass
class PlayerConfig:
    name: str
    init_kwargs: dict = None

    def __call__(self):
        # Look up player by name
        player_class = getattr(axelrod, self.name)
        if self.init_kwargs:
            return player_class(**self.init_kwargs)
        return player_class()


@dataclass
class MatchParameters:
    turns: Optional[int] = None
    noise: Optional[float] = None
    prob_end: Optional[float] = None
    seed: Optional[int] = None
    game: Optional[axelrod.Game] = None


@dataclass
class ExpectedMatchOutcome:
    player_actions: Tuple[Action, ...]
    coplayer_actions: Tuple[Action, ...]
    player_attributes: Optional[dict] = None


@dataclass
class MatchConfig:
    player: PlayerConfig
    coplayer: PlayerConfig
    match_parameters: MatchParameters
    expected_outcome: Optional[ExpectedMatchOutcome] = None

    def __call__(self):
        """Generate the match."""
        player = self.player()
        coplayer = self.coplayer()
        noise = self.match_parameters.noise
        prob_end = self.match_parameters.prob_end
        turns = len(self.expected_outcome.player_actions)
        match = axelrod.Match(
            (player, coplayer),
            turns=turns,
            noise=noise,
            prob_end=prob_end
        )
        return match

    def test_match(self):
        pass
