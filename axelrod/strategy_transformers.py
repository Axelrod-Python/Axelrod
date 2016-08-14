
"""
Strategy Transformers -- class decorators that transform the behavior of any
strategy.

See the various Meta strategies for another type of transformation.
"""

import inspect
import random
import collections
from numpy.random import choice

from .actions import Actions, flip_action
from .random_ import random_choice

C, D = Actions.C, Actions.D

# Note: After a transformation is applied,
# the player's history is overwritten with the modified history
# just like in the noisy tournament case
# This can lead to unexpected behavior, such as when
# FlipTransform is applied to Alternator


def StrategyTransformerFactory(strategy_wrapper, name_prefix=None):
    """Modify an existing strategy dynamically by wrapping the strategy
    method with the argument `strategy_wrapper`.

    Parameters
    ----------
    strategy_wrapper: function
        A function of the form `strategy_wrapper(player, opponent, proposed_action, *args, **kwargs)`
        Can also use a class that implements
            def __call__(self, player, opponent, action)
    wrapper_args: tuple
        Any arguments to pass to the wrapper
    wrapper_kwargs: dict
        Any keyword arguments to pass to the wrapper
    name_prefix: string, "Transformed "
        A string to prepend to the strategy and class name
    """

    # Create a class that applies a wrapper function to the strategy method
    # of a given class. We use a class here instead of a function so that the
    # decorator can have arguments.

    class Decorator(object):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            if "name_prefix" in kwargs:
                self.name_prefix = kwargs["name_prefix"]
            else:
                self.name_prefix = name_prefix

        def __call__(self, PlayerClass):
            """
            Parameters
            ----------
            PlayerClass: A subclass of axelrod.Player, e.g. Cooperator
                The Player Class to modify
            name_prefix: str
                A string to prepend to the Player and Class name

            Returns
            -------
            new_class, class object
                A class object that can create instances of the modified
                PlayerClass
            """

            args = self.args
            kwargs = self.kwargs
            try:
                # if "name_prefix" in kwargs remove as only want dec arguments
                del kwargs["name_prefix"]
            except KeyError:
                pass

            # Define the new strategy method, wrapping the existing method
            # with `strategy_wrapper`
            def strategy(self, opponent):
                # Is the original strategy method a static method?
                argspec = inspect.getargspec(getattr(PlayerClass, "strategy"))
                if 'self' in argspec.args:
                    # it's not a static method
                    proposed_action = PlayerClass.strategy(self, opponent)
                else:
                    proposed_action = PlayerClass.strategy(opponent)
                # Apply the wrapper
                return strategy_wrapper(self, opponent, proposed_action,
                                        *args, **kwargs)

            # Define a new class and wrap the strategy method
            # Modify the PlayerClass name
            new_class_name = PlayerClass.__name__
            name = PlayerClass.name
            name_prefix = self.name_prefix
            if name_prefix:
                # Modify the Player name (class variable inherited from Player)
                new_class_name = name_prefix + PlayerClass.__name__
                # Modify the Player name (class variable inherited from Player)
                name = name_prefix + ' ' + PlayerClass.name
            # Dynamically create the new class
            new_class = type(
                new_class_name, (PlayerClass,),
                {
                    "name": name,
                    "strategy": strategy,
                    "__module__": PlayerClass.__module__
                })
            return new_class
    return Decorator


def compose_transformers(t1, t2):
    """Compose transformers without having to invoke the first on
    a PlayerClass."""
    class Composition(object):
        def __init__(self):
            self.t1 = t1
            self.t2 = t2

        def __call__(self, PlayerClass):
            return t1(t2(PlayerClass))
    return Composition()


def generic_strategy_wrapper(player, opponent, proposed_action, *args, **kwargs):
    """
    Strategy wrapper functions should be of the following form.

    Parameters
    ----------
    player: Player object or subclass (self)
    opponent: Player object or subclass
    proposed_action: an axelrod.Action, C or D
        The proposed action by the wrapped strategy
        proposed_action = Player.strategy(...)
    args, kwargs:
        Any additional arguments that you need.

    Returns
    -------
    action: an axelrod.Action, C or D

    """

    # This example just passes through the proposed_action
    return proposed_action

IdentityTransformer = StrategyTransformerFactory(generic_strategy_wrapper)


def flip_wrapper(player, opponent, action):
    """Applies flip_action at the class level."""
    return flip_action(action)

FlipTransformer = StrategyTransformerFactory(
    flip_wrapper, name_prefix="Flipped")


def noisy_wrapper(player, opponent, action, noise=0.05):
    """Applies flip_action at the class level."""
    r = random.random()
    if r < noise:
        return flip_action(action)
    return action

NoisyTransformer = StrategyTransformerFactory(
    noisy_wrapper, name_prefix="Noisy")


def forgiver_wrapper(player, opponent, action, p):
    """If a strategy wants to defect, flip to cooperate with the given
    probability."""
    if action == D:
        return random_choice(p)
    return C

ForgiverTransformer = StrategyTransformerFactory(
    forgiver_wrapper, name_prefix="Forgiving")


def initial_sequence(player, opponent, action, initial_seq):
    """Play the moves in `seq` first (must be a list), ignoring the strategy's
    moves until the list is exhausted."""

    index = len(player.history)
    if index < len(initial_seq):
        return initial_seq[index]
    return action

InitialTransformer = StrategyTransformerFactory(initial_sequence,
                                                name_prefix="Initial")


def final_sequence(player, opponent, action, seq):
    """Play the moves in `seq` first, ignoring the strategy's moves until the
    list is exhausted."""

    length = player.match_attributes["length"]
    player.classifier["makes_use_of"].update(["length"])

    if length < 0:  # default is -1
        return action

    index = length - len(player.history)
    # If for some reason we've overrun the expected game length, just pass
    # the intended action through
    if len(player.history) >= length:
        return action
    # Check if we're near the end and need to start passing the actions
    # from seq for the final few rounds.
    if index <= len(seq):
        return seq[-index]
    return action

FinalTransformer = StrategyTransformerFactory(final_sequence,
                                              name_prefix="Final")


def history_track_wrapper(player, opponent, action):
    """Wrapper to track a player's history in a variable `._recorded_history`."""
    try:
        player._recorded_history.append(action)
    except AttributeError:
        player._recorded_history = [action]
    return action

TrackHistoryTransformer = StrategyTransformerFactory(
    history_track_wrapper, name_prefix="HistoryTracking")


def deadlock_break_wrapper(player, opponent, action):
    """Detect and attempt to break deadlocks by cooperating."""
    if len(player.history) < 2:
        return action
    last_round = (player.history[-1], opponent.history[-1])
    penultimate_round = (player.history[-2], opponent.history[-2])
    if (penultimate_round, last_round) == ((C, D), (D, C)) or \
       (penultimate_round, last_round) == ((D, C), (C, D)):
        # attempt to break deadlock by Cooperating
        return C
    return action

DeadlockBreakingTransformer = StrategyTransformerFactory(
    deadlock_break_wrapper, name_prefix="DeadlockBreaking")


def grudge_wrapper(player, opponent, action, grudges):
    """After `grudges` defections, defect forever."""
    if opponent.defections > grudges:
        return D
    return action

GrudgeTransformer = StrategyTransformerFactory(
    grudge_wrapper, name_prefix="Grudging")


def apology_wrapper(player, opponent, action, myseq, opseq):
    length = len(myseq)
    if len(player.history) < length:
        return action
    if (myseq == player.history[-length:]) and \
       (opseq == opponent.history[-length:]):
        return C
    return action

ApologyTransformer = StrategyTransformerFactory(
    apology_wrapper, name_prefix="Apologizing")


def mixed_wrapper(player, opponent, action, probability, m_player):
    """Randomly picks a strategy to play, either from a distribution on a list
    of players or a single player.

    In essence creating a mixed strategy.

    Parameters
    ----------

    probability: a float (or integer: 0 or 1) OR an iterable representing a
        an incomplete probability distribution (entries to do not have to sum to
        1). Eg: 0, 1, [.5,.5], (.5,.3)
    m_players: a single player class or iterable representing set of player
        classes to mix from.
        Eg: axelrod.TitForTat, [axelod.Cooperator, axelrod.Defector]
    """

    # If a single probability, player is passed
    if isinstance(probability, float) or isinstance(probability, int):
        m_player = [m_player]
        probability = [probability]

    # If a probability distribution, players is passed
    if isinstance(probability, collections.Iterable) and \
            isinstance(m_player, collections.Iterable):
        mutate_prob = sum(probability)  # Prob of mutation
        if mutate_prob > 0:
            # Distribution of choice of mutation:
            normalised_prob = [prob / float(mutate_prob)
                               for prob in probability]
            if random.random() < mutate_prob:
                p = choice(list(m_player), p=normalised_prob)()
                p.history = player.history
                return p.strategy(opponent)

    return action

MixedTransformer = StrategyTransformerFactory(
    mixed_wrapper, name_prefix="Mutated")

# Strategy wrappers as classes


class RetaliationWrapper(object):
    """Retaliates `retaliations` times after a defection (cumulative)."""

    def __call__(self, player, opponent, action, retaliations):
        if len(player.history) == 0:
            self.retaliation_count = 0
            return action
        if opponent.history[-1] == D:
            self.retaliation_count += retaliations - 1
            return D
        if self.retaliation_count == 0:
            return action
        if self.retaliation_count > 0:
            self.retaliation_count -= 1
            return D

RetaliationTransformer = StrategyTransformerFactory(
    RetaliationWrapper(), name_prefix="Retaliating")


class RetaliationUntilApologyWrapper(object):
    """Enforces the TFT rule that the opponent pay back a defection with a
    cooperation for the player to stop defecting."""

    def __call__(self, player, opponent, action):
        if len(player.history) == 0:
            self.is_retaliating = False
            return action
        if opponent.history[-1] == D:
            self.is_retaliating = True
        if self.is_retaliating:
            if opponent.history[-1] == C:
                self.is_retaliating = False
                return C
            return D
        return action

RetaliateUntilApologyTransformer = StrategyTransformerFactory(
    RetaliationUntilApologyWrapper(), name_prefix="RUA")
