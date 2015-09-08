import copy
import inspect

from axelrod import Player, RoundRobin, Game, update_histories


def simulate_match(player_1, player_2, strategy, rounds = 10):
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

def look_ahead(player_1, player_2, rounds=10):
    """Looks ahead for `rounds` and selects the next strategy appropriately."""
    results = []
    game = Game()

    # Simulate plays for `rounds` rounds
    strategies = ['C', 'D']
    for strategy in strategies:
        #opponent_ = copy.deepcopy(player_2) # need deepcopy here
        opponent_ = player_2
        round_robin = RoundRobin(players=[player_1, opponent_], game=game,
                                 turns=rounds)
        simulate_match(player_1, opponent_, strategy, rounds)
        results.append(round_robin._calculate_scores(player_1, opponent_)[0])

        # Restore histories and counts
        roll_back_history(player_1, rounds)
        roll_back_history(player_2, rounds)

    return strategies[results.index(max(results))]


class MindReader(Player):
    """A player that looks ahead at what the opponent will do and decides what to do."""

    name = 'Mind Reader'

    def __init__(self):
        Player.__init__(self)
        self.behaviour['stochastic'] = True # Don't cache me

    def strategy(self, opponent):
        """Pretends to play the opponent a number of times before each match.
        The primary purpose is to look far enough ahead to see if a defect will
        be punished by the opponent.
        If the MindReader attempts to play itself (or another similar strategy),
        then it will cause a recursion loop, so this is also handeled in this
        method, by defecting if the method is called by strategy
        """

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        calname = calframe[1][3]

        if calname in ('strategy', 'simulate_match'):
            return 'D'

        best_strategy = look_ahead(self, opponent)

        return best_strategy


class ProtectedMindReader(MindReader):
    """A player that looks ahead at what the opponent will do and decides what to do.
    It is also protected from mind control strategies"""

    name = 'Protected Mind Reader'

    def __setattr__(self, name, val):
        """Stops any other strategy altering the methods of this class """

        if name == 'strategy':
            pass
        else:
            self.__dict__[name] = val
