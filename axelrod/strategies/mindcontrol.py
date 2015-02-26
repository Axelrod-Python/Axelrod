from axelrod import Player, Axelrod

class MindControl(Player):
    """ A player that changes the opponents strategy to cooperate """
    
    name = 'Mind Control'

    def strategy(self, opponent):
        """Alters the opponents strategy method """
        
        opponent.strategy = lambda opponent: 'C'

        return 'D' 


