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


class LimitedRetaliate(Player):
    """
    A player that co-operates unless the opponent defects and wins.
    It will then retaliate by defecting. It stops when either, it has beaten
    the opponent 10 times more often that it has lost or it reaches the
    retaliation limit (20 defections).
    """
    name = 'Limited Retaliate'
    retaliation_limit = 20
    retaliating = False
    retaliation_count = 0

    def strategy(self, opponent):
        history = zip(self.history, opponent.history)
        if history.count(('C', 'D')) > history.count(('D', 'C')) * 0.1:
            self.retaliating = True
        else:
            self.retaliating = False
            self.retaliation_count = 0

        if self.retaliating:
            if self.retaliation_count < self.retaliation_limit:
                self.retaliation_count += 1
                return 'D'
            else:
                self.retaliation_count = 0
                self.retaliating = False

        return 'C'

    def reset(self):
        super(LimitedRetaliate, self).reset()
        self.retaliating = False
        self.retaliation_count = 0
