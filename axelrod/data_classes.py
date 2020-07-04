from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple

import axelrod
from axelrod.action import Action


def verify_match_outcomes(match, expected_actions1, expected_actions2, attrs):
    """Tests that match produces the expected results."""
    match.play()
    player1, player2 = match.players
    for (play, expected_play) in zip(player1.history, expected_actions1):
        if play != expected_play:
            # print(play, expected_play)
            return False
    for (play, expected_play) in zip(player2.history, expected_actions2):
        # print(play, expected_play)
        if play != expected_play:
            return False
    # Test final player attributes are as expected
    if attrs:
        for attr, value in attrs.items():
            if getattr(player1, attr) != value:
                return False
    return True


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
    match_attributes: Optional[dict] = None


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

    def match(self, seed=None):
        """Generate the match."""
        player = self.player()
        coplayer = self.coplayer()
        noise = self.match_parameters.noise
        if not seed:
            seed = self.match_parameters.seed
        prob_end = self.match_parameters.prob_end
        match_attributes = self.match_parameters.match_attributes
        turns = len(self.expected_outcome.player_actions)
        match = axelrod.Match(
            (player, coplayer),
            turns=turns,
            noise=noise,
            prob_end=prob_end,
            seed=seed,
            match_attributes=match_attributes
        )
        return match

    def verify_match_outcomes(self, seed=None):
        match = self.match(seed=seed)
        verify_match_outcomes(match,
                              self.expected_outcome.player_actions,
                              self.expected_outcome.coplayer_actions,
                              self.expected_outcome.player_attributes)

    def search_seeds(self, lower=1, upper=100000):
        """Searches for a working seed."""
        for seed in range(lower, upper):
            match = self.match(seed=seed)
            if verify_match_outcomes(match,
                                     self.expected_outcome.player_actions,
                                     self.expected_outcome.coplayer_actions,
                                     self.expected_outcome.player_attributes):
                return seed
        return None


@dataclass
class TestMatchConfig:
    name: str
    description: Optional[str]
    match_config: MatchConfig


