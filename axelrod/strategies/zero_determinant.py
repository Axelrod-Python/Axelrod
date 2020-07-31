from axelrod.action import Action

from .memoryone import MemoryOnePlayer

C, D = Action.C, Action.D


class LRPlayer(MemoryOnePlayer):
    """
    Abstraction for Linear Relation players. These players enforce a linear
    difference in stationary payoffs :math:`s (S_{xy} - l) = S_{yx} - l.`

    The parameter :math:`s` is called the slope and the parameter :math:`l` the
    baseline payoff. For extortionate strategies, the extortion factor
    :math:`\chi` is the inverse of the slope :math:`s`.

    For the standard prisoner's dilemma where :math:`T > R > P > S` and
    :math:`R > (T + S) / 2 > P`, a pair :math:`(l, s)` is enforceable iff

    .. math::
       :nowrap:

       \\begin{eqnarray}
       &P &<= l <= R \\\\
       &s_{min} &= -\min\\left( \\frac{T - l}{l - S}, \\frac{l - S}{T - l}\\right) <= s <= 1
       \\end{eqnarray}

    And also that there exists :math:`\\phi` such that

    .. math::
       :nowrap:

       \\begin{eqnarray}
          p_1 &= P(C|CC) &= 1 - \\phi (1 - s)(R - l) \\\\
          p_2 &= P(C|CD) &= 1 - \\phi (s(l - S) + (T - l)) \\\\
          p_3 &= P(C|DC) &= \\phi ((l - S) + s(T - l)) \\\\
          p_4 &= P(C|DD) &= \\phi (1 - s)(l - P)
       \\end{eqnarray}


    These conditions also force :math:`\\phi >= 0`. For a given pair :math:`(l, s)`
    there may be multiple such :math:`\\phi`.

    This parameterization is Equation 14 in [Hilbe2013]_.
    See Figure 2 of the article for a more in-depth explanation. Other game
    parameters can alter the relations and bounds above.

    Names:

    - Linear Relation player: [Hilbe2013]_
    """

    name = "LinearRelation"
    classifier = {
        "memory_depth": 1,  # Memory-one Four-Vector
        "stochastic": True,
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
