from axelrod import Player

class Appeaser(Player):
    """A player who tries to guess what the opponent wants.
    
    Switch the behaviour every time the opponent plays 'D'.
    Start with 'C', switch between 'C' and 'D' when opponent plays 'D'.
    """

    name = 'Appeaser'

    def strategy(self, opponent):
        if len(self.history) == 0:
            self.str = 'C'
        else:
            if opponent.history[-1] == 'D':
                if self.str == 'C':
                    self.str = 'D'
                else:
                    self.str = 'C'
        return self.str
