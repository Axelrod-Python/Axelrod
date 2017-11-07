from axelrod.action import Action, actions_to_str
from axelrod.player import Player
from axelrod.random_ import random_choice
from axelrod.strategy_transformers import (
    TrackHistoryTransformer, FinalTransformer)

C, D = Action.C, Action.D


class RandTitForTat(Player):
    """
    A player starts random, then copies its opponent, then switches
    between random and tit for tat every other iteration.

    Name:

    - Bipoler Random TitForTat: [Axelrod1980]_
    """

    # These are various properties for the strategy
    name = 'Bipoler Random Tit for Tat'
    classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        """This is the actual strategy"""
        # First move
        if not self.history:
            return random_choice(p: float=0.5)

        # check if even number of moves
        if len(opponent.history) % 2 == 0:
            # React to the opponent's last move
            if opponent.history[-1] == D:
                return D
            return C
        else:
            return random_choice(p: float=0.5)
