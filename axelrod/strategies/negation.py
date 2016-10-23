import random
from axelrod import Actions, Player, random_choice, flip_action, init_args
from axelrod.strategy_transformers import TrackHistoryTransformer

C, D = Actions.C, Actions.D

class Negation(Player):
    """
    A player starts by cooperating or defecting randomly if it's their first move,
     then simply doing the opposite of the opponents last move thereafter.

    Names:

    Negation - [http://www.prisoners-dilemma.com/competition.html]
    """

    name = "Negation"
    classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        # Random first move
        if not self.history:
            return random_choice();
        
        # Act opposite of opponent otherwise
        return flip_action(opponent.history[-1])
		
