"""
Strategy Transformers -- class decorators that transform the behavior of any
strategy.

See the various Meta strategies for another type of transformation.
"""

import collections
import copy
import inspect
import random
from numpy.random import choice
from .actions import Actions, flip_action
from .random_ import random_choice


C, D = Actions.C, Actions.D

# Note: After a transformation is applied, the player's history is overwritten
# with the modified history just like in the noisy tournament case. This can
# lead to unexpected behavior, such as when FlipTransform is applied to
# Alternator.


def StrategyTransformerFactory(strategy_wrapper, name_prefix=None,
                               reclassifier=None):
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
    reclassifier: function,
        A function which will update the classifier of the strategy being
        transformed
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

            Returns
            -------
            new_class, class object
                A class object that can create instances of the modified
                PlayerClass
            """

            args = self.args
            kwargs = self.kwargs
            try:
                # If "name_prefix" in kwargs remove as only want decorator
                # arguments
                del kwargs["name_prefix"]
            except KeyError:
                pass
            try:
                del kwargs["reclassifier"]
            except KeyError:
                pass

            # Is the original strategy method a static method?
            signature = inspect.signature(PlayerClass.strategy)
            strategy_args = [p.name for p in signature.parameters.values()
                    if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD]
            is_static = True
            if len(strategy_args) > 1:
                is_static = False

            # Define the new strategy method, wrapping the existing method
            # with `strategy_wrapper`
            def strategy(self, opponent):

                if is_static:
                    # static method
                    proposed_action = PlayerClass.strategy(opponent)
                else:
                    proposed_action = PlayerClass.strategy(self, opponent)

                # Apply the wrapper
                return strategy_wrapper(self, opponent, proposed_action,
                                        *args, **kwargs)

            # Modify the PlayerClass name
            new_class_name = PlayerClass.__name__
            name = PlayerClass.name
            name_prefix = self.name_prefix
            if name_prefix:
                # Modify the Player name (class variable inherited from Player)
                new_class_name = ''.join([name_prefix, PlayerClass.__name__])
                # Modify the Player name (class variable inherited from Player)
                name = ' '.join([name_prefix, PlayerClass.name])

            original_classifier = copy.deepcopy(PlayerClass.classifier) # Copy
            if reclassifier is not None:
                classifier = reclassifier(original_classifier, *args, **kwargs,)
            else:
                classifier = original_classifier

            # Define the new __repr__ method to add the wrapper arguments
            # at the end of the name
            def __repr__(self):
                name = PlayerClass.__repr__(self)
                # add eventual transformers' arguments in name
                prefix = ': '
                for arg in args:
                    try:
                        arg = [player.name for player in arg]
                    except TypeError:
                        pass
                    except AttributeError:
                        pass
                    name = ''.join([name, prefix, str(arg)])
                    prefix = ', '
                return name

            # Define a new class and wrap the strategy method
            # Dynamically create the new class
            new_class = type(
                new_class_name, (PlayerClass,),
                {
                    "name": name,
                    "original_class": PlayerClass,
                    "strategy": strategy,
                    "__repr__": __repr__,
                    "__module__": PlayerClass.__module__,
                    "classifier": classifier,
                    "__doc__": PlayerClass.__doc__,
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


def generic_strategy_wrapper(player, opponent, proposed_action, *args,
                             **kwargs):
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


def dual_wrapper(player, opponent, proposed_action):
    """Wraps the players strategy function to produce the Dual.

    The Dual of a strategy will return the exact opposite set of moves to the
    original strategy when both are faced with the same history.

    A formal definition can be found in [Ashlock2010]_.
    http://doi.org/10.1109/ITW.2010.5593352

    Parameters
    ----------
    player: Player object or subclass (self)
    opponent: Player object or subclass
    proposed_action: axelrod.Action, C or D
        The proposed action by the wrapped strategy

    Returns
    -------
    action: an axelrod.Action, C or D
    """
    if not player.history:
        player.original_player = player.original_class(**player.init_kwargs)

    action = player.original_player.strategy(opponent)
    player.original_player.history.append(action)
    return flip_action(action)


DualTransformer = StrategyTransformerFactory(dual_wrapper, name_prefix="Dual")


def noisy_wrapper(player, opponent, action, noise=0.05):
    """Applies flip_action at the class level."""
    r = random.random()
    if r < noise:
        return flip_action(action)
    return action

def noisy_reclassifier(original_classifier, noise):
    """Function to reclassify the strategy"""
    if noise not in (0, 1):
        original_classifier["stochastic"] = True
    return original_classifier

NoisyTransformer = StrategyTransformerFactory(
    noisy_wrapper, name_prefix="Noisy", reclassifier=noisy_reclassifier)


def forgiver_wrapper(player, opponent, action, p):
    """If a strategy wants to defect, flip to cooperate with the given
    probability."""
    if action == D:
        return random_choice(p)
    return C

def forgiver_reclassifier(original_classifier, p):
    """Function to reclassify the strategy"""
    if p not in (0, 1):
        original_classifier["stochastic"] = True
    return original_classifier

ForgiverTransformer = StrategyTransformerFactory(
    forgiver_wrapper, name_prefix="Forgiving",
    reclassifier=forgiver_reclassifier)


def nice_wrapper(player, opponent, action):
    """Makes sure that the player doesn't defect unless the opponent has already
    defected."""
    if action == D:
        if opponent.defections == 0:
            return C
    return action


NiceTransformer = StrategyTransformerFactory(
    nice_wrapper, name_prefix="Nice")


def initial_sequence(player, opponent, action, initial_seq):
    """Play the moves in `seq` first (must be a list), ignoring the strategy's
    moves until the list is exhausted."""

    index = len(player.history)
    if index < len(initial_seq):
        return initial_seq[index]
    return action

def initial_reclassifier(original_classifier, initial_seq):
    """
    If needed this extends the memory depth to be the length of the initial
    sequence
    """
    original_classifier["memory_depth"] = max(len(initial_seq),
                                            original_classifier["memory_depth"])
    return original_classifier


InitialTransformer = StrategyTransformerFactory(initial_sequence,
                                            name_prefix="Initial",
                                            reclassifier=initial_reclassifier)


def final_sequence(player, opponent, action, seq):
    """Play the moves in `seq` first, ignoring the strategy's moves until the
    list is exhausted."""

    length = player.match_attributes["length"]

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

def final_reclassifier(original_classifier, seq):
    """Reclassify the strategy"""
    original_classifier["makes_use_of"].update(["length"])
    original_classifier["memory_depth"] = max(len(seq),
                                            original_classifier["memory_depth"])
    return original_classifier


FinalTransformer = StrategyTransformerFactory(final_sequence,
                                              name_prefix="Final",
                                              reclassifier=final_reclassifier)


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
            normalised_prob = [prob / mutate_prob
                               for prob in probability]
            if random.random() < mutate_prob:
                p = choice(list(m_player), p=normalised_prob)()
                p.history = player.history
                return p.strategy(opponent)

    return action

def mixed_reclassifier(original_classifier, probability, m_player):
    """Function to reclassify the strategy"""
    # If a single probability, player is passed
    if isinstance(probability, float) or isinstance(probability, int):
        m_player = [m_player]
        probability = [probability]

    if min(probability) == max(probability) == 0:  # No probability given
        return original_classifier

    if 1 in probability:  # If all probability  given to one player
        player = m_player[probability.index(1)]
        original_classifier["stochastic"] = player.classifier["stochastic"]
        return original_classifier

    # Otherwise: stochastic.
    original_classifier["stochastic"] = True
    return original_classifier

MixedTransformer = StrategyTransformerFactory(
    mixed_wrapper, name_prefix="Mutated", reclassifier=mixed_reclassifier)


def joss_ann_wrapper(player, opponent, proposed_action, probability):
    """Wraps the players strategy function to produce the Joss-Ann.

    The Joss-Ann of a strategy is a new strategy which has a probability of
    choosing the move C, a probability of choosing the move D, and otherwise
    uses the response appropriate to the original strategy.

    A formal definition can be found in [Ashlock2010]_.
    http://doi.org/10.1109/ITW.2010.5593352

    Parameters
    ----------

    player: Player object or subclass (self)
    opponent: Player object or subclass
    proposed_action: axelrod.Action, C or D
        The proposed action by the wrapped strategy
    probability: tuple
        a tuple or list representing a probability distribution of playing move
        C or D (doesn't have to be complete) ie. (0, 1) or (0.2, 0.3)

    Returns
    -------
    action: an axelrod.Action, C or D
    """
    if sum(probability) > 1:
        probability = tuple([i / sum(probability) for i in probability])

    remaining_probability = max(0, 1 - probability[0] - probability[1])
    probability += (remaining_probability,)
    options = [C, D, proposed_action]
    action = choice(options, p=probability)
    return action

def jossann_reclassifier(original_classifier, probability):
    """
    Reclassify: note that if probabilities are (0, 1) or (1, 0) then we override
    the original classifier.
    """
    if sum(probability) > 1:
        probability = tuple([i / sum(probability) for i in probability])

    if probability in [(1, 0), (0, 1)]:
        original_classifier["stochastic"] = False
    elif sum(probability) != 0:
        original_classifier["stochastic"] = True

    return original_classifier


JossAnnTransformer = StrategyTransformerFactory(
    joss_ann_wrapper, name_prefix="Joss-Ann", reclassifier=jossann_reclassifier)


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
