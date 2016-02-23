import collections
import functools
import itertools

from axelrod import Actions, Player, init_args


class SequencePlayer(Player):
    """Abstract base class for players that use a generated sequence to
    determine their plays."""

    @init_args
    def __init__(self, generator_function, generator_args=()):
        Player.__init__(self)
        # Initialize the sequence generator
        self.generator_function = generator_function
        self.generator_args = generator_args
        self.sequence_generator = self.generator_function(*self.generator_args)

    def meta_strategy(self, value):
        """Determines how to map the sequence value to cooperate or defect.
        By default, treat values like python truth values. Override in child
        classes for alternate behaviors."""
        if value == 0:
            return Actions.D
        else:
            return Actions.C

    def strategy(self, opponent):
        # Iterate through the sequence and apply the meta strategy
        for s in self.sequence_generator:
            return self.meta_strategy(s)

    def reset(self):
        # Be sure to reset the sequence generator
        Player.reset(self)
        self.sequence_generator = self.generator_function(*self.generator_args)


class Memoized(object):
   """Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated). From:
   https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
   """
   def __init__(self, func):
        self.func = func
        self.cache = {}

   def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

   def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

   def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


@Memoized
def recursive_thue_morse(n):
    """The recursive definition of the Thue-Morse sequence. The first few terms
    of the Thue-Morse sequence are:
    0 1 1 0 1 0 0 1 1 0 0 1 0 1 1 0 . . ."""

    if n == 0:
        return 0
    if n % 2 == 0:
        return recursive_thue_morse(n / 2)
    if n % 2 == 1:
        return 1 - recursive_thue_morse((n - 1) / 2)

def thue_morse_generator(start=0):
    """A generator for the Thue-Morse sequence."""

    for n in itertools.count(start):
        yield recursive_thue_morse(n)


class ThueMorse(SequencePlayer):
    """
    A player who cooperates or defects according to the Thue-Morse sequence.

    The first few terms of the Thue-Morse sequence are:
    0 1 1 0 1 0 0 1 1 0 0 1 0 1 1 0 . . .
    """

    name = 'ThueMorse'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self):
        SequencePlayer.__init__(self, thue_morse_generator, (0,))


class ThueMorseInverse(ThueMorse):
    """A player who defects or cooperates according to the Thue-Morse sequence
    (Inverse of ThueMorse)."""

    name = 'ThueMorseInverse'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self):
        SequencePlayer.__init__(self, thue_morse_generator, (0,))

    def meta_strategy(self, value):
        # Switch the default cooperate and defect action on 0 or 1
        if value == 0:
            return Actions.C
        else:
            return Actions.D

