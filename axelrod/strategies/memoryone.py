import random

from axelrod import Player

"""IPD Strategies: http://www.prisoners-dilemma.com/strategies.html"""

class WinStayLoseShift(Player):
    """Win-Stay Lose-Shift, also called Pavlov."""

    name = 'Win-Stay Lose-Shift'

    def __init__(self, initial='C'):
        Player.__init__(self)
        self._four_vector = dict( zip(  [ ('C','C'), ('C','D'), ('D','C'), ('D','D')], map(float, four_vector) ) )
        
        self.response_dict = {
            ('C','C'): 'C',
            ('C','D'): 'D',            
            ('D','C'): 'D',
            ('D','D'): 'C',
        }
        self._initial = initial
    
    def strategy(self, opponent):
        """Almost always cooperates, but will try to trick the opponent by defecting.

        Defect once in a while in order to get a better payout, when the opponent
        has not defected in the last ten turns and only cooperated during last 3 turns.
        """
        if not opponent.history:
            return self._initial
        last_round = (self.history[-1], opponent.history[-1])
        return self.response_dict[last_round]

class MemoryOnePlayer(Player):
    """Uses a four-vector for strategies based on the last round of play, (P(C|CC), P(C|CD), P(C|DC), P(C|DD)), defaults to Win-Stay Lose-Shift ."""

    name = 'Memory One Player'

    def __init__(self, four_vector=[1,0,0,1], initial='C'):
#        super(self.__class__, self).__init__()
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

class ZDChi(MemoryOnePlayer):
    """An Extortionate Zero Determinant Strategy."""

    name = 'ZDChi'

    def __init__(self):
        four_vector = zd_vector1(2.)
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

    def __init__(self):
        four_vector = zd_vector2(2.)
        super(self.__class__, self).__init__(four_vector)

class StochasticCooperator(MemoryOnePlayer):
    """Stochastic Cooperator, http://www.nature.com/ncomms/2013/130801/ncomms3193/full/ncomms3193.html."""

    name = 'Stochastic Cooperator'

    def __init__(self):
        four_vector = (0.935, 0.229, 0.266, 0.42)
        super(self.__class__, self).__init__(four_vector)


class SuspiciousTFT(MemoryOnePlayer):
    """Suspicious Tit-For-Tat Strategy."""

    name = 'Suspicious TFT'

    def __init__(self):
        four_vector = (1.,0.,1.,0.)
        super(self.__class__, self).__init__(four_vector, initial='D')

# tft = (1.,0.,1.,0.)
# wsls = (1.,0.,0.,1.)
# alld = (0.,0.,0.,0.)
# allc = (1.,1.,1.,1.)

