from axelrod import Actions, Player
from axelrod.actions import Action

C, D = Actions.C, Actions.D

class ShortMem(Player):
    """
    A player starts by always cooperating for the first 10 moves.
    
    The opponent answers are stored in the memory, whose maximum size is 10 results. From the tenth round on, the program analyzes the memory, and compare the number of defects and cooperates of the opponent, based in percentage. If cooperation occurs 30% more than defection, it will cooperate.
    If defection occurs 30% more than cooperation, the program will defect. Otherwise, the program follows the TitForTat algorithm.
    
    Names:
    
    - ShortMem: [Andre:2013]_
    """

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

        if len(self.history) <= memoryDepth:
            return C
        
        array = self.history[:-11:-1]
        cooperateRatio = array.count('C')/memoryDepth
        defectRatio = array.count('D')/memoryDepth
            
        if cooperateRatio - defectRatio > 0.3:
            return C
        elif defectRatio - cooperateRatio > 0.3:
            return D
        else:
            return opponent.history[-1]
        
