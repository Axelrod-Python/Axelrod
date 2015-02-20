from axelrod import Player, Axelrod
import copy

class MindReader(Player):
    """
    A player that looks ahead at what the opponent will do and decides what to do
    """
    def strategy(self, opponent):
        """
        Simulates the next 50 rounds and decides whether to cooperate or defect
        """
        
        best_strategy = self.look_ahead(opponent)

        return ['C','D'][best_strategy]


    def look_ahead(self, opponent, rounds = 50):
        """
        Plays a number of rounds to determine the best strategy 
        """
        results = []
        tournement = Axelrod()

        dummy_history_self = copy.copy(self.history)
        dummy_history_opponent = copy.copy(opponent.history)

        for match in range(rounds):
            play_1 = self.strategy_coop(opponent)
            play_2 = opponent.strategy(self)
            self.history.append(play_1)
            opponent.history.append(play_2)

        results.append(tournement.calculate_scores(self, opponent)[0])

        self.history = copy.copy(dummy_history_self)
        opponent.history = copy.copy(dummy_history_opponent)

        for match in range(rounds):
            play_1 = self.strategy_defect(opponent)
            play_2 = opponent.strategy(self)
            self.history.append(play_1)
            opponent.history.append(play_2)


        results.append(tournement.calculate_scores(self, opponent)[0])

        self.history = copy.copy(dummy_history_self)
        opponent.history = copy.copy(dummy_history_opponent)

        return results.index(min(results))

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
