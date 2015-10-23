
"""
Strategy Transformers -- class decorators that transform the behavior of any
strategy.

Run Axelrod one tournament

Flip Action
Forgiver
Initial Sequence
Final Sequence

TFT -- force a repayment, return to other strategy

Noisy
RetaliateUntilApology

Compose.

Memory-depth inference

As Decorators

Meta Strategies

"""

import random
from types import FunctionType

import axelrod
from axelrod import flip_action, random_choice, simulate_play, Actions
C, D = Actions.C, Actions.D

# Note: the history is overwritten with the modified history
# Just like in the Noisy case
# This can lead to unexpected behavior, such as when
# Flip transform is applied to Alternator


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

def StrategyTransformerFactory(strategy_wrapper, wrapper_args=(), wrapper_kwargs={},
                        name_prefix="Transformed "):
    """Modify an existing strategy dynamically by wrapping the strategy
    method with the argument `strategy_wrapper`.

    Parameters
    ----------
    strategy_wrapper: function
        A function of the form `strategy_wrapper(player, opponent, proposed_action, *args, **kwargs)`
    wrapper_args: tuple
        Any arguments to pass to the wrapper
    wrapper_kwargs: dict
        Any keyword arguments to pass to the wrapper
    name_prefix: string, "Transformed "
        A string to prepend to the strategy and class name
    """

    # Create a function that applies a wrapper function to the strategy method
    # of a given class
    def decorate(PlayerClass):
        """
        Parameters
        ----------
        PlayerClass: A subclass of axelrod.Player, e.g. Cooperator

        Returns
        -------
        new_class, class object
            A class object that can create instances of the modified PlayerClass
        """

        # Define the new strategy method, wrapping the existing method
        # with `strategy_wrapper`
        def strategy(self, opponent):
            # Is the original strategy method a static method?
            if isinstance(PlayerClass.strategy, FunctionType):
                proposed_action = PlayerClass.strategy(opponent)
            else:
                proposed_action = PlayerClass.strategy(self, opponent)
            # Apply the wrapper
            return strategy_wrapper(self, opponent, proposed_action,
                                    *wrapper_args, **wrapper_kwargs)

        # Define a new class and wrap the strategy method
        # Modify the PlayerClass name
        new_class_name = name_prefix + PlayerClass.__name__
        # Modify the Player name (class variable inherited from Player)
        name = name_prefix + PlayerClass.name
        # Dynamically create the new class
        new_class = type(new_class_name, (PlayerClass,),
                         {"name": name, "strategy": strategy})
        return new_class
    return decorate

def flip_wrapper(player, opponent, action):
    """Applies flip_action at the class level."""
    return flip_action(action)

FlipTransformer = StrategyTransformerFactory(flip_wrapper, name_prefix="Flipped ")

def forgiver_wrapper(player, opponent, action, p):
    """If a strategy wants to defect, flip to cooperate with the given
    probability."""
    if action == D:
        return random_choice(p)
    return C

def ForgiverTransformer(p):
    return StrategyTransformerFactory(forgiver_wrapper, wrapper_args=(p,))

def initial_sequence(player, opponent, action, initial_seq):
    """Play the moves in `seq` first (must be a list), ignoring the strategy's
    moves until the list is exhausted."""
    index = len(player.history)
    if index < len(initial_seq):
        return initial_seq[index]
    return action

## Defection initially three times
def InitialTransformer(seq=None):
    if not seq:
        seq = [D] * 3
    transformer = StrategyTransformerFactory(initial_sequence, wrapper_args=(seq,),
                                      name_prefix="Initial ")
    return transformer

def final_sequence(player, opponent, action, seq):
    """Play the moves in `seq` first, ignoring the strategy's
    moves until the list is exhausted."""
    try:
        length = player.tournament_attributes["length"]
    except KeyError:
        return action
    finally:
        if length < 0: # default is -1
            return action

    index = length - len(player.history)
    if index <= len(seq):
        return seq[-index]
    return action

# Defect on last N actions
def FinalTransformer(seq=None):
    if not seq:
        seq = [D] * 3
    transformer = StrategyTransformerFactory(final_sequence, wrapper_args=(seq,))
    return transformer


# Strategy wrapper as a class example
class RetaliationWrapper(object):
    def __init__(self):
        self.is_retaliating = False

    def __call__(self, player, opponent, action):
        if len(player.history) == 0:
            return action
        if opponent.history[-1]:
            self.is_retaliating = True
            return D
        if self.is_retaliating:
            if opponent.history[-1] == C:
                self.is_retaliating = False
                return C
            return D
        return action

def RetailiateUntilApologyTransformer():
    strategy_wrapper = RetaliationWrapper()
    return StrategyTransformerFactory(strategy_wrapper, name_prefix="RUA ")



#if __name__ == "__main__":
    ## Cooperator to Defector
    #p1 = axelrod.Cooperator()
    #p2 = FlipTransformer(axelrod.Cooperator)() # Defector
    #print p1, p2
    #print simulate_play(p1, p2)
    #print simulate_play(p1, p2)

    ## Test that cloning preserves transform
    #p3 = p2.clone()
    #print simulate_play(p1, p3)
    #print simulate_play(p1, p3)

    ## Forgiving example
    #p1 = ForgiverTransformer(axelrod.Defector)()
    #print simulate_play(p1, p2)
    #print simulate_play(p1, p2)
    #print simulate_play(p1, p2)
    #print simulate_play(p1, p2)
    #print simulate_play(p1, p2)
    #print simulate_play(p1, p2)

    ## Difference between Alternator and CyclerCD
    #p1 = axelrod.Cycler(cycle="CD")
    #p2 = FlipTransformer(axelrod.Cycler)(cycle="CD")
    #for _ in range(5):
        #p1.play(p2)
    #print p1.history, p2.history

    ## Initial play transformer
    #p1 = axelrod.Cooperator()
    #p2 = InitialTransformer()(axelrod.Cooperator)()

    #for _ in range(6):
        #p1.play(p2)
    #print p1.history, p2.history

    ## Final Play transformer
    #p1 = FinalTransformer()(axelrod.Cooperator)()
    #p2 = axelrod.Cooperator()
    #p1.tournament_attributes["length"] = 6

    #for _ in range(6):
        #p1.play(p2)
    #print p1.history, p2.history


    ## Composition
    #cls1 = InitialTransformer()(axelrod.Cooperator)
    #cls2 = FinalTransformer()(cls1)
    #p1 = cls2()

    #p2 = axelrod.Cooperator()
    #p1.tournament_attributes["length"] = 8

    #for _ in range(8):
        #p1.play(p2)
    #print p1.history

    ## Composition
    ##cls2 = FinalTransformer()(InitialTransformer(axelrod.Cooperator))
    ##p1 = cls2()

    #cls1 = InitialTransformer([D, D, D])(axelrod.Cooperator)
    #cls2 = FinalTransformer([D, D])(cls1)
    #p1 = cls2()

    #p2 = axelrod.Cooperator()
    #p1.tournament_attributes["length"] = 8

    #for _ in range(8):
        #p1.play(p2)
    #print p1.history


