from axelrod import Actions, Player
from axelrod.actions import Action

C, D = Actions.C, Actions.D

class ShortMem(Player):
    """A player who only ever defects."""

    name = 'ShortMem'
    classifier = {
        'memory_depth': 10,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        
        memoryDepth = self.classifier['memoryDepth']
        cooperateRatio = array.count('C')/memoryDepth
        defectRatio = array.count('D')/memoryDepth
        
        if len(self.history) <= memoryDepth:
            return C
            
        if cooperateRatio - defectRatio > 0.3:
            return C
        elif defectRatio - cooperateRatio > 0.3:
            return D
        else:
            return TitForTat().strategy(opponent)
        
