from axelrod import Player, Axelrod

class MindControl(Player):
    """A player that changes the opponents strategy to cooperate."""
    
    name = 'Mind Control'

    def strategy(self, opponent):
        """Alters the opponents strategy method to be a lambda function which always returns C
        This player will then always return D to take advantage of this
        """
        
        opponent.strategy = lambda opponent: 'C'

        return 'D' 


class MindWarp(Player):
    """A player that changes the opponent's strategy but block changing it's own."""

    name = 'Mind Warp'

    def __setattr__(self, name, val):
        if name == 'strategy':
            pass
        else:
            self.__dict__[name] = val

    def strategy(self, opponent):
        opponent.strategy = lambda opponent: 'C'
        return 'D'

class MindBend(MindWarp):
    """A player that changes the opponent's strategy by modifying the internal dictionary."""

    name = 'Mind Bend'

    def strategy(self, opponent):
        opponent.__dict__['strategy'] = lambda opponent: 'C'
        return 'D'