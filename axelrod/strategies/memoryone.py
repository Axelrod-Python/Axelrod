from random import random

from axelrod import Player, Actions

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
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, four_vector=None, initial=C):
        """
        Parameters
        ----------
        fourvector, list or tuple of floats of length 4
            The response probabilities to the preceeding round of play
            ( P(C|CC), P(C|CD), P(C|DC), P(C|DD) )
        initial, C or D
            The initial move

        Special Cases
        -------------
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
        self.init_args = (four_vector, initial)

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
        # Draw a random number in [0,1] to decide
        return C if random() < p else D


class WinStayLoseShift(MemoryOnePlayer):
    """Win-Stay Lose-Shift, also called Pavlov."""

    name = 'Win-Stay Lose-Shift'

    def __init__(self, initial=C):
        Player.__init__(self)
        self.set_four_vector([1,0,0,1])
        self._initial = initial
        self.init_args = (initial,)


class GTFT(MemoryOnePlayer):
    """Generous Tit-For-Tat Strategy."""

    name = 'GTFT'

    def __init__(self, p=None):
        """
        Parameters
        ----------
        p, float
            A parameter used to compute the four-vector

        Special Cases
        -------------
        TitForTat is equivalent to GTFT(0)
        """
        self.p = p
        super(self.__class__, self).__init__()
        self.init_args = (p,)

    def receive_tournament_attributes(self):
        (R, P, S, T) = self.tournament_attributes["game"].RPST()
        if self.p is None:
            self.p = min(1 - float(T - R) / (R - S), float(R - P) / (T - P))
        four_vector = [1, self.p, 1, self.p]
        self.set_four_vector(four_vector)

    def __repr__(self):
        return "%s: %s" % (self.name, round(self.p, 2))


class StochasticCooperator(MemoryOnePlayer):
    """Stochastic Cooperator, http://www.nature.com/ncomms/2013/130801/ncomms3193/full/ncomms3193.html."""

    name = 'Stochastic Cooperator'

    def __init__(self):
        four_vector = (0.935, 0.229, 0.266, 0.42)
        super(self.__class__, self).__init__(four_vector)
        self.init_args = ()
        self.set_four_vector(four_vector)


class StochasticWSLS(MemoryOnePlayer):
    """Stochastic WSLS, similar to Generous TFT"""

    name = 'Stochastic WSLS'

    def __init__(self, ep=0.05):
        """
        Parameters
        ----------
        ep, float
            A parameter used to compute the four-vector -- the probability of
            cooperating when the previous round was CD or DC

        Special Cases
        -------------
        WinStayLoseShift is equivalent to StochasticWSLS(0)
        """

        self.ep = ep
        four_vector = (1.-ep, ep, ep, 1.-ep)
        super(self.__class__, self).__init__(four_vector)
        self.init_args = (ep,)
        self.set_four_vector(four_vector)


class ZeroDeterminantPlayer(MemoryOnePlayer):
    """Abstraction for ZD players. The correct formula is Equation 14 in
    http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0077886 .
    These players enforce a linear difference in stationary payoffs
    s * (S_xy - l) = S_yx - l, yielding extortionate strategies with l = P and
    generous strategies when l = R and s > 0"""

    name = 'ZD ABC'

    def receive_tournament_attributes(self, phi=0, s=None, l=None):
        """
        Parameters
        ----------
        phi, s, l: floats
            Parameter used to compute the four-vector according to the
            parameterization of Zero Determinant strategies below.
        """

        (R, P, S, T) = self.tournament_attributes["game"].RPST()
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


class ZDGTFT2(ZeroDeterminantPlayer):
    """A Generous Zero Determinant Strategy."""

    name = 'ZD-GTFT-2'

    def __init__(self, phi=0.25, s=0.5):
        """
        Parameters
        ----------
        phi, s: floats
            Parameters passed through to ZeroDeterminantPlayer to determine
            the four vector.
        """
        self.phi = phi
        self.s = s
        super(self.__class__, self).__init__()
        self.init_args = (phi, s)

    def receive_tournament_attributes(self):
        (R, P, S, T) = self.tournament_attributes["game"].RPST()
        self.l = R
        super(self.__class__, self).receive_tournament_attributes(self.phi,
                                                                  self.s,
                                                                  self.l)

class ZDExtort2(ZeroDeterminantPlayer):
    """An Extortionate Zero Determinant Strategy."""

    name = 'ZD-Extort-2'

    def __init__(self, phi=1./9, s=0.5):
        """
        Parameters
        ----------
        phi, s: floats
            Parameters passed through to ZeroDeterminantPlayer to determine
            the four vector.
        """
        self.phi = phi
        self.s = s
        super(self.__class__, self).__init__()
        self.init_args = (phi, s)

    def receive_tournament_attributes(self):
        (R, P, S, T) = self.tournament_attributes["game"].RPST()
        self.l = P
        super(self.__class__, self).receive_tournament_attributes(self.phi,
                                                                  self.s,
                                                                  self.l)


### Strategies for recreating tournaments
# See also Joss in axelrod_tournaments.py

class SoftJoss(MemoryOnePlayer):
    """
    Defects with probability 0.9 when the opponent defects, otherwise
    emulates Tit-For-Tat.
    """

    name = "Soft Joss"

    def __init__(self, q=0.9):
        """
        Parameters
        ----------
        q, float
            A parameter used to compute the four-vector

        Special Cases
        -------------
        Cooperator is equivalent to SoftJoss(0)
        TitForTat  is equivalent to SoftJoss(1)
        """
        self.q = q
        four_vector = (1., 1 - q, 1, 1 - q)
        super(self.__class__, self).__init__(four_vector)
        self.init_args = (q,)

    def __repr__(self):
        return "%s: %s" % (self.name, round(self.q, 2))
