import inspect
import random
import copy

C, D = 'C', 'D'
flip_dict = {C: D, D: C}


# Strategy classifiers

def is_basic(s):
    """
    Defines criteria for a strategy to be considered 'basic'
    """
    stochastic = s.classifier['stochastic']
    depth = s.classifier['memory_depth']
    inspects_source = s.classifier['inspects_source']
    manipulates_source = s.classifier['manipulates_source']
    manipulates_state = s.classifier['manipulates_state']
    return (not stochastic) and (not inspects_source) and (not manipulates_source) and (not manipulates_state) and (depth in (0, 1))

def is_cheater(s):
    """
    A function to check if a strategy cheats.
    """
    classifier = s.classifier
    return classifier['inspects_source'] or\
           classifier['manipulates_source'] or\
           classifier['manipulates_state']


def update_histories(player1, player2, move1, move2):
    """Updates histories and cooperation / defections counts following play."""
    # Update histories
    player1.history.append(move1)
    player2.history.append(move2)
    # Update player counts of cooperation and defection
    if move1 == C:
        player1.cooperations += 1
    elif move1 == D:
        player1.defections += 1
    if move2 == C:
        player2.cooperations += 1
    elif move2 == D:
        player2.defections += 1


class Player(object):
    """A class for a player in the tournament.

    This is an abstract base class, not intended to be used directly.
    """

    name = "Player"
    classifier = {}
    default_classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),
        'inspects_source': None,
        'manipulates_source': None,
        'manipulates_state': None
    }

    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        self.history = []
        self.classifier = copy.copy(self.classifier)
        if self.name == "Player":
            self.classifier['stochastic'] = False
        for dimension in self.default_classifier:
            if dimension not in self.classifier:
                self.classifier[dimension] = self.default_classifier[dimension]
        self.tournament_attributes = {'length': -1, 'game': None}
        self.cooperations = 0
        self.defections = 0

    def __repr__(self):
        """The string method for the strategy."""
        return self.name

    def _add_noise(self, noise, s1, s2):
        r = random.random()
        if r < noise:
            s1 = flip_dict[s1]
        r = random.random()
        if r < noise:
            s2 = flip_dict[s2]
        return s1, s2

    def strategy(self, opponent):
        """This is a placeholder strategy."""
        return None

    def play(self, opponent, noise=0):
        """This pits two players against each other."""
        s1, s2 = self.strategy(opponent), opponent.strategy(self)
        if noise:
            s1, s2 = self._add_noise(noise, s1, s2)
        update_histories(self, opponent, s1, s2)

    def reset(self):
        """Resets history.

        When creating strategies that create new attributes then this method should be
        re-written (in the inherited class) and should not only reset history but also
        rest all other attributes.
        """
        self.history = []
        self.cooperations = 0
        self.defections = 0
