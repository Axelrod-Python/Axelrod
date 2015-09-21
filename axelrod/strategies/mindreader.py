import copy
import inspect

from axelrod import Player, RoundRobin, update_histories


def simulate_match(player_1, player_2, strategy, rounds=10):
    """Simulates a number of matches."""
    for match in range(rounds):
        play_1, play_2 = strategy, player_2.strategy(player_1)
        # Update histories and counts
        update_histories(player_1, player_2, play_1, play_2)

def roll_back_history(player, rounds):
    """Undo the last `rounds` rounds as sufficiently as possible."""
    for i in range(rounds):
        play = player.history.pop(-1)
        if play == 'C':
            player.cooperations -= 1
        elif play == 'D':
            player.defections -= 1

def look_ahead(player_1, player_2, game, rounds=10):
    """Looks ahead for `rounds` and selects the next strategy appropriately."""
    results = []

    # Simulate plays for `rounds` rounds
    strategies = ['C', 'D']
    for strategy in strategies:
        opponent_ = copy.deepcopy(player_2) # need deepcopy here
        round_robin = RoundRobin(players=[player_1, opponent_], game=game,
                                 turns=rounds)
        simulate_match(player_1, opponent_, strategy, rounds)
        results.append(round_robin._calculate_scores(player_1, opponent_)[0])

        # Restore histories and counts
        roll_back_history(player_1, rounds)

    return strategies[results.index(max(results))]


class MindReader(Player):
    """A player that looks ahead at what the opponent will do and decides what to do."""

    name = 'Mind Reader'
    classifier = {
        'memory_depth': -10,
        'stochastic': False,
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
            return 'D'

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
            return 'C'

        return opponent.strategy(self)
