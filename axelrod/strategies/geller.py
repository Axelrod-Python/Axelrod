"""
The player classes in this module do not obey standard rules of the IPD (as
indicated by their classifier). We do not recommend putting a lot of time in to
optimising them.
"""

from axelrod.action import Action
from axelrod.player import Player
from axelrod.random_ import random_choice
from axelrod._strategy_utils import inspect_strategy

C, D = Action.C, Action.D


class Geller(Player):
    """Observes what the player will do in the next round and adjust.

    If unable to do this: will play randomly.


    This code is inspired by Matthew Williams' talk
    "Cheating at rock-paper-scissors — meta-programming in Python"
    given at Django Weekend Cardiff in February 2014.

    His code is here: https://github.com/mattjw/rps_metaprogramming
    and there's some more info here: http://www.mattjw.net/2014/02/rps-metaprogramming/

    This code is **way** simpler than Matt's, as in this exercise we already
    have access to the opponent instance, so don't need to go
    hunting for it in the stack. Instead we can just call it to
    see what it's going to play, and return a result based on that

    This is almost certainly cheating, and more than likely against the
    spirit of the 'competition' :-)

    Names:

    - Geller: Original name by Martin Chorley (@martinjc)
    """

    name = 'Geller'
    classifier = {
        'memory_depth': float("inf"),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,  # Finds out what opponent will do
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def foil_strategy_inspection() -> Action:
        """Foils _strategy_utils.inspect_strategy and _strategy_utils.look_ahead"""
        return random_choice(0.5)

    def strategy(self, opponent: Player) -> Action:
        """
        Look at what the opponent will play in the next round and choose a strategy
        that gives the least jail time, which is is equivalent to playing the same
        strategy as that which the opponent will play.
        """

        return inspect_strategy(self, opponent)


class GellerCooperator(Geller):
    """Observes what the player will do (like :code:`Geller`) but if unable to
    will cooperate.

    Names:

    - Geller Cooperator: Original name by Karol Langner
    """
    name = 'Geller Cooperator'
    classifier = {
        'memory_depth': float("inf"),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,  # Finds out what opponent will do
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def foil_strategy_inspection() -> Action:
        """
        Foils _strategy_utils.inspect_strategy and _strategy_utils.look_ahead
        """
        return C


class GellerDefector(Geller):
    """Observes what the player will do (like :code:`Geller`) but if unable to
    will defect.

    Names:

    - Geller Defector: Original name by Karol Langner
    """
    name = 'Geller Defector'
    classifier = {
        'memory_depth': float("inf"),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,  # Finds out what opponent will do
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def foil_strategy_inspection() -> Action:
        """Foils _strategy_utils.inspect_strategy and _strategy_utils.look_ahead"""
        return D
