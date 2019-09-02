import copy
import inspect
import itertools
import types
from typing import Any, Dict

import numpy as np

from axelrod.action import Action
from axelrod.game import DefaultGame
from axelrod.history import History
from axelrod.random_ import random_flip

C, D = Action.C, Action.D


# Strategy classifiers


def is_basic(s):
    """
    Defines criteria for a strategy to be considered 'basic'
    """
    stochastic = s.classifier["stochastic"]
    depth = s.classifier["memory_depth"]
    inspects_source = s.classifier["inspects_source"]
    manipulates_source = s.classifier["manipulates_source"]
    manipulates_state = s.classifier["manipulates_state"]
    return (
        not stochastic
        and not inspects_source
        and not manipulates_source
        and not manipulates_state
        and depth in (0, 1)
    )


def obey_axelrod(s):
    """
    A function to check if a strategy obeys Axelrod's original tournament
    rules.
    """
    classifier = s.classifier
    return not (
        classifier["inspects_source"]
        or classifier["manipulates_source"]
        or classifier["manipulates_state"]
    )


def simultaneous_play(player, coplayer, noise=0):
    """This pits two players against each other."""
    s1, s2 = player.strategy(coplayer), coplayer.strategy(player)
    if noise:
        s1 = random_flip(s1, noise)
        s2 = random_flip(s2, noise)
    player.update_history(s1, s2)
    coplayer.update_history(s2, s1)
    return s1, s2


class Player(object):
    """A class for a player in the tournament.

    This is an abstract base class, not intended to be used directly.
    """

    name = "Player"
    classifier = {}  # type: Dict[str, Any]
    default_classifier = {
        "stochastic": False,
        "memory_depth": float("inf"),
        "makes_use_of": None,
        "long_run_time": False,
        "inspects_source": None,
        "manipulates_source": None,
        "manipulates_state": None,
    }

    def __new__(cls, *args, **kwargs):
        """Caches arguments for Player cloning."""
        obj = super().__new__(cls)
        obj.init_kwargs = cls.init_params(*args, **kwargs)
        return obj

    @classmethod
    def init_params(cls, *args, **kwargs):
        """
        Return a dictionary containing the init parameters of a strategy
        (without 'self').
        Use *args and *kwargs as value if specified
        and complete the rest with the default values.
        """
        sig = inspect.signature(cls.__init__)
        # The 'self' parameter needs to be removed or the first *args will be
        # assigned to it
        self_param = sig.parameters.get("self")
        new_params = list(sig.parameters.values())
        new_params.remove(self_param)
        sig = sig.replace(parameters=new_params)
        boundargs = sig.bind_partial(*args, **kwargs)
        boundargs.apply_defaults()
        return boundargs.arguments

    def __init__(self):
        """Initiates an empty history."""
        self._history = History()
        self.classifier = copy.deepcopy(self.classifier)
        for dimension in self.default_classifier:
            if dimension not in self.classifier:
                self.classifier[dimension] = self.default_classifier[dimension]
        self.set_match_attributes()

    def __eq__(self, other):
        """
        Test if two players are equal.
        """
        if self.__repr__() != other.__repr__():
            return False

        for attribute in set(list(self.__dict__.keys()) + list(other.__dict__.keys())):

            value = getattr(self, attribute, None)
            other_value = getattr(other, attribute, None)

            if isinstance(value, np.ndarray):
                if not (np.array_equal(value, other_value)):
                    return False

            elif isinstance(value, types.GeneratorType) or isinstance(
                value, itertools.cycle
            ):
                # Split the original generator so it is not touched
                generator, original_value = itertools.tee(value)
                other_generator, original_other_value = itertools.tee(other_value)

                if isinstance(value, types.GeneratorType):
                    setattr(self, attribute, (ele for ele in original_value))
                    setattr(other, attribute, (ele for ele in original_other_value))
                else:
                    setattr(self, attribute, itertools.cycle(original_value))
                    setattr(other, attribute, itertools.cycle(original_other_value))

                for _ in range(200):
                    try:
                        if next(generator) != next(other_generator):
                            return False
                    except StopIteration:
                        break

            # Code for a strange edge case where each strategy points at each
            # other
            elif value is other and other_value is self:
                pass
            else:
                if value != other_value:
                    return False
        return True

    def receive_match_attributes(self):
        # Overwrite this function if your strategy needs
        # to make use of match_attributes such as
        # the game matrix, the number of rounds or the noise
        pass

    def set_match_attributes(self, length=-1, game=None, noise=0):
        if not game:
            game = DefaultGame
        self.match_attributes = {"length": length, "game": game, "noise": noise}
        self.receive_match_attributes()

    def __repr__(self):
        """The string method for the strategy.
        Appends the `__init__` parameters to the strategy's name."""
        name = self.name
        prefix = ": "
        gen = (value for value in self.init_kwargs.values() if value is not None)
        for value in gen:
            try:
                if issubclass(value, Player):
                    value = value.name
            except TypeError:
                pass
            name = "".join([name, prefix, str(value)])
            prefix = ", "
        return name

    def __getstate__(self):
        """Used for pickling. Override if Player contains unpickleable attributes."""
        return self.__dict__

    def strategy(self, opponent):
        """This is a placeholder strategy."""
        raise NotImplementedError()

    def play(self, opponent, noise=0):
        """This pits two players against each other."""
        return simultaneous_play(self, opponent, noise)

    def clone(self):
        """Clones the player without history, reapplying configuration
        parameters as necessary."""

        # You may be tempted to re-implement using the `copy` module
        # Note that this would require a deepcopy in some cases and there may
        # be significant changes required throughout the library.
        # Consider overriding in special cases only if necessary
        cls = self.__class__
        new_player = cls(**self.init_kwargs)
        new_player.match_attributes = copy.copy(self.match_attributes)
        return new_player

    def reset(self):
        """Resets a player to its initial state

        This method is called at the beginning of each match (between a pair
        of players) to reset a player's state to its initial starting point.
        It ensures that no 'memory' of previous matches is carried forward.
        """
        # This also resets the history.
        self.__init__(**self.init_kwargs)

    def update_history(self, play, coplay):
        self.history.append(play, coplay)

    @property
    def history(self):
        return self._history

    # Properties maintained for legacy API, can refactor to self.history.X
    # in 5.0.0 to reduce function call overhead.
    @property
    def cooperations(self):
        return self._history.cooperations

    @property
    def defections(self):
        return self._history.defections

    @property
    def state_distribution(self):
        return self._history.state_distribution
