from axelrod import Actions, Player, init_args

C, D = Actions.C, Actions.D

class Desperate(Player):
	"""A player only cooperates after mutual defection"""

    name = 'Desperate'
    classifier = {
        'memory_depth': 1,  
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        if not opponent.history:
            return D
        if self.history[-1] == D and opponent.history[-1] == D:
            return C
        return D

class Hopeless(Player): 
	"""A player only defects after mutual cooperation"""

    name = 'Hopeless'
    classifier = {
        'memory_depth': 1,  
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
		if not opponent.history:
            return C
        if self.history[-1] == C and opponent.history[-1] == C:
            return D
        return C

class Willing(Player):
	"""A player only defects after mutual defection"""

	name = 'Willing'
    classifier = {
        'memory_depth': 1,  
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

	def strategy(self, opponent):
		if not opponent.history:
            return C
        if self.history[-1] == D and opponent.history[-1] == D:
            return D
        return C

class Grim(Player):
	"""A player only cooperates after mutual cooperation"""

	name = 'Grim'
    classifier = {
        'memory_depth': 1,  
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
		if not opponent.history:
            return D
        if self.history[-1] == C and opponent.history[-1] == C:
            return C
        return D

