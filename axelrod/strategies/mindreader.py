"""
The player classes in this module do not obey standard rules of the IPD (as
indicated by their classifier). We do not recommend putting a lot of time in to
optimising them.
"""
from axelrod.actions import Actions, Action
from axelrod.player import Player
from axelrod._strategy_utils import look_ahead, inspect_strategy


C, D = Actions.C, Actions.D


class MindReader(Player):
    """A player that looks ahead at what the opponent will do and decides what
    to do.

    Names:

    - Mind reader: Original name by Jason Young
    """

    name = 'Mind Reader'
    classifier = {
        'memory_depth': -10,
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

    def strategy(self, opponent: Player) -> Action:
        """
        Pretends to play the opponent a number of times before each match.
        The primary purpose is to look far enough ahead to see if a defect will
        be punished by the opponent.
        """
        game = self.match_attributes["game"]

        best_strategy = look_ahead(self, opponent, game)

        return best_strategy


class ProtectedMindReader(MindReader):
    """A player that looks ahead at what the opponent will do and decides what
    to do. It is also protected from mind control strategies

    Names:

    - Protected Mind reader: Original name by Jason Young
    """

    name = 'Protected Mind Reader'
    classifier = {
        'memory_depth': -10,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,  # Finds out what opponent will do
        'manipulates_source': True,  # Stops opponent's strategy
        'manipulates_state': False
    }

    def __setattr__(self, name: str, val: str):
        """Stops any other strategy altering the methods of this class """

        if name == 'strategy':
            pass
        else:
            self.__dict__[name] = val


class MirrorMindReader(ProtectedMindReader):
    """A player that will mirror whatever strategy it is playing against by
    cheating and calling the opponent's strategy function instead of its own.

    Names:

    - Protected Mind reader: Original name by Brice Fernandes
    """

    name = 'Mirror Mind Reader'

    classifier = {
        'memory_depth': -10,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,  # Reads and copies the source of the opponent
        'manipulates_source': True,  # Changes own source dynamically
        'manipulates_state': False
    }

    @staticmethod
    def foil_strategy_inspection() -> Action:
        """Foils _strategy_utils.inspect_strategy and _strategy_utils.look_ahead"""
        return C

    def strategy(self, opponent: Player) -> Action:
        """Will read the mind of the opponent and play the opponent's strategy. """
        return inspect_strategy(self, opponent)
