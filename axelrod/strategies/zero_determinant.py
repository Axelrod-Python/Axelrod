from axelrod.action import Action
from .memoryone import MemoryOnePlayer

# from typing import List, Tuple, Union
# type_four_vector = Union[List[float], Tuple[float, float, float, float]]


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

    def receive_match_attributes(self, phi: float = 0, s: float = None,
                                 l: float = None):
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
