from axelrod import Player

class Appeaser(Player):
    """
    A player who tries to guess what the opponent wants, switching his 
    behaviour every time the opponent plays 'D'.
    """
    def strategy(self, opponent):
        """
        Start with 'C', switch between 'C' and 'D' when opponent plays 'D'.
        """
        if len(self.history) == 0:
	    self.str = 'C'
        if opponent.history[-1] == 'D':
	    if self.str == 'C':
		self.str = 'D'
 	    else:
		self.str = 'C'
        return self.str

    def __repr__(self):
        """
        The string method for the strategy:
        """
        return 'Appeaser'
