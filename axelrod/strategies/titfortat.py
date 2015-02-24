from axelrod import Player

class TitForTat(Player):
    """
    A player starts by cooperating and then mimics previous move by opponent.
    """

    name = 'Tit For Tat'

    def strategy(self, opponent):
        """
        Begins by playing 'C':
        This is affected by the history of the opponent: the strategy simply repeats the last action of the opponent
        """
        try:
            return opponent.history[-1]
        except IndexError:
            return 'C'

class TitFor2Tats(Player):
    """
    A player starts by cooperating and then defects only after two defects by opponent.
    """

    name = "Tit For 2 Tats"

    def strategy(self, opponent):
        """
        Begins by playing 'C':
        Will defect whenever anopponent has defected twice
        """
        if opponent.history[-2:] == ['D', 'D']:
            return 'D'
        return 'C'

class TwoTitsForTat(Player):
    """
    A player starts by cooperating and replies to each defect by two defections.
    """

    name = "Two Tits For Tat"

    def strategy(self, opponent):
        """
        Begins by playing 'C':
        Will defect twice after each defection by opponent
        """
        if 'D' in opponent.history[-2:]:
            return 'D'
        return 'C'

class AntiTitForTat(Player):
    """
    Starts by defecting and then does the opposite of opponent's previous move.
    This the opposite of TIT FOR TAT, also sometimes called BULLY.
    """

    name = "Anti Tit For Tat"

    def strategy(self, opponent):
        """Begins with D, then does opposite of what opponent does."""
        return 'C' if opponent.history[-1:] == ['D'] else 'D'
