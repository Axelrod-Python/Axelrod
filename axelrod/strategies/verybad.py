from axelrod.actions import Actions, Action
from axelrod.player import Player

C, D = Actions.C, Actions.D

class VeryBad(Player):
    """
    It cooperates in the first three rounds, and uses probability
    (it implements a memory, which stores the opponent’s moves) to decide for
    cooperating or defecting.
        
    Names:
    
    - VeryBad: [Andre2013]_
    """

    name = 'VeryBad'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        
        if len(opponent.history) < 4:
            return C
        
        total_moves = len(opponent.history)
        cooperations = opponent.cooperations
        
        cooperation_probability = cooperations / (total_moves * 1.0)
        
        if cooperation_probability > 0.5:
            return C
            
        elif cooperation_probability < 0.5:
            return D
            
        else:
            return opponent.history[-1]
