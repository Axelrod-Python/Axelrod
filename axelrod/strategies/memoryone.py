import random

from axelrod import Player, game_matrix
#from tournament import game_matrix

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
    
    def strategy(self, opponent):
        """Switches if it doesn't get the best payout, traditionally equivalent to a Memory one strategy of [1,0,0,1], but this implementation does not require random draws."""
        if not opponent.history:
            return self._initial
        last_round = (self.history[-1], opponent.history[-1])
        return self.response_dict[last_round]

class MemoryOnePlayer(Player):
    """Uses a four-vector for strategies based on the last round of play, (P(C|CC), P(C|CD), P(C|DC), P(C|DD)), defaults to Win-Stay Lose-Shift ."""

    name = 'Memory One Player'

    def __init__(self, four_vector=[1,0,0,1], initial='C'):
        Player.__init__(self)
        self._four_vector = dict( zip(  [ ('C','C'), ('C','D'), ('D','C'), ('D','D')], map(float, four_vector) ) )
        self._initial = initial

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

def zd_vector1(chi):
    return (1. - (2. * chi - 2.) / (4. * chi + 1.), 0.,
            (chi + 4.) / (4. * chi + 1.), 0.)


def zd_vector2(chi):
    return (1., (chi - 1.)/(3. * chi + 2.), 1., 2.*(chi - 1.)/(3. * chi + 2.))


#def press_dyson_determinant():
    #pass


#def exact_stationary(p,q):
    #"""Using the Press and Dyson Formula where p and q are the conditional probability vectors."""
    #s = []
    #c1 = [-1 + p[0]*q[0], p[1]*q[2], p[2]*q[1], p[3]*q[3]]
    #c2 = [-1 + p[0], -1 + p[1], p[2], p[3]]
    #c3 = [-1 + q[0], q[2], -1 + q[1], q[3]]
    
    #for i in range(4):
        #f = numpy.zeros(4)
        #f[i] = 1
        #m = numpy.matrix([c1,c2,c3,f])
        #d = linalg.det(m)
        #s.append(d)
    ## normalize
    #n = sum(s)
    #if n == 0.:
        #raise ValueError('exact_stationary() cannot handle zeros')
    #s = numpy.array(s) / n
    #return s


class ZDChi(MemoryOnePlayer):
    """An Extortionate Zero Determinant Strategy."""

    name = 'ZDChi'

    def __init__(self, chi=2):
        chi = float(chi)
        scores = game_matrix()
        R = scores[('C', 'C')][0]
        P = scores[('D', 'D')][0]
        T = scores[('C', 'D')][0]
        S = scores[('D', 'C')][0]
        
        phi_max = float(P-S) / ((P-S) + chi * (T-P))
        phi = phi_max / 2.

        p1 = 1. - phi*(chi - 1) * float(R-P) / (P-S)
        p2 = 1 - phi * (1 + chi * float(T-P) / (P-S))
        p3 = phi * (chi + float(T-P)/(P-S))
        p4 = 0

        four_vector = (p1, p2, p3, p4)
        super(self.__class__, self).__init__(four_vector)


class ZDGTFT2(MemoryOnePlayer):
    """A Generous Zero Determinant Strategy."""

    name = 'ZDGTFT2'

    def __init__(self):
        four_vector = zd_vector2(2.)
        super(self.__class__, self).__init__(four_vector)

class GTFT2(MemoryOnePlayer):
    """Generous Tit-For-Tat Strategy."""

    name = 'ZDGTFT2'

    def __init__(self, ep=0.02):
        four_vector = [1-ep, ep, 1-ep, ep]
        super(self.__class__, self).__init__(four_vector)

class StochasticCooperator(MemoryOnePlayer):
    """Stochastic Cooperator, http://www.nature.com/ncomms/2013/130801/ncomms3193/full/ncomms3193.html."""

    name = 'Stochastic Cooperator'

    def __init__(self):
        four_vector = (0.935, 0.229, 0.266, 0.42)
        super(self.__class__, self).__init__(four_vector)


class SuspiciousTFT(MemoryOnePlayer):
    """Suspicious Tit-For-Tat Strategy, initial move is D rather than C."""

    name = 'Suspicious TFT'

    def __init__(self):
        four_vector = (1.,0.,1.,0.)
        super(self.__class__, self).__init__(four_vector, initial='D')

# tft = (1.,0.,1.,0.)
# wsls = (1.,0.,0.,1.)
# alld = (0.,0.,0.,0.)
# allc = (1.,1.,1.,1.)

