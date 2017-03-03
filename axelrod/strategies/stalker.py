from typing import List

from axelrod.actions import Action, Actions
from axelrod.player import Player
from axelrod.random_ import random_choice
from axelrod.strategy_transformers import FinalTransformer

C, D = Actions.C, Actions.D

@FinalTransformer((D), name_prefix=None)  # End with defection
class Stalker(Player):
    """
    A player starts by always cooperating for the first 10 moves.

    From the tenth round on, the player analyzes the last ten actions, and
    compare the number of defects and cooperates of the opponent, based in
    percentage. If cooperation occurs 30% more than defection, it will
    cooperate.
    If defection occurs 30% more than cooperation, the program will defect.
    Otherwise, the program follows the TitForTat algorithm.

    Names:

    - Stalker: [Andre2013]_
    """

    name = 'Stalker'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }
    def __init__(self, initial_plays: List[Action] =None) -> None:
        super().__init__()
        self.R, self.P, self.S, self.T  = self.match_attributes["game"].RPST()
        self.scores = []

    def score_last_round(self, opponent: Player):
        # Load the default game if not supplied by a tournament.
        game = self.match_attributes["game"]
        last_round = (self.history[-1], opponent.history[-1])
        scores = game.score(last_round)
        self.scores.append(scores[0])

    def strategy(self, opponent: Player) -> Action:

        if len(self.history) == 0:
            return C

        self.score_last_round(opponent)

        current_average_score = sum(self.scores) / len(self.scores)
        very_good_score = self.R
        very_bad_score = self.P
        wish_score = ( very_bad_score + very_good_score ) / 2

        if current_average_score > very_good_score:
            return D

        elif (current_average_score > wish_score) and (current_average_score < very_good_score):
            return C

        elif current_average_score > 2:
            return C

        elif (current_average_score < 2) and (current_average_score > 1):
            return D

        elif current_average_score < 1:
            return random_choice()
