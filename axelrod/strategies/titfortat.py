from axelrod import Player

class TitForTat(Player):
    """
    A player starts by cooperating and then mimics previous move by opponent.
    """
    def strategy(self, opponent):
        """
        Begins by playing 'C':
        This is affected by the history of the opponent: the strategy simply repeats the last action of the opponent
        """
        try:
            return opponent.history[-1]
        except IndexError:
            return 'C'

    def __repr__(self):
        """
        The string method for the strategy.
        """
        return 'Tit For Tat'

class TitFor2Tats(Player):
    """
    A player starts by cooperating and then defects only after two defects by opponent.
    """
    def strategy(self, opponent):
        """
        Being by playing 'C':
        Will defect whenever anopponent has defected twice
        """
        if opponent.history[-2:] == ['D', 'D']:
            return 'D'
        return 'C'

    def __repr__(self):
        """The string method for the strategy."""
        return "Tit For 2 Tats"

class TwoTitsForTat(Player):
    """
    A player starts by cooperating and replies to each defect by two defections.
    """
    def strategy(self, opponent):
        """
        Being by playing 'C':
        Will defect twice after each defection by opponent
        """
        if 'D' in opponent.history[-2:]:
            return 'D'
        return 'C'

    def __repr__(self):
        """The string method for the strategy."""
        return "Two Tits For Tat"
