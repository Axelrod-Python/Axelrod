from axelrod import Player

class GoByMajority(Player):
    """
    A player examines the history of the opponent: if the opponent has more defections than cooperations then the player defects
    """
    def strategy(self, opponent):
        """
        This is affected by the history of the opponent:
        As long as the opponent cooperates at least as often as they defect then the player will defect.
        If at any point the opponent has more defections than cooperations the player defects.
        """
        if sum([s == 'D' for s in opponent.history]) > sum([s == 'C' for s in opponent.history]):
            return 'D'
        return 'C'

    def __repr__(self):
        """
        The string method for the strategy.
        """
        return 'Go By Majority'
