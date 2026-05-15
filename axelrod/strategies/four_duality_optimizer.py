from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D

class FourDualityOptimizer1(Player):
    """
    A strategy that operates as follows:
    cooperate by default;
    ignore betrayals of length 1;
    when the other agent performs a series of betrayals of length greater than 1,
    respond with a series of betrayals whose number is equal to the number
    of series of betrayals performed by the other agent since the beginning.

    Names:
    4-Duality Optimizer 1 original by Paul Franceschi
    """
    name = "4-Duality Optimizer 1"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        # Calculate the number of opponent betrayal streaks of length > 1
        waves_greater_than_one = 0
        current_wave_length = 0
        for action in opponent.history:
            if action == axl.Action.D:
                current_wave_length += 1
            else:
                if current_wave_length > 1:
                    waves_greater_than_one += 1
                current_wave_length = 0

        # Calculate the length of our current betrayal streak
        consecutive_our_defections = 0
        for i in range(len(self.history) - 1, -1, -1):
            if self.history[i] == axl.Action.D:
                consecutive_our_defections += 1
            else:
                break

        # Calculate the length of the opponent's current betrayal streak
        consecutive_opp_defections = 0
        for i in range(len(opponent.history) - 1, -1, -1):
            if opponent.history[i] == axl.Action.D:
                consecutive_opp_defections += 1
            else:
                break

        # Decision rules
        if consecutive_opp_defections >= 2:
            return D

        if consecutive_our_defections > 0 and consecutive_our_defections < waves_greater_than_one:
            return D

        return C
