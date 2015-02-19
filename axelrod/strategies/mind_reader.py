from axelrod import Player
import copy

class MindReader(Player):
    """
    A player that looks ahead at what the opponent will do and decides what to do
    """
    def strategy(self, opponent):
        """
        """
        
        best_strategy = self.look_ahead(opponent)

        if best_strategy == 0:
            return self.strategy_coop(opponent)
        if best_strategy == 1:
            return self.strategy_defect(opponent)

    def look_ahead(self, opponent, rounds = 50):
        """
        Plays a number of rounds to determine the best strategy 
        """
        results = []

        dummy_history_self = copy.copy(self.history)
        dummy_history_opponent = copy.copy(opponent.history)

        for match in range(rounds):
            play_1 = self.strategy_coop(opponent)
            play_2 = opponent.strategy(self)
            self.history.append(play_1)
            opponent.history.append(play_2)

        results.append(self.calculate_score(self.history, opponent.history))

        self.history = copy.copy(dummy_history_self)
        opponent.history = copy.copy(dummy_history_opponent)

        for match in range(rounds):
            play_1 = self.strategy_defect(opponent)
            play_2 = opponent.strategy(self)
            self.history.append(play_1)
            opponent.history.append(play_2)


        results.append(self.calculate_score(self.history, opponent.history))

        self.history = copy.copy(dummy_history_self)
        opponent.history = copy.copy(dummy_history_opponent)

        return results.index(min(results))

    def calculate_score(self, history_1, history_2):
        
        s1 = 0
        for pair in zip(history_1, history_2):
            if pair[0] == pair[1] == 'C':
                s1 += 2
            if pair[0] == pair[1] == 'D':
                s1 += 4
            if pair[0] == 'C' and  pair[1] == 'D':
                s1 += 5
            if pair[0] == 'D' and  pair[1] == 'C':
                s1 += 0

        return s1

    def __repr__(self):
        """
        The string method for the strategy.
        """
        return 'Mind Reader'

    def strategy_coop(self, opponent):
        """
        Always Cooperate
        """

        return 'C'

    def strategy_defect(self, opponent):
        """
        Always defect
        """

        return 'D'
