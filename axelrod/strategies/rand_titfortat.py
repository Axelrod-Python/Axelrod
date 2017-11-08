from axelrod.action import Action, actions_to_str
from axelrod.player import Player
from axelrod.random_ import random_choice
from axelrod.strategy_transformers import (
    TrackHistoryTransformer, FinalTransformer)

C, D = Action.C, Action.D


class RandomTitForTat(Player):
    """
    A player starts random, then copies its opponent, then switches
    between random and tit for tat every other iteration.

    Name:

    - Bipoler Random TitForTat: Original name by Zachary M. Taylor
    """

    # These are various properties for the strategy
    name = 'Random Tit for Tat'
    classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }


    def __init__(self, p: float=0.5) -> None:
        """
        Parameters
        ----------
        p, float
            The probability to cooperate

        Special Cases
        -------------
        Random(0) is equivalent to Defector
        Random(1) is equivalent to Cooperator
        """
        super().__init__()
        self.p = p
        if p in [0, 1]:
            self.classifier['stochastic'] = False


    def strategy(self, opponent: Player) -> Action:
        """This is the actual strategy"""
        # import pdb; pdb.set_trace()
        # First move
        if not self.history:
            return random_choice(self.p)
        # check if even number of moves
        if len(opponent.history) % 2 == 0:
            return random_choice(self.p)
        else:
            # React to the opponent's last move
            if opponent.history[-1] == D:
                return D
            return C
