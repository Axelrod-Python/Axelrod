from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class Cooperator(Player):
    """A player who only ever cooperates.

    Names:

    - Cooperator: [Axelrod1984]_
    - ALLC: [Press2012]_
    - Always cooperate: [Mittal2009]_
    """

    name = 'Cooperator'
    classifier = {
        'memory_depth': 0,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        return C


class TrickyCooperator(Player):
    """
    A cooperator that is trying to be tricky.

    Names:

    - Tricky Cooperator: Original name by Karol Langner
    """

    name = "Tricky Cooperator"
    classifier = {
        'memory_depth': 10,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    _min_history_required_to_try_trickiness = 3
    _max_history_depth_for_trickiness = -10

    def strategy(self, opponent: Player) -> Action:
        """Almost always cooperates, but will try to trick the opponent by
        defecting.

        Defect once in a while in order to get a better payout.
        After 3 rounds, if opponent has not defected to a max history depth of
        10, defect.
        """
        if (self._has_played_enough_rounds_to_be_tricky() and
                self._opponents_has_cooperated_enough_to_be_tricky(opponent)):
            return D
        return C

    def _has_played_enough_rounds_to_be_tricky(self):
        return len(self.history) >= self._min_history_required_to_try_trickiness

    def _opponents_has_cooperated_enough_to_be_tricky(self, opponent):
        rounds_to_be_checked = opponent.history[
                               self._max_history_depth_for_trickiness:]
        return D not in rounds_to_be_checked
