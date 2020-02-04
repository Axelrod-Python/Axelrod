from axelrod.action import Action
from axelrod.player import Player
from axelrod.random_ import random_choice
from typing import Tuple
from typing import List

C, D = Action.C, Action.D

class AdaptiveZeroDet(Player):
	name = 'AdaptiveZeroDet'
	classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }
	def __init__(self, phi: float = 0.125, s: float = 0.5, l: float = 3, four_vector: Tuple[float, float, float, float] = None, initial: Action = C) -> None:
		# This Keeps track of the parameter values (phi,s,l) as well as the four vector which makes final decisions.
		self.scores = {C: 0, D: 0}
		self.phi = phi
		self.s = s
		self.l = l
		self._initial = initial
		super().__init__()

	def set_four_vector(self, four_vector: Tuple[float, float, float, float]):
		# This checks the four vector is usable and allows previous matches' output to be input for next four vector
		if not all(0 <= p <= 1 for p in four_vector):
			raise ValueError("An element in the probability vector, {}, is not between 0 and 1.".format(str(four_vector)))
		self._four_vector = dict(zip([(C, C), (C, D), (D, C), (D, D)], map(float, four_vector)))
		self.classifier['stochastic'] = any(0 < x < 1 for x in set(four_vector))

	def score_last_round(self, opponent: Player):
		# This gives the strategy the game attributes and allows the strategy to score itself properly
		game = self.match_attributes["game"]
		if len(self.history):
			last_round = (self.history[-1], opponent.history[-1])
			scores = game.score(last_round)
			self.scores[last_round[0]] += scores[0]

	def strategy(self, opponent: Player) -> Action:
		s = self.s
		phi = self.phi
		l = self.l
		d = randint(0, 9)/1000 # Selects random value to adjust s and l
		if self.scores[C] > self.scores[D] & len(self.history):
			# This checks scores to determine how to adjust s and l either up or down by d
			# This also checks if the length of the game is long enough to start adjusting
			self.l = l+d
			l = self.l
			# adjust l up
			self.s = s-d
			s = self.s
			# adjust s down
			R, P, S, T = self.match_attributes["game"].RPST()
			phi = self.phi
			s_min = - min((T - l) / (l - S), (l - S) / (T - l)) # Sets minimum for s
			if  (l > R) or (s < s_min):
				# This checks that neither s nor l is leaving its range
				if (l > R):
					l = l-d
					self.l = (l+R)/2
					l = self.l
					# If l would leave its range instead its distance from its max is halved
				if (s < s_min):
					s = s+d
					self.s = (s+s_min)/2
					s = self.s
					# If s would leave its range instead its distance from its min is halved
			p1 = 1 - phi * (1 - s) * (R - l)
			p2 = 1 - phi * (s * (l - S) + (T - l))
			p3 = phi * ((l - S) + s * (T - l))
			p4 = phi * (1 - s) * (l - P)
			four_vector = [p1, p2, p3, p4]
			# Four vector is calculated with new parameters
			self.set_four_vector(four_vector)
			if not hasattr(self, "_four_vector"):
				raise ValueError("_four_vector not yet set")
			if len(opponent.history) == 0:
				return self._initial
			p = self._four_vector[(self.history[-1], opponent.history[-1])]
			return random_choice(p)
		else:
			# This adjusts s and l in the opposite direction
			self.l = l-d
			l = self.l
			# adjust l down
			self.s = s+d
			s = self.s
			# adjust s up
			R, P, S, T = self.match_attributes["game"].RPST()
			phi = self.phi
			if (l < P) or (s > 1):
				# This checks that neither s nor l is leaving its range
				if (l < P):
					l = l+d
					self.l = (l+P)/2
					l = self.l
					# If l would leave its range instead its distance from its min is halved
				if (s > 1):
					s = s-d
					self.s = (s+1)/2
					s = self.s
					# If s would leave its range instead its distance from its max is halved
			p1 = 1 - phi * (1 - s) * (R - l)
			p2 = 1 - phi * (s * (l - S) + (T - l))
			p3 = phi * ((l - S) + s * (T - l))
			p4 = phi * (1 - s) * (l - P)
			four_vector = [p1, p2, p3, p4]
			# Four vector is calculated with new parameters
			self.set_four_vector(four_vector)
			if not hasattr(self, "_four_vector"):
				raise ValueError("_four_vector not yet set")
			if len(opponent.history) == 0:
				return self._initial
			p = self._four_vector[(self.history[-1], opponent.history[-1])]
			return random_choice(p)
