from axelrod.actions import Actions, Action
from axelrod.player import Player
from axelrod.random_ import random_choice

from typing import List, Tuple, Union

type_four_vector = Union[List[float], Tuple[float, float, float, float]]


C, D = Actions.C, Actions.D


class MemoryOnePlayer(Player):
    """
    Uses a four-vector for strategies based on the last round of play,
    (P(C|CC), P(C|CD), P(C|DC), P(C|DD)), defaults to Win-Stay Lose-Shift.
    Intended to be used as an abstract base class or to at least be supplied
    with a initializing four_vector.

    Names

    - Memory One: [Nowak1990]_
    """

    name = 'Generic Memory One Player'
    classifier = {
        'memory_depth': 1,  # Memory-one Four-Vector
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, four_vector: type_four_vector = None, initial: Action = C) -> None:
        """
        Parameters

        fourvector, list or tuple of floats of length 4
            The response probabilities to the preceeding round of play
            ( P(C|CC), P(C|CD), P(C|DC), P(C|DD) )
        initial, C or D
            The initial move

        Special Cases

        Alternator is equivalent to MemoryOnePlayer((0, 0, 1, 1), C)
        Cooperator is equivalent to MemoryOnePlayer((1, 1, 1, 1), C)
        Defector   is equivalent to MemoryOnePlayer((0, 0, 0, 0), C)
        Random     is equivalent to MemoryOnePlayer((0.5, 0.5, 0.5, 0.5))
           (with a random choice for the initial state)
        TitForTat  is equivalent to MemoryOnePlayer((1, 0, 1, 0), C)
        WinStayLoseShift is equivalent to MemoryOnePlayer((1, 0, 0, 1), C)
        See also: The remaining strategies in this file
                  Multiple strategies in titfortat.py
                  Grofman, Joss in axelrod_tournaments.py
        """
        super().__init__()
        self._initial = initial
        if four_vector is not None:
            self.set_four_vector(four_vector)
            if self.name == 'Generic Memory One Player':
                self.name = "%s: %s" % (self.name, four_vector)

    def set_four_vector(self, four_vector: type_four_vector):
        if not all(0 <= p <= 1 for p in four_vector):
            raise ValueError("An element in the probability vector, {}, is not "
                             "between 0 and 1.".format(str(four_vector)))

        self._four_vector = dict(zip([(C, C), (C, D), (D, C), (D, D)],
                                     map(float, four_vector)))
        self.classifier['stochastic'] = any(0 < x < 1 for x in set(four_vector))

    def strategy(self, opponent: Player) -> Action:
        if not hasattr(self, "_four_vector"):
            raise ValueError("_four_vector not yet set")
        if len(opponent.history) == 0:
            return self._initial
        # Determine which probability to use
        p = self._four_vector[(self.history[-1], opponent.history[-1])]
        # Draw a random number in [0, 1] to decide
        return random_choice(p)


class WinStayLoseShift(MemoryOnePlayer):
    """
    Win-Stay Lose-Shift, also called Pavlov.

    Names:

    - Win Stay Lose Shift: [Nowak1993]_
    - WSLS: [Stewart2012]_
    - Pavlov: [Kraines1989]_
    """

    name = 'Win-Stay Lose-Shift'
    classifier = {
        'memory_depth': 1,  # Memory-one Four-Vector
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, initial: Action = C) -> None:
        super().__init__()
        self.set_four_vector([1, 0, 0, 1])
        self._initial = initial


class WinShiftLoseStay(MemoryOnePlayer):
    """Win-Shift Lose-Stay, also called Reverse Pavlov.

    Names:

    - WSLS: [Li2011]_
    """

    name = 'Win-Shift Lose-Stay'
    classifier = {
        'memory_depth': 1,  # Memory-one Four-Vector
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, initial: Action = D) -> None:
        super().__init__()
        self.set_four_vector([0, 1, 1, 0])
        self._initial = initial


class GTFT(MemoryOnePlayer):
    """Generous Tit For Tat Strategy.

    Names:

    - Generous Tit For Tat: [Nowak1993]_
    - Naive peace maker: [Gaudesi2016]_
    - Soft Joss: [Gaudesi2016]_
    """

    name = 'GTFT'
    classifier = {
        'memory_depth': 1,  # Memory-one Four-Vector
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, p: float = None) -> None:
        """
        Parameters

        p, float
            A parameter used to compute the four-vector

        Special Cases

        TitForTat is equivalent to GTFT(0)
        """
        self.p = p
        super().__init__()

    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        if self.p is None:
            self.p = min(1 - (T - R) / (R - S), (R - P) / (T - P))
        four_vector = [1, self.p, 1, self.p]
        self.set_four_vector(four_vector)

    def __repr__(self) -> str:
        return "%s: %s" % (self.name, round(self.p, 2))


class FirmButFair(MemoryOnePlayer):
    """A strategy that cooperates on the first move, and cooperates except after
    receiving a sucker payoff.

    Names:

    - Firm But Fair: [Frean1994]_"""

    name = 'Firm But Fair'

    def __init__(self) -> None:
        four_vector = (1, 0, 1, 2/3)
        super().__init__(four_vector)
        self.set_four_vector(four_vector)


class StochasticCooperator(MemoryOnePlayer):
    """Stochastic Cooperator.

	Names:

	- Stochastic Cooperator: [Adami2013]_
	"""

    name = 'Stochastic Cooperator'

    def __init__(self) -> None:
        four_vector = (0.935, 0.229, 0.266, 0.42)
        super().__init__(four_vector)
        self.set_four_vector(four_vector)


class StochasticWSLS(MemoryOnePlayer):
    """
    Stochastic WSLS, similar to Generous TFT. Note that this is not the same as
    Stochastic WSLS described in [Amaral2016]_, that strategy is a modification
    of WSLS that learns from the performance of other strategies.

    Names:

    - Stochastic WSLS: Original name by Marc Harper
    """

    name = 'Stochastic WSLS'

    def __init__(self, ep: float = 0.05) -> None:
        """
        Parameters

        ep, float
            A parameter used to compute the four-vector -- the probability of
            cooperating when the previous round was CD or DC

        Special Cases

        WinStayLoseShift is equivalent to StochasticWSLS(0)
        """

        self.ep = ep
        four_vector = (1.-ep, ep, ep, 1.-ep)
        super().__init__(four_vector)
        self.set_four_vector(four_vector)


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

    name = 'LinearRelation'
    classifier = {
        'memory_depth': 1,  # Memory-one Four-Vector
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }


    def receive_match_attributes(self, phi: float = 0, s: float = None, l: float = None):
        """
        Parameters

        phi, s, l: floats
            Parameter used to compute the four-vector according to the
            parameterization of the strategies below.
        """

        (R, P, S, T) = self.match_attributes["game"].RPST()
        if s is None:
            s = 1
        if l is None:
            l = R

        # Check parameters
        s_min = - min((T-l) / (l-S), (l-S) / (T-l))
        if (l < P) or (l > R) or (s > 1) or (s < s_min):
            raise ValueError

        p1 = 1 - phi * (1 - s) * (R - l)
        p2 = 1 - phi * (s * (l - S) + (T - l))
        p3 = phi * ((l - S) + s * (T - l))
        p4 = phi * (1 - s) * (l - P)

        four_vector = [p1, p2, p3, p4]
        self.set_four_vector(four_vector)


class ZDExtort2(LRPlayer):
    """
    An Extortionate Zero Determinant Strategy with l=P.

    Names:

    - Extort-2: [Stewart2012]_
    """

    name = 'ZD-Extort-2'

    def __init__(self, phi: float = 1/9, s: float = 0.5) -> None:
        """
        Parameters

        phi, s: floats
            Parameters passed through to LRPlayer to determine
            the four vector.
        """
        self.phi = phi
        self.s = s
        super().__init__()

    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        self.l = P
        super().receive_match_attributes(
            self.phi, self.s, self.l)


class ZDExtort2v2(LRPlayer):
    """
    An Extortionate Zero Determinant Strategy with l=1.


    Names:

    - EXTORT2: [Kuhn2017]_
    """

    name = 'ZD-Extort-2 v2'

    def __init__(self, phi: float = 1/8, s: float = 0.5, l: float = 1) -> None:
        """
        Parameters

        phi, s: floats
            Parameters passed through to LRPlayer to determine
            the four vector.
        """
        self.phi = phi
        self.s = s
        self.l = l
        super().__init__()

    def receive_match_attributes(self):
        super().receive_match_attributes(
            self.phi, self.s, self.l)


class ZDExtort4(LRPlayer):
    """
    An Extortionate Zero Determinant Strategy with l=1, s=1/4. TFT is the
    other extreme (with l=3, s=1)


    Names:

    - Extort 4: Original name by Marc Harper
    """

    name = 'ZD-Extort-4'

    def __init__(self, phi: float = 4/17, s: float = 0.25, l: float = 1) -> None:
        """
        Parameters

        phi, s: floats
            Parameters passed through to LRPlayer to determine
            the four vector.
        """
        self.phi = phi
        self.s = s
        self.l = l
        super().__init__()

    def receive_match_attributes(self):
        super().receive_match_attributes(
            self.phi, self.s, self.l)


class ZDGen2(LRPlayer):
    """
    A Generous Zero Determinant Strategy with l=3.

    Names:

    - GEN2: [Kuhn2017]_
    """

    name = 'ZD-GEN-2'

    def __init__(self, phi: float = 1/8, s: float = 0.5, l: float = 3) -> None:
        """
        Parameters

        phi, s: floats
            Parameters passed through to LRPlayer to determine
            the four vector.
        """
        self.phi = phi
        self.s = s
        self.l = l
        super().__init__()

    def receive_match_attributes(self):
        super().receive_match_attributes(
            self.phi, self.s, self.l)


class ZDGTFT2(LRPlayer):
    """
    A Generous Zero Determinant Strategy with l=R.

    Names:

    - ZDGTFT-2: [Stewart2012]_
    """

    name = 'ZD-GTFT-2'

    def __init__(self, phi: float = 0.25, s: float = 0.5) -> None:
        """
        Parameters

        phi, s: floats
            Parameters passed through to LRPlayer to determine
            the four vector.
        """
        self.phi = phi
        self.s = s
        super().__init__()

    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        self.l = R
        super().receive_match_attributes(
            self.phi, self.s, self.l)


class ZDSet2(LRPlayer):
    """
    A Generous Zero Determinant Strategy with l=2.

    Names:

    - SET2: [Kuhn2017]_
    """

    name = 'ZD-SET-2'

    def __init__(self, phi: float = 1/4, s: float = 0., l: float = 2) -> None:
        """
        Parameters

        phi, s: floats
            Parameters passed through to LRPlayer to determine
            the four vector.
        """
        self.phi = phi
        self.s = s
        self.l = l
        super().__init__()

    def receive_match_attributes(self):
        super().receive_match_attributes(
            self.phi, self.s, self.l)


class SoftJoss(MemoryOnePlayer):
    """
    Defects with probability 0.9 when the opponent defects, otherwise
    emulates Tit-For-Tat.

    Names:

    - Soft Joss: [Prison1998]_
    """

    name = "Soft Joss"

    def __init__(self, q: float = 0.9) -> None:
        """
        Parameters

        q, float
            A parameter used to compute the four-vector

        Special Cases

        Cooperator is equivalent to SoftJoss(0)
        TitForTat  is equivalent to SoftJoss(1)
        """
        self.q = q
        four_vector = (1., 1 - q, 1, 1 - q)
        super().__init__(four_vector)

    def __repr__(self) -> str:
        return "%s: %s" % (self.name, round(self.q, 2))


class ALLCorALLD(Player):
    """This strategy is at the parameter extreme of the ZD strategies (phi = 0).
    It simply repeats its last move, and so mimics ALLC or ALLD after round one.
    If the tournament is noisy, there will be long runs of C and D.

    For now starting choice is random of 0.6, but that was an arbitrary choice
    at implementation time.

    Names:

    - ALLC or ALLD: Original name by Marc Harper
    """

    name = "ALLCorALLD"
    classifier = {
        'memory_depth': 1,  # Memory-one Four-Vector (1, 1, 0, 0)
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        if len(self.history) == 0:
            return random_choice(0.6)
        return self.history[-1]
