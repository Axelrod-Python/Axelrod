import random
from axelrod import Player


class OnceBitten(Player):
    """
    Co-operates once when the opponent defects, but if they defect twice in a row defaults to forgetful grudger for 10 turns defecting
    """

    name = 'Once Bitten'
    classifier = {
        'memory_depth': 12,  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        """
        Initialised the player
        """
        super(OnceBitten, self).__init__()
        self.mem_length = 10
        self.grudged = False
        self.grudge_memory = 0
        self.stochastic = False

    def strategy(self, opponent):
        """
        Begins by playing C, then plays D for mem_length rounds if the opponent ever plays D twice in a row
        """
        if self.grudge_memory >= self.mem_length:
            self.grudge_memory = 0
            self.grudged = False

        if len(opponent.history) < 2:
            return 'C'

        if self.grudged:
            self.grudge_memory += 1
            return 'D'
        elif not ('C' in opponent.history[-2:]):
            self.grudged = True
            return 'D'
        return 'C'

    def reset(self):
        """
        Resets scores and history
        """
        Player.reset(self)
        self.grudged = False
        self.grudge_memory = 0


class FoolMeOnce(Player):
    """
    Forgives one D then retaliates forever on a second D.
    """

    name = 'Fool Me Once'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        Player.__init__(self)
        self.classifier['stochastic'] = False

    def strategy(self, opponent):
        if not opponent.history:
            return 'C'
        if opponent.defections > 1:
            return 'D'
        return 'C'


class ForgetfulFoolMeOnce(Player):
    """
    Forgives one D then retaliates forever on a second D. Sometimes randomly forgets the defection count, and so keeps a secondary count separate from the the
    standard count in Player.
    """

    name = 'Forgetful Fool Me Once'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, forget_probability = 0.05):
        Player.__init__(self)
        self.D_count = 0
        self._initial = 'C'
        self.forget_probability = forget_probability
        self.init_args = (forget_probability,)

    def strategy(self, opponent):
        r = random.random()
        if not opponent.history:
            return self._initial
        if opponent.history[-1] == 'D':
            self.D_count += 1
        if r < self.forget_probability:
            self.D_count = 0
        if self.D_count > 1:
            return 'D'
        return 'C'

    def reset(self):
        Player.reset(self)
        self.D_count = 0


class FoolMeForever(Player):
    """
    Fool me once, shame on me. Teach a man to fool me and I'll be fooled for
    the rest of my life.
    """

    name = 'Fool Me Forever'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        if opponent.defections > 0:
            return 'C'
        return 'D'
