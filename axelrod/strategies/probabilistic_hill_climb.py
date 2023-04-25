from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D

class ProbabilisticHillClimb(Player):
	"""
	Defects with probability of 50%.
	Every time the oppenent deffects, probability becomes '(100 + 1)/100', increasing by 1%.
	Every time the opponent confesses, probability becomes '(100 - 1)/100', decreasing by 1%.
	In case of error (conditions aren't triggered, repeat last move)

	This strategy is based on the following assumption: if the opponent is going to deffect,
	it is better to deffect. If the opponent is going to confess, it is better to confess. 
	Using a simple probabilistic approach, we can predict the opponents nexzt move and chose
	to confess/deffect accordingly.
	
	"""
	
	name = "Hill Climb"
	classifier = {
		"memory_depth": float("inf"),
		"stochastic": True,
		"long_run_time": False,
		"inpects_source": False,
		"manipulates_source": False,
		"manipulates_state": False,
	}
	
	def __init__(self) -> None:
		super().__init__()
		self.probability = 0.5
	
	def strategy(self, opponent: Player) -> Action:
		"""Actual strategy definition that determines player's action."""
		MAX = 100
		if not len(opponent.history): # if opponent has no previous moves, confess on first move
			return C
		
		else:
			if opponent.history[-1] == D:
				self.probability += 1/MAX
				if(self.probability >= 1):
					self.probability = 0.5 # to excape local maxima
				return self._random.random_choice(self.probability)
				
			if opponent.history[-1] == C:
				self.probability -= 1/MAX
				if(self.probability <= 0):
					self.probability = 0.1 # avoid crash
				return self._random.random_choice(self.probability)
			
			else:
				print("There has been an error")
				return self.history[-1]
