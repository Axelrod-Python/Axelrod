from axelrod import Player
import random

class Average_Copier(Player):
    """
    The player will cooperate with probability p if the opponent's cooperation ratio is p
    """
    def strategy(self, opponent):
        """
        Randomly picks a strategy (not affected by history)
        """
        if len(opponent.history) == 0:
            return random.choice(['C', 'D'])
        p = sum([s == 'C' for s in opponent.history]) / len(opponent.history)
        rnd_num = random.random()
        if rnd_num < p:
            return 'C'
        return 'D'

    def __repr__(self):
        """
        The string method for the strategy:
        """
        return 'Average_Copier'
