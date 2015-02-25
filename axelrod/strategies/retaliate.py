from axelrod import Player


class Retaliate(Player):
    """
    A player starts by cooperating but will retaliate once the opponent
    has won more than 10 percent times the number of defections the player has.
    """
    name = "Retaliate"

    def strategy(self, opponent):
        history = zip(self.history, opponent.history)
        if history.count(('C', 'D')) > history.count(('D', 'C')) * 0.1:
            return 'D'

        return 'C'
