import random
from axelrod.action import Action
from axelrod.player import Player

from .memoryone import MemoryOnePlayer

C, D = Action.C, Action.D


class LRPlayer(MemoryOnePlayer):
    """Abstraction for Linear Relation players. These players enforce a linear
    difference in stationary payoffs s * (S_xy - l) = S_yx - l, with 0 <= l <= R.
    The parameter `s` is called the slope and the parameter `l` the
    baseline payoff. For extortionate strategies, the extortion factor is the
    inverse of the slope.

    This parameterization is Equation 14 in
    http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0077886.
    See Figure 2 of the article for a more in-depth explanation.

    Names:

    - Linear Relation player: [Hilbe2013]_
    """

    name = "LinearRelation"
    classifier = {
        "memory_depth": 1,  # Memory-one Four-Vector
        "stochastic": True,
        "makes_use_of": set(["game"]),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, phi: float = 0.2, s: float = 0.1, l: float = 1) -> None:
        """
        Parameters

        phi, s, l: floats
            Parameters determining the four_vector of the LR player.
        """
        self.phi = phi
        self.s = s
        self.l = l
        super().__init__()

    def set_initial_four_vector(self, four_vector):
        pass

    def receive_match_attributes(self):
        """
        Parameters

        phi, s, l: floats
            Parameter used to compute the four-vector according to the
            parameterization of the strategies below.
        """

        R, P, S, T = self.match_attributes["game"].RPST()
        l = self.l
        phi = self.phi
        s = self.s

        # Check parameters
        s_min = -min((T - l) / (l - S), (l - S) / (T - l))
        if (l < P) or (l > R) or (s > 1) or (s < s_min):
            raise ValueError

        p1 = 1 - phi * (1 - s) * (R - l)
        p2 = 1 - phi * (s * (l - S) + (T - l))
        p3 = phi * ((l - S) + s * (T - l))
        p4 = phi * (1 - s) * (l - P)

        four_vector = [p1, p2, p3, p4]
        self.set_four_vector(four_vector)


class ZDExtortion(LRPlayer):
    """
    An example ZD Extortion player.

    Names:

    - ZDExtortion: [Roemheld2013]_
    """

    name = "ZD-Extortion"

    def __init__(self, phi: float = 0.2, s: float = 0.1, l: float = 1) -> None:
        super().__init__(phi, s, l)


class ZDExtort2(LRPlayer):
    """
    An Extortionate Zero Determinant Strategy with l=P.

    Names:

    - Extort-2: [Stewart2012]_
    """

    name = "ZD-Extort-2"

    def __init__(self, phi: float = 1 / 9, s: float = 0.5) -> None:
        # l = P will be set by receive_match_attributes
        super().__init__(phi, s, None)

    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        self.l = P
        super().receive_match_attributes()


class ZDExtort2v2(LRPlayer):
    """
    An Extortionate Zero Determinant Strategy with l=1.


    Names:

    - EXTORT2: [Kuhn2017]_
    """

    name = "ZD-Extort-2 v2"

    def __init__(self, phi: float = 1 / 8, s: float = 0.5, l: float = 1) -> None:
        super().__init__(phi, s, l)


class ZDExtort3(LRPlayer):
    """
    An extortionate strategy from Press and Dyson's paper witn an extortion
    factor of 3.

    Names:

    - ZDExtort3: Original name by Marc Harper
    - Unnamed: [Press2012]_
    """

    name = "ZD-Extort3"

    def __init__(self, phi: float = 3 / 26, s: float = 1 / 3, l: float = 1) -> None:
        super().__init__(phi, s, l)


class ZDExtort4(LRPlayer):
    """
    An Extortionate Zero Determinant Strategy with l=1, s=1/4. TFT is the
    other extreme (with l=3, s=1)


    Names:

    - Extort 4: Original name by Marc Harper
    """

    name = "ZD-Extort-4"

    def __init__(self, phi: float = 4 / 17, s: float = 0.25, l: float = 1) -> None:
        super().__init__(phi, s, l)


class ZDGen2(LRPlayer):
    """
    A Generous Zero Determinant Strategy with l=3.

    Names:

    - GEN2: [Kuhn2017]_
    """

    name = "ZD-GEN-2"

    def __init__(self, phi: float = 1 / 8, s: float = 0.5, l: float = 3) -> None:
        super().__init__(phi, s, l)


class ZDGTFT2(LRPlayer):
    """
    A Generous Zero Determinant Strategy with l=R.

    Names:

    - ZDGTFT-2: [Stewart2012]_
    """

    name = "ZD-GTFT-2"

    def __init__(self, phi: float = 0.25, s: float = 0.5) -> None:
        # l = R will be set by receive_match_attributes
        super().__init__(phi, s, None)

    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        self.l = R
        super().receive_match_attributes()


class ZDMischief(LRPlayer):
    """
    An example ZD Mischief player.

    Names:

    - ZDMischief: [Roemheld2013]_
    """

    name = "ZD-Mischief"

    def __init__(self, phi: float = 0.1, s: float = 0.0, l: float = 1) -> None:
        super().__init__(phi, s, l)


class ZDSet2(LRPlayer):
    """
    A Generous Zero Determinant Strategy with l=2.

    Names:

    - SET2: [Kuhn2017]_
    """

    name = "ZD-SET-2"

    def __init__(self, phi: float = 1 / 4, s: float = 0.0, l: float = 2) -> None:
        super().__init__(phi, s, l)


class AdaptiveZeroDet(LRPlayer):
    """A Strategy that uses a zero determinant structure that updates
    its parameters after each round of play.

    Names:
    - AdaptiveZeroDet by Emmanuel Estrada and Dashiell Fryer
    """
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

    def __init__(self, phi: float = 0.125, s: float = 0.5, l: float = 3,
                 initial: Action = C) -> None:
        # This Keeps track of the parameter values (phi,s,l) as well as the
        # four vector which makes final decisions.
        super().__init__(phi=phi, s=s, l=l)
        self._scores = {C: 0, D: 0}
        self._initial = initial

    def score_last_round(self, opponent: Player):
        """This gives the strategy the game attributes and allows the strategy
         to score itself properly."""
        game = self.match_attributes["game"]
        if len(self.history):
            last_round = (self.history[-1], opponent.history[-1])
            scores = game.score(last_round)
            self._scores[last_round[0]] += scores[0]

    def _adjust_parameters(self):
        d = random.randint(0, 9) / 1000  # Selects random value to adjust s and l

        if self._scores[C] > self._scores[D]:
            # This checks scores to determine how to adjust s and l either
            # up or down by d
            self.l = self.l + d
            self.s = self.s - d
            R, P, S, T = self.match_attributes["game"].RPST()
            l = self.l
            s = self.s
            s_min = - min((T - l) / (l - S), (l - S) / (T - l))  # Sets minimum for s
            if (l > R) or (s < s_min):
                # This checks that neither s nor l is leaving its range
                # If l would leave its range instead its distance from its max is halved
                if l > R:
                    l = l - d
                    self.l = (l + R) / 2
                # If s would leave its range instead its distance from its min is halved
                if s < s_min:
                    s = s + d
                    self.s = (s + s_min) / 2
        else:
            # This adjusts s and l in the opposite direction
            self.l = self.l - d
            self.s = self.s + d
            R, P, S, T = self.match_attributes["game"].RPST()
            l = self.l
            s = self.s
            if (l < P) or (s > 1):
                # This checks that neither s nor l is leaving its range
                if l < P:
                    l = l + d
                    self.l = (l + P) / 2
                # If l would leave its range instead its distance from its min is halved
                if s > 1:
                    s = s - d
                    self.s = (s + 1) / 2
        # Update the four vector for the new l and s values
        self.receive_match_attributes()

    def strategy(self, opponent: Player) -> Action:
        if len(self.history) > 0:
            self.score_last_round(opponent)
            self._adjust_parameters()
        return super().strategy(opponent)
