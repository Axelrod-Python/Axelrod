import inspect
import random

flip_dict = {'C': 'D', 'D':'C'}

class Player(object):
    """A class for a player in the tournament.

    This is an abstract base class, not intended to be used directly.
    """

    name = "Player"
    noise_probability = 0.0

    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        self.history = []
        self.stochastic = "random" in inspect.getsource(self.__class__)
        if self.name == "Player":
            self.stochastic = False

    def __repr__(self):
        """The string method for the strategy."""
        return self.name

    def strategy(self, opponent):
        """This is a placeholder strategy."""
        return None

    def play(self, opponent):
        """This pits two players against each other."""
        s1, s2 = self.strategy(opponent), opponent.strategy(self)
        if self.noise_probability:
            r = random.random()
            if r < self.noise_probability:
                s1 = flip_dict[s1]
            r = random.random()
            if r < self.noise_probability:
                s2 = flip_dict[s2]
        self.history.append(s1)
        opponent.history.append(s2)

    def reset(self):
        """Resets history.

        When creating strategies that create new attributes then this method should be
        re-written (in the inherited class) and should not only reset history but also
        rest all other attributes.
        """
        self.history = []
