from axelrod import Player, RoundRobin, Game, update_histories
import copy
import inspect

class MindReader(Player):
    """A player that looks ahead at what the opponent will do and decides what to do."""

    name = 'Mind Reader'
    max_look_ahead = 200

    def strategy(self, opponent):
        """Pretends to play the opponent 50 times before each match.
        The primary purpose is to look far enough ahead to see if a defect will be punished by the opponent.
        If the MindReader attempts to play itself (or another similar strategy), then it will cause a recursion loop, so this is also handeled in this method, by defecting if the method is called by strategy
        """

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        calname = calframe[1][3]

        if calname in ('strategy', 'simulate_match'):
            return 'D'

        # Clone myself to preserve histories
        clone = copy.deepcopy(self)
        best_strategy = clone.look_ahead(opponent)

        return best_strategy

    def simulate_match(self, opponent, strategy, rounds = 10):
        """Simulates a number of matches."""
        for match in range(rounds):
            play_1, play_2 = strategy, opponent.strategy(self)
            # Update histories and counts
            update_histories(self, opponent, play_1, play_2)

    def look_ahead(self, opponent, rounds = 10):
        """Plays a number of rounds to determine the best strategy."""
        results = []
        game = Game()
        round_robin = RoundRobin(players=[self, opponent], game=game, turns=rounds)
        strategies = ['C', 'D']

        # Record internal variables 
        dummy_history_self = copy.copy(self.history)
        cooperations = self.cooperations
        defections = self.defections

        for strategy in strategies:
            opponent_ = copy.deepcopy(opponent)
            self.simulate_match(opponent_, strategy, rounds)
            results.append(round_robin._calculate_scores(self, opponent_)[0])

            # Restore histories and counts
            self.history = copy.copy(dummy_history_self)
            self.cooperations = cooperations
            self.defections = defections

        return strategies[results.index(max(results))]

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
