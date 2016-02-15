from axelrod import Actions, Player

class ThueMorse(Player):
    """A player who cooperates or defects according to the Thue-Morse sequence."""

    name = 'ThueMorse'
    classifier = {
        'memory_depth': float('Inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def thuemorse_sequence(self, x):
	    if x == 0:
	        return 0
	    if x%2==0:
	        return self.thuemorse_sequence(x/2)
	    if x%2==1:
	        f = x-1
	        return 1 - self.thuemorse_sequence(f/2)

    def strategy(self, opponent):
        n = len(self.history)
        if self.thuemorse_sequence(n) == 1:
            return Actions.C
        return Actions.D




class ThueMorseInverse(Player):
    """A player who defects or cooperates according to the Thue-Morse sequence (Inverse of ThueMorse)."""

    name = 'ThueMorseInverse'
    classifier = {
        'memory_depth': float('Inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def thuemorse_sequence(self, x):
	    if x == 0:
	        return 0
	    if x%2==0:
	        return self.thuemorse_sequence(x/2)
	    if x%2==1:
	        f = x-1
	        return 1 - self.thuemorse_sequence(f/2)

    def strategy(self, opponent):
        n = len(self.history)
        if self.thuemorse_sequence(n) == 1:
            return Actions.D
        return Actions.C
