from axelrod import Actions, Player, init_args, random_choice

"""IPD Strategies: http://www.prisoners-dilemma.com/strategies.html"""

C, D = Actions.C, Actions.D

class MemoryOnePlayer(Player):
    """Uses a four-vector for strategies based on the last round of play,
    (P(C|CC), P(C|CD), P(C|DC), P(C|DD)), defaults to Win-Stay Lose-Shift.
    Intended to be used as an abstract base class or to at least be supplied
    with a initializing four_vector."""

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

    @init_args
    def __init__(self, four_vector=None, initial=C):
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
        Player.__init__(self)
        self._initial = initial
        if four_vector:
            self.set_four_vector(four_vector)

    def set_four_vector(self, four_vector):
        if not all(0 <= p <= 1 for p in four_vector):
            raise ValueError('An element in the probability vector, %s, is not between 0 and 1.' % str(four_vector))

        self._four_vector = dict(zip([(C, C), (C, D), (D, C), (D, D)], map(float, four_vector)))
        self.classifier['stochastic'] = any(0 < x < 1 for x in set(four_vector))

    def strategy(self, opponent):
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

    - WSLS: [Stewart2012]_
    - Win Stay Lose Shift: [Nowak1993]_
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

    @init_args
    def __init__(self, initial=C):
        Player.__init__(self)
        self.set_four_vector([1, 0, 0, 1])
        self._initial = initial


class WinShiftLoseStay(MemoryOnePlayer):
    """Win-Shift Lose-Stay, also called Reverse Pavlov.

    For reference see: "Engineering Design of Strategies for Winning
    Iterated Prisoner's Dilemma Competitions" by Jiawei Li, Philip Hingston,
    and Graham Kendall.  IEEE TRANSACTIONS ON COMPUTATIONAL INTELLIGENCE AND AI
    IN GAMES, VOL. 3, NO. 4, DECEMBER 2011
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

    @init_args
    def __init__(self, initial=D):
        Player.__init__(self)
        self.set_four_vector([0, 1, 1, 0])
        self._initial = initial


class GTFT(MemoryOnePlayer):
    """Generous Tit-For-Tat Strategy."""

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

    def __init__(self, p=None):
        """
        Parameters

        p, float
            A parameter used to compute the four-vector

        Special Cases

        TitForTat is equivalent to GTFT(0)
        """
        self.p = p
        super(GTFT, self).__init__()
        self.init_args = (p,)

    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        if self.p is None:
            self.p = min(1 - float(T - R) / (R - S), float(R - P) / (T - P))
        four_vector = [1, self.p, 1, self.p]
        self.set_four_vector(four_vector)

    def __repr__(self):
        return "%s: %s" % (self.name, round(self.p, 2))


class FirmButFair(MemoryOnePlayer):
    """A Classical Strategy described in this paper (and earlier):
    http://www.math.ubc.ca/~hauert/publications/reprints/hauert_jtb02b.pdf"""

    name = 'Firm But Fair'

    @init_args
    def __init__(self):
        four_vector = (1, 0, 1, 2./3)
        super(FirmButFair, self).__init__(four_vector)
        self.set_four_vector(four_vector)


class StochasticCooperator(MemoryOnePlayer):
    """Stochastic Cooperator, http://www.nature.com/ncomms/2013/130801/ncomms3193/full/ncomms3193.html."""

    name = 'Stochastic Cooperator'

    @init_args
    def __init__(self):
        four_vector = (0.935, 0.229, 0.266, 0.42)
        super(StochasticCooperator, self).__init__(four_vector)
        self.set_four_vector(four_vector)


class StochasticWSLS(MemoryOnePlayer):
    """Stochastic WSLS, similar to Generous TFT"""

    name = 'Stochastic WSLS'

    @init_args
    def __init__(self, ep=0.05):
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
        super(StochasticWSLS, self).__init__(four_vector)
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


    def receive_match_attributes(self, phi=0, s=None, l=None):
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
    """An Extortionate Zero Determinant Strategy with l=P."""

    name = 'ZD-Extort-2'

    @init_args
    def __init__(self, phi=1./9, s=0.5):
        """
        Parameters

        phi, s: floats
            Parameters passed through to LRPlayer to determine
            the four vector.
        """
        self.phi = phi
        self.s = s
        super(ZDExtort2, self).__init__()

    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        self.l = P
        super(ZDExtort2, self).receive_match_attributes(
            self.phi, self.s, self.l)


class ZDExtort2v2(LRPlayer):
    """An Extortionate Zero Determinant Strategy with l=1."""

    name = 'ZD-Extort-2 v2'

    @init_args
    def __init__(self, phi=1./8, s=0.5, l=1):
        """
        Parameters

        phi, s: floats
            Parameters passed through to LRPlayer to determine
            the four vector.
        """
        self.phi = phi
        self.s = s
        self.l = l
        super(ZDExtort2v2, self).__init__()

    def receive_match_attributes(self):
        super(ZDExtort2v2, self).receive_match_attributes(
            self.phi, self.s, self.l)


class ZDExtort4(LRPlayer):
    """An Extortionate Zero Determinant Strategy with l=1, s=1/4. TFT is the
    other extreme (with l=3, s=1)"""

    name = 'ZD-Extort-4'

    @init_args
    def __init__(self, phi=4./17, s=0.25, l=1):
        """
        Parameters

        phi, s: floats
            Parameters passed through to LRPlayer to determine
            the four vector.
        """
        self.phi = phi
        self.s = s
        self.l = l
        super(ZDExtort4, self).__init__()

    def receive_match_attributes(self):
        super(ZDExtort4, self).receive_match_attributes(
            self.phi, self.s, self.l)


class ZDGen2(LRPlayer):
    """A Generous Zero Determinant Strategy with l=3."""

    name = 'ZD-GEN-2'

    @init_args
    def __init__(self, phi=1./8, s=0.5, l=3):
        """
        Parameters

        phi, s: floats
            Parameters passed through to LRPlayer to determine
            the four vector.
        """
        self.phi = phi
        self.s = s
        self.l = l
        super(ZDGen2, self).__init__()

    def receive_match_attributes(self):
        super(ZDGen2, self).receive_match_attributes(
            self.phi, self.s, self.l)


class ZDGTFT2(LRPlayer):
    """A Generous Zero Determinant Strategy with l=R."""

    name = 'ZD-GTFT-2'

    def __init__(self, phi=0.25, s=0.5):
        """
        Parameters

        phi, s: floats
            Parameters passed through to LRPlayer to determine
            the four vector.
        """
        self.phi = phi
        self.s = s
        super(ZDGTFT2, self).__init__()
        self.init_args = (phi, s)

    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        self.l = R
        super(ZDGTFT2, self).receive_match_attributes(
            self.phi, self.s, self.l)


class ZDSet2(LRPlayer):
    """A Generous Zero Determinant Strategy with l=2."""

    name = 'ZD-SET-2'

    @init_args
    def __init__(self, phi=1./4, s=0., l=2):
        """
        Parameters

        phi, s: floats
            Parameters passed through to LRPlayer to determine
            the four vector.
        """
        self.phi = phi
        self.s = s
        self.l = l
        super(ZDSet2, self).__init__()

    def receive_match_attributes(self):
        super(ZDSet2, self).receive_match_attributes(
            self.phi, self.s, self.l)


### Strategies for recreating tournaments
# See also Joss in axelrod_tournaments.py

class SoftJoss(MemoryOnePlayer):
    """
    Defects with probability 0.9 when the opponent defects, otherwise
    emulates Tit-For-Tat.
    """

    name = "Soft Joss"

    @init_args
    def __init__(self, q=0.9):
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
        super(SoftJoss, self).__init__(four_vector)

    def __repr__(self):
        return "%s: %s" % (self.name, round(self.q, 2))


class ALLCorALLD(Player):
    """This strategy is at the parameter extreme of the ZD strategies (phi = 0).
    It simply repeats its last move, and so mimics ALLC or ALLD after round one.
    If the tournament is noisy, there will be long runs of C and D.

    For now starting choice is random of 0.6, but that was an arbitrary choice
    at implementation time.
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

    def strategy(self, opponent):
        if len(self.history) == 0:
            return random_choice(0.6)
        return self.history[-1]
