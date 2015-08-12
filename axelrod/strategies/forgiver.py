from axelrod import Player


class Forgiver(Player):
    """
    A player starts by cooperating however will defect if at any point
    the opponent has defected more than 10 percent of the time
    """

    name = 'Forgiver'
    memory_depth = float('inf')  # Long memory

    @staticmethod
    def strategy(opponent):
        """
        Begins by playing C, then plays D if the opponent has defected more than 10 percent of the time
        """
        if opponent.defections > len(opponent.history) / 10.:
            return 'D'
        return 'C'


class ForgivingTitForTat(Player):
    """
    A player starts by cooperating however will defect if at any point,
    the opponent has defected more than 10 percent of the time,
    and their most recent decision was defect.
    """

    name = 'Forgiving Tit For Tat'
    memory_depth = float('inf')  # Long memory

    @staticmethod
    def strategy(opponent):
        """
        Begins by playing C, then plays D if,
        the opponent has defected more than 10 percent of the time,
        and their most recent decision was defect.
        """
        if opponent.defections > len(opponent.history) / 10.:
            return opponent.history[-1]
        return 'C'
