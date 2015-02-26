from axelrod import Player, Axelrod

class MindControl(Player):
    """
    A player that changes the opponents strategy to cooperate
    """
    
    name = 'Mind Control'

    def strategy(self, opponent):
        """
        Simulates the next 50 rounds and decides whether to cooperate or defect
        """
        
        opponent.strategy = lambda opponent: 'C'

        return 'D' 


