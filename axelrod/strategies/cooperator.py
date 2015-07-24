from axelrod import Player


class Cooperator(Player):
    """A player who only ever cooperates."""

    name = 'Cooperator'
    memory_depth = 0  # Memory-one Four-Vector = (1,1,1,1)

    @staticmethod
    def strategy(opponent):
        return 'C'


class TrickyCooperator(Player):
    """A cooperator that is trying to be tricky."""

    name = "Tricky Cooperator"
    memory_depth = 10  # Long memory

    @staticmethod
    def strategy(opponent):
        """Almost always cooperates, but will try to trick the opponent by defecting.

        Defect once in a while in order to get a better payout, when the opponent
        has not defected in the last ten turns and only cooperated during last 3 turns.
        """
        if 'D' not in opponent.history[-10:] and opponent.history[-3:] == ['C']*3:
            return 'D'
        return 'C'


class Aggravater(Player):
    """The worst possible strategy?
    Defects twice at the beginning, followed by endless cooperation."""

    name = 'Aggravater'
    memory_depth = 0

    @staticmethod
    def strategy(opponent):
        if len(opponent.history) < 2:
            return 'D'
        return 'C'
