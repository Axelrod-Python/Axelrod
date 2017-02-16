from axelrod.actions import Actions
from axelrod.player import Player
from axelrod.strategy_transformers import TrackHistoryTransformer

C, D = Actions.C, Actions.D


class Resurrection(Player):
    """
    A player starts by cooperating and then defects if there are five
    consecutive defects by the player.
    
    Names:
    - Resurrection: Name from CoopSim https://github.com/jecki/CoopSim     
    """

    # These are various properties for the strategy
    name = 'Resurrection'
    classifier = {
        'memory_depth': 1,  
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        if self.history:
            return C
        if len(self.history) >= 5 and self.history[-5:] == [D,D,D,D,D]:
            return D
        else:
            return opponent.history[-1]

