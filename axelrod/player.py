from collections import defaultdict
from functools import wraps
import random
import copy

from axelrod.actions import Actions, flip_action, Action
from .game import DefaultGame

from typing import Dict, Any

C, D = Actions.C, Actions.D


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
    return (
        not stochastic and
        not inspects_source and
        not manipulates_source and
        not manipulates_state and
        depth in (0, 1)
    )


def obey_axelrod(s):
    """
    A function to check if a strategy obeys Axelrod's original tournament
    rules.
    """
    classifier = s.classifier
    return not (
        classifier['inspects_source'] or
        classifier['manipulates_source'] or
        classifier['manipulates_state'])


def update_history(player, move):
    """Updates histories and cooperation / defections counts following play."""
    # Update histories
    player.history.append(move)
    # Update player counts of cooperation and defection
    if move == C:
        player.cooperations += 1
    elif move == D:
        player.defections += 1


def get_state_distribution_from_history(player, history_1, history_2):
    """Gets state_distribution from player's and opponent's histories."""
    for action, reply in zip(history_1, history_2):
        update_state_distribution(player, action, reply)


def update_state_distribution(player, action, reply):
    """Updates state_distribution following play. """
    last_turn = (action, reply)
    player.state_distribution[last_turn] += 1


def init_args(func):
    """Decorator to simplify the handling of init_args. Use whenever overriding
    Player.__init__ in subclasses of Player that require arguments as follows:

    @init_args
    def __init__(self, myarg1, ...)
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        r = func(self, *args, **kwargs)
        self.init_args = args
        self.init_kwargs = kwargs
        return r
    return wrapper


class Player(object):
    """A class for a player in the tournament.

    This is an abstract base class, not intended to be used directly.
    """

    name = "Player"
    classifier = {} # type: Dict[str, Any]
    default_classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),
        'makes_use_of': None,
        'long_run_time': False,
        'inspects_source': None,
        'manipulates_source': None,
        'manipulates_state': None
    }

    def __new__(cls, *args, **kwargs):
        """Caches arguments for Player cloning."""
        obj = super().__new__(cls)
        obj.init_args = args
        obj.init_kwargs = kwargs
        return obj

    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        self.history = []
        self.classifier = copy.deepcopy(self.classifier)
        if self.name == "Player":
            self.classifier['stochastic'] = False
        for dimension in self.default_classifier:
            if dimension not in self.classifier:
                self.classifier[dimension] = self.default_classifier[dimension]
        self.cooperations = 0
        self.defections = 0
        self.state_distribution = defaultdict(int)
        self.set_match_attributes()

    def receive_match_attributes(self):
        # Overwrite this function if your strategy needs
        # to make use of match_attributes such as
        # the game matrix, the number of rounds or the noise
        pass

    def set_match_attributes(self, length=-1, game=None, noise=0):
        if not game:
            game = DefaultGame
        self.match_attributes = {
            "length": length,
            "game": game,
            "noise": noise
        }
        self.receive_match_attributes()

    def __repr__(self):
        """The string method for the strategy."""
        return self.name

    @staticmethod
    def _add_noise(noise, s1, s2):
        r = random.random()
        if r < noise:
            s1 = flip_action(s1)
        r = random.random()
        if r < noise:
            s2 = flip_action(s2)
        return s1, s2

    def strategy(self, opponent):
        """This is a placeholder strategy."""
        raise NotImplementedError()

    def play(self, opponent, noise=0):
        """This pits two players against each other."""
        s1, s2 = self.strategy(opponent), opponent.strategy(self)
        if noise:
            s1, s2 = self._add_noise(noise, s1, s2)
        update_history(self, s1)
        update_history(opponent, s2)
        update_state_distribution(self, s1, s2)
        update_state_distribution(opponent, s2, s1)

    def clone(self):
        """Clones the player without history, reapplying configuration
        parameters as necessary."""

        # You may be tempted to re-implement using the `copy` module
        # Note that this would require a deepcopy in some cases and there may
        # be significant changes required throughout the library.
        # Override in special cases only if absolutely necessary
        cls = self.__class__
        new_player = cls(*self.init_args, **self.init_kwargs)
        new_player.match_attributes = copy.copy(self.match_attributes)
        return new_player

    def reset(self):
        """Resets history.
        When creating strategies that create new attributes then this method
        should be re-written (in the inherited class) and should not only reset
        history but also rest all other attributes.
        """
        self.history = []
        self.cooperations = 0
        self.defections = 0
        self.state_distribution = defaultdict(int)
