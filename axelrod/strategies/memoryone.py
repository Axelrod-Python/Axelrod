import random

from axelrod import Player, Game

"""IPD Strategies: http://www.prisoners-dilemma.com/strategies.html"""


class WinStayLoseShift(Player):
    """Win-Stay Lose-Shift, also called Pavlov."""

    name = 'Win-Stay Lose-Shift'

    def __init__(self, initial='C'):
        Player.__init__(self)
        self.response_dict = {
            ('C','C'): 'C',
            ('C','D'): 'D',
            ('D','C'): 'D',
            ('D','D'): 'C',
        }
        self._initial = initial
        self.stochastic = False

    def strategy(self, opponent):
        """Switches if it doesn't get the best payout, traditionally equivalent to a Memory one strategy of [1,0,0,1], but this implementation does not require random draws."""
        if not opponent.history:
            return self._initial
        last_round = (self.history[-1], opponent.history[-1])
        return self.response_dict[last_round]

class MemoryOnePlayer(Player):
    """Uses a four-vector for strategies based on the last round of play, (P(C|CC), P(C|CD), P(C|DC), P(C|DD)), defaults to Win-Stay Lose-Shift. Intended to be used as an abstract base class or to at least be supplied with a initializing four_vector."""

    name = 'Generic Memory One Player'

    def __init__(self, four_vector=[1,0,0,1], initial='C'):
        Player.__init__(self)
        self._four_vector = dict( zip(  [ ('C','C'), ('C','D'), ('D','C'), ('D','D')], map(float, four_vector) ) )
        self._initial = initial
        self.stochastic = False
        for x in set(four_vector):
            if x != 0 and x!= 1:
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

## Examples of strategies as Memory-One
# tft = (1.,0.,1.,0.)
# gtft = (1.-ep,ep.,1.-ep,ep)
# wsls = (1.,0.,0.,1.)
# alld = (0.,0.,0.,0.)
# allc = (1.,1.,1.,1.)

class GTFT(MemoryOnePlayer):
    """Generous Tit-For-Tat Strategy."""

    name = 'Generous Tit-For-Tat'

    def __init__(self, ep=0.05):
        four_vector = [1-ep, ep, 1-ep, ep]
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
        four_vector = (1.-ep, ep, ep, 1.-ep)
        super(self.__class__, self).__init__(four_vector)

class ZDChi(MemoryOnePlayer):
    """An Extortionate Zero Determinant Strategy. See the Press and Dyson paper in PNAS for the original formula."""

    name = 'ZDChi'

    def __init__(self, chi=2):
        chi = float(chi)
        (R, P, T, S) = Game().RPTS()

        phi_max = float(P-S) / ((P-S) + chi * (T-P))
        phi = phi_max / 2.

        p1 = 1. - phi*(chi - 1) * float(R-P) / (P-S)
        p2 = 1 - phi * (1 + chi * float(T-P) / (P-S))
        p3 = phi * (chi + float(T-P)/(P-S))
        p4 = 0

        four_vector = (p1, p2, p3, p4)
        super(self.__class__, self).__init__(four_vector)

class ZDChi(MemoryOnePlayer):
    """An Extortionate Zero Determinant Strategy enforcing the relationship 's_x - P = chi (s_y - P)'. See the Press and Dyson paper in PNAS for the original formula."""

    name = 'ZD Extort-2'

    def __init__(self, chi=2):
        chi = float(chi)
        (R, P, T, S) = Game().RPTS()

        phi_max = float(P-S) / ((P-S) + chi * (T-P))
        phi = phi_max / 2.

        p1 = 1. - phi*(chi - 1) * float(R-P) / (P-S)
        p2 = 1 - phi * (1 + chi * float(T-P) / (P-S))
        p3 = phi * (chi + float(T-P)/(P-S))
        p4 = 0

        four_vector = (p1, p2, p3, p4)
        super(self.__class__, self).__init__(four_vector)

class ZDGTFT2(MemoryOnePlayer):
    """A Generous Zero Determinant Strategy enforcing the relationship 's_x - R = 2 (s_y - R)'. There are infinitely many such strategies depending on the choice of parameters. See the paper "From extortion to generosity, evolution in the Iterated Prisoner's Dilemma" PNAS 2013 for more details."""

    name = 'ZD GTFT2'

    def __init__(self, phi=1., chi=0.5):
        chi = float(chi)
        (R, P, T, S) = Game().RPTS()
        kappa = R
        B = T
        C = T-R 
        ## Compute minimum allowed chi (max allowed is 1)
        #min_chi = max([(kappa - B) / (kappa + C), (kappa + C) / (kappa - B)])
        #if min_chi < 0:
            #min_chi = 0
        #chi = min_chi
        p1 = 1. - phi*(1-chi) * (R-kappa)
        p2 = 1. - phi * (chi *C + B - (1 - chi)*kappa)
        p3 = phi * (chi*B + C + (1- chi)*kappa)
        p4 = phi*(1-chi)*kappa

        four_vector = (p1, p2, p3, p4)
        super(self.__class__, self).__init__(four_vector)

