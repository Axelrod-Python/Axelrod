from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D

class ProbabilisticHillClimb(Player):
	"""
	Defects with initial probability of 50%.
	Every time the oppenent deffects, probability becomes '(100 + 1)/100', increasing by 1%.
	Every time the opponent cooperates, probability becomes '(100 - 1)/100', decreasing by 1%.
	In case of error (conditions aren't triggered, repeat last move)

	This strategy is based on the following assumption: if the opponent is going to defect,
	it is better to defect. If the opponent is going to cooperate, it is better to cooperate. 
	Using a simple probabilistic approach, we can predict the opponents next move and chose
	to cooperate/defect accordingly.
	
    Hill climbing algorithms can be prone to being 'stuck' in local minima. To avoid this we 
    introduce some randomness, that is, if the probability of defection becomes equal to or 
    greater than 1 ( >= 100%), the probability of defection will be reset to 50% to avoid this. 
    For example: Think of this strategy playing against another strategy such as Tit-For-Tat. 
    If the probability of defection becomes too high, then (without adding radomness) both 
    ProbabilistciHillClimbing and Tit-For-Tat will infinitely defect, leading to a worse outcome.
	"""
	
	name = "Hill Climb"
	classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }
	
	def __init__(self) -> None:
		super().__init__()
		self.probability_of_defection = 0.5
	
	def strategy(self, opponent: Player) -> Action:
		"""Actual strategy definition that determines player's action."""
        
		if len(opponent.history) == 0:
			return C
		
		else:
			if opponent.history[-1] == D:
				self.probability_of_defection += 1 / 100
				if(self.probability_of_defection >= 1):
					self.probability_of_defection = 0.5
				return self._random.random_choice(self.probability_of_defection)
				
			if opponent.history[-1] == C:
				self.probability_of_defection -= 1 / 100
				if(self.probability_of_defection <= 0):
					self.probability_of_defection = 0.1 # avoid crash
				return self._random.random_choice(self.probability_of_defection)
			
		return self.history[-1]
