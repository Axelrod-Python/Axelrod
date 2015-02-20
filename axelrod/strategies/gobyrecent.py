from axelrod import Player


class GoByRecentMajority(Player):
    """
    A player examines the history of the opponent: if the opponent recently has more defections than cooperations, then the player defects
    """

    length = 1

    def strategy(self, opponent):
        """
        This is affected by the history of the opponent:
        As long as the opponent cooperates at least as often as they defect in recent, turns then the player will cooperate.
        If the opponent has more defections than cooperations recently, the player defects.
        """
        recent = opponent.history[-self.length:]
        if sum([s == 'D' for s in recent]) > sum([s == 'C' for s in recent]):
            return 'D'
        return 'C'

    def __repr__(self):
        """
        The string method for the strategy.
        """
        return 'Go By Majority/%i' % self.length


class GoByRecentMajority40(GoByRecentMajority):
    length = 40

class GoByRecentMajority20(GoByRecentMajority):
    length = 20

class GoByRecentMajority10(GoByRecentMajority):
    length = 10

class GoByRecentMajority5(GoByRecentMajority):
    length = 5