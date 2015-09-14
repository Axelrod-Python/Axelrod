from axelrod import Player


class Cooperator(Player):
    """A player who only ever cooperates."""

    name = 'Cooperator'
    classifier = {
        'memory_depth': 0,
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return 'C'


class TrickyCooperator(Player):
    """A cooperator that is trying to be tricky."""

    name = "Tricky Cooperator"
    classifier = {
        'memory_depth': 10,
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        """Almost always cooperates, but will try to trick the opponent by defecting.

        Defect once in a while in order to get a better payout, when the opponent
        has not defected in the last ten turns and only cooperated during last 3 turns.
        """
        if 'D' not in opponent.history[-10:] and opponent.history[-3:] == ['C']*3:
            return 'D'
        return 'C'
