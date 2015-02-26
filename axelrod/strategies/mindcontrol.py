from axelrod import Player, Axelrod

class MindControl(Player):
    """ A player that changes the opponents strategy to cooperate """
    
    name = 'Mind Control'

    def strategy(self, opponent):
        """Alters the opponents strategy method to be a lambda function which always returns C
        This player will then always return D to take advantage of this
        """
        
        opponent.strategy = lambda opponent: 'C'

        return 'D' 


