import inspect

from axelrod import Actions, Player
from axelrod._strategy_utils import look_ahead


C, D = Actions.C, Actions.D

class MindReader(Player):
    """A player that looks ahead at what the opponent will do and decides what to do."""

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

    def strategy(self, opponent):
        """Pretends to play the opponent a number of times before each match.
        The primary purpose is to look far enough ahead to see if a defect will
        be punished by the opponent.

        If the MindReader attempts to play itself (or another similar
        strategy), then it will cause a recursion loop, so this is also handled
        in this method, by defecting if the method is called by strategy
        """

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        calname = calframe[1][3]

        if calname in ('strategy', 'simulate_match'):
            return D

        game = self.match_attributes["game"]

        best_strategy = look_ahead(self, opponent, game)

        return best_strategy


class ProtectedMindReader(MindReader):
    """A player that looks ahead at what the opponent will do and decides what to do.
    It is also protected from mind control strategies"""

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

    def __setattr__(self, name, val):
        """Stops any other strategy altering the methods of this class """

        if name == 'strategy':
            pass
        else:
            self.__dict__[name] = val

class MirrorMindReader(ProtectedMindReader):
    """A player that will mirror whatever strategy it is playing against by cheating
    and calling the opponent's strategy function instead of its own."""

    name = 'Mirror Mind Reader'

    classifier = {
        'memory_depth': -10,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True, # reading and copying the source of the component
        'manipulates_source': True, # changing own source dynamically
        'manipulates_state': False
    }

    def strategy(self, opponent):
        """Will read the mind of the opponent and play the opponent's strategy.

        Also avoid infinite recursion when called by itself or another mind reader
        or bender by cooperating.
        """

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        calname = calframe[1][3]

        if calname in ('strategy', 'simulate_match'):
            return C

        return opponent.strategy(self)
