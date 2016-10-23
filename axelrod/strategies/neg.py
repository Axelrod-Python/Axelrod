import random
from axelrod import Actions, Player, random_choice, flip_action, init_args
from axelrod.strategy_transformers import TrackHistoryTransformer

C, D = Actions.C, Actions.D

class Neg(Player):
    """
    A player starts by cooperating or defecting randomly if it's their first move,
     then simply doing the opposite of the opponents last move thereafter.

    Names:

    Neg - [No official reference found in docs, only found in 'Desired New Strategies' list: https://github.com/Axelrod-Python/Axelrod/issues/379]
    """

    name = "Neg"
    classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        # Random first move
        if(len(self.history) == 0):
            return random_choice();
        
        # Act opposite of opponent otherwise
        return flip_action(opponent.history[-1])
		