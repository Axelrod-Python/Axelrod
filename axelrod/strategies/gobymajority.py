from axelrod import Player


class GoByMajority(Player):
    """A player examines the history of the opponent: if the opponent has more defections than cooperations then the player defects.

    An optinal memory attribute will limit the number of turns remembered
    """

    memory = 0

    def strategy(self, opponent):
        """This is affected by the history of the opponent.

        As long as the opponent cooperates at least as often as they defect then the player will cooperate.
        If at any point the opponent has more defections than cooperations in memory the player defects.
        """
        history = opponent.history[-self.memory:]
        if sum([s == 'D' for s in history]) > sum([s == 'C' for s in history]):
            return 'D'
        return 'C'

    def __repr__(self):
        """The string method for the strategy."""
        return 'Go By Majority' + (self.memory > 0) * ("/%i" % self.memory)


class GoByMajority40(GoByMajority):
    memory = 40

class GoByMajority20(GoByMajority):
    memory = 20

class GoByMajority10(GoByMajority):
    memory = 10

class GoByMajority5(GoByMajority):
    memory = 5

