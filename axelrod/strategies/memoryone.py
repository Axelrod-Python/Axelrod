import random

from axelrod import Player, Game

"""IPD Strategies: http://www.prisoners-dilemma.com/strategies.html"""


class WinStayLoseShift(Player):
    """Win-Stay Lose-Shift, also called Pavlov."""

    name = 'Win-Stay Lose-Shift'
    memory_depth = 1  # Four-Vector = (1,0,0,1)

    def __init__(self, initial='C'):
        Player.__init__(self)
        self.response_dict = {
            ('C', 'C'): 'C',
            ('C', 'D'): 'D',
            ('D', 'C'): 'D',
            ('D', 'D'): 'C',
        }
        self._initial = initial
        self.stochastic = False

    def strategy(self, opponent):
        """Switches if it doesn't get the best payout, traditionally equivalent
        to a Memory one strategy of [1,0,0,1], but this implementation does not
        require random draws."""
        if not opponent.history:
            return self._initial
        last_round = (self.history[-1], opponent.history[-1])
        return self.response_dict[last_round]


class MemoryOnePlayer(Player):
    """Uses a four-vector for strategies based on the last round of play,
    (P(C|CC), P(C|CD), P(C|DC), P(C|DD)), defaults to Win-Stay Lose-Shift.
    Intended to be used as an abstract base class or to at least be supplied
    with a initializing four_vector."""

    name = 'Generic Memory One Player'
    memory_depth = 1

    def __init__(self, four_vector, initial='C'):
        Player.__init__(self)
        self._four_vector = dict(zip([('C', 'C'), ('C', 'D'), ('D', 'C'), ('D', 'D')], map(float, four_vector)))
        self._initial = initial
        self.stochastic = False
        for x in set(four_vector):
            if x != 0 and x != 1:
                self.stochastic = True

    def strategy(self, opponent):
        if not len(opponent.history):
            return self._initial
        # Determine which probability to use
        p = self._four_vector[(self.history[-1], opponent.history[-1])]
        # Draw a random number in [0,1] to decide
        r = random.random()
        if r < p:
            return 'C'
        return 'D'


class GTFT(MemoryOnePlayer):
    """Generous Tit-For-Tat Strategy."""

    name = 'Generous Tit-For-Tat'

    def __init__(self, p=None):
        (R, P, S, T) = Game().RPST()
        if not p:
            p = min(1 - float(T - R) / (R - S), float(R - P) / (T - P))
        four_vector = [1, p, 1, p]
        super(self.__class__, self).__init__(four_vector)


class StochasticCooperator(MemoryOnePlayer):
    """Stochastic Cooperator, http://www.nature.com/ncomms/2013/130801/ncomms3193/full/ncomms3193.html."""

    name = 'Stochastic Cooperator'

    def __init__(self):
        four_vector = (0.935, 0.229, 0.266, 0.42)
        super(self.__class__, self).__init__(four_vector)


class StochasticWSLS(MemoryOnePlayer):
    """Stochastic WSLS, similar to Generous TFT"""

    name = 'Stochastic WSLS'

    def __init__(self, ep=0.05):
        self.ep = ep
        four_vector = (1.-ep, ep, ep, 1.-ep)
        super(self.__class__, self).__init__(four_vector)


class ZeroDeterminantPlayer(MemoryOnePlayer):
    """Abstraction for ZD players. The correct formula is Equation 14 in
    http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0077886 .
    These players enforce a linear difference in stationary payoffs
    s * (S_xy - l) = S_yx - l, yielding extortionate strategies with l = P and
    generous strategies when l = R and s > 0"""
    name = 'ZD ABC'

    def __init__(self, phi=0., s=None, l=None):
        (R, P, S, T) = Game().RPST()
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
        MemoryOnePlayer.__init__(self, four_vector)


class ZDGTFT2(ZeroDeterminantPlayer):
    """A Generous Zero Determinant Strategy."""

    name = 'ZD-GTFT-2'

    def __init__(self, phi=0., chi=2.):
        (R, P, S, T) = Game().RPST()
        ZeroDeterminantPlayer.__init__(self, phi=0.25, s=0.5, l=R)


class ZDExtort2(ZeroDeterminantPlayer):
    """An Extortionate Zero Determinant Strategy."""

    name = 'ZD-Extort-2'

    def __init__(self):
        (R, P, S, T) = Game().RPST()
        ZeroDeterminantPlayer.__init__(self, phi=1./9, s=0.5, l=P)


### Strategies for recreating Axelrod's tournament ###


class Grofman(MemoryOnePlayer):
    """
    Cooperates with probability 2/7.
    """

    name = "Grofman"

    def __init__(self):
        p = float(2) / 7
        four_vector = (p, p, p, p)
        super(self.__class__, self).__init__(four_vector)


class Joss(MemoryOnePlayer):
    """
    Cooperates with probability 0.9 when the opponent cooperates, otherwise 
    emulates Tit-For-Tat.
    """

    name = "Joss"

    def __init__(self, p=0.9):
        four_vector = (p, 0, p, 0)
        super(self.__class__, self).__init__(four_vector)


class SoftJoss(MemoryOnePlayer):
    """
    Defects with probability 0.9 when the opponent defects, otherwise 
    emulates Tit-For-Tat.
    """

    name = "Soft Joss"

    def __init__(self, q=0.9):
        four_vector = (1., 1 - q, 1, 1 - q)
        super(self.__class__, self).__init__(four_vector)
