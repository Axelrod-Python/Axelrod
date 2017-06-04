from axelrod.actions import Actions, Action
from axelrod.player import Player

from typing import List

C, D = Actions.C, Actions.D


class Adaptive(Player):
    """Start with a specific sequence of C and D, then play the strategy that
    has worked best, recalculated each turn.

    Names:

    - Adaptive: [Li2011]_

    """

    name = 'Adaptive'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, initial_plays: List[Action] = None) -> None:
        super().__init__()
        if not initial_plays:
            initial_plays = [C] * 6 + [D] * 5
        self.initial_plays = initial_plays
        self.scores = {C: 0, D: 0}

    def score_last_round(self, opponent: Player):
        # Load the default game if not supplied by a tournament.
        game = self.match_attributes["game"]
        if len(self.history):
            last_round = (self.history[-1], opponent.history[-1])
            scores = game.score(last_round)
            self.scores[last_round[0]] += scores[0]

    def strategy(self, opponent: Player)-> Action:
        # Update scores from the last play
        self.score_last_round(opponent)
        # Begin by playing the sequence C,C,C,C,C,C,D,D,D,D,D
        index = len(self.history)
        if index < len(self.initial_plays):
            return self.initial_plays[index]
        # Play the strategy with the highest average score so far
        if self.scores[C] > self.scores[D]:
            return C
        return D

    def reset(self):
        super().reset()
        self.scores = {C: 0, D: 0}
