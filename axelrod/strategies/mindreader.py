import copy
import inspect

from axelrod import Actions, Player, RoundRobin, update_history
from .cycler import Cycler

C, D = Actions.C, Actions.D

def limited_simulate_play(player_1, player_2, h1):
    """Here we want to replay player_1's history to player_2, allowing
    player_2's strategy method to set any internal variables as needed. If you
    need a more complete simulation, see `simulate_play` in player.py. This
    function is specifically designed for the needs of MindReader."""
    h2 = player_2.strategy(player_1)
    update_history(player_1, h1)
    update_history(player_2, h2)

def simulate_match(player_1, player_2, strategy, rounds=10):
    """Simulates a number of matches."""
    for match in range(rounds):
        limited_simulate_play(player_1, player_2, strategy)

def look_ahead(player_1, player_2, game, rounds=10):
    """Looks ahead for `rounds` and selects the next strategy appropriately."""
    results = []

    # Simulate plays for `rounds` rounds
    strategies = [C, D]
    for strategy in strategies:
        # Instead of a deepcopy, create a new opponent and play out the history
        opponent_ = player_2.clone()
        player_ = Cycler(strategy) # Either cooperator or defector
        for h1 in player_1.history:
            limited_simulate_play(player_, opponent_, h1)

        round_robin = RoundRobin(players=[player_, opponent_], game=game,
                                 turns=rounds)
        simulate_match(player_, opponent_, strategy, rounds)
        results.append(round_robin._calculate_scores(player_, opponent_)[0])

    return strategies[results.index(max(results))]


class MindReader(Player):
    """A player that looks ahead at what the opponent will do and decides what to do."""

    name = 'Mind Reader'
    classifier = {
        'memory_depth': -10,
        'stochastic': False,
        'makes_use_of': set(),
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

        game = self.tournament_attributes["game"]

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
