from axelrod import Player

class GoByRecentMajority10(Player):
    """
    A player examines the history of the opponent: if the opponent has more defections than cooperations in the past 10 turns then the player defects
    """
    def strategy(self, opponent):
        """
        This is affected by the history of the opponent:
        As long as the opponent cooperates at least as often as they defect in the past 10 turns then the player will cooperate.
        If at any point the opponent has more defections than cooperations the player defects.
        """
        recent10 = opponent.history[-10:]
        if sum([s == 'D' for s in recent10]) > sum([s == 'C' for s in recent10]):
            return 'D'
        return 'C'

    def __repr__(self):
        """
        The string method for the strategy.
        """
        return 'Go By Recent Majority 10'
