from axelrod.actions import Action, Actions
from axelrod.player import Player
from axelrod.random_ import random_choice
from axelrod.strategy_transformers import FinalTransformer

C, D = Actions.C, Actions.D


@FinalTransformer((D), name_prefix=None)  # End with defection
class Stalker(Player):
    """

    This is a strategy which is only influenced by the score.
    Its behavior is based on three values:
    the very_bad_score (all rounds in defection)
    very_good_score (all rounds in cooperation)
    wish_score (average between bad and very_good score)

    It starts with cooperation.

    - If current_average_score > very_good_score, it defects
    - If current_average_score lies in (wish_score, very_good_score) it
      cooperates
    - If current_average_score > 2, it cooperates
    - If current_average_score lies in (1, 2)
    - The remaining case, current_average_score < 1, it behaves randomly.
    - It defects in the last round

    Names:

    - Stalker: [Andre2013]_
    """

    name = 'Stalker'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(["game", "length"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        R, P, S, T  = self.match_attributes["game"].RPST()
        self.very_good_score = R
        self.very_bad_score = P
        self.wish_score = (R + P) / 2
        self.current_score = 0

    def score_last_round(self, opponent: Player):
        # Load the default game if not supplied by a tournament.
        game = self.match_attributes["game"]
        last_round = (self.history[-1], opponent.history[-1])
        scores = game.score(last_round)
        self.current_score += scores[0]

    def strategy(self, opponent: Player) -> Action:

        if len(self.history) == 0:
            return C

        self.score_last_round(opponent)

        current_average_score = self.current_score / len(self.history)

        if current_average_score > self.very_good_score:
            return D

        elif (current_average_score > self.wish_score) and (current_average_score < self.very_good_score):
            return C

        elif current_average_score > 2:
            return C

        elif (current_average_score < 2) and (current_average_score > 1):
            return D

        return random_choice()

    def reset(self):
        super().reset()
        self.current_score = 0
