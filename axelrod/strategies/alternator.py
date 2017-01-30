from axelrod import Actions, Player
import axelrod

C, D = Actions.C, Actions.D


class Alternator(Player):
    """A player who alternates between cooperating and defecting."""

    name = 'Alternator'
    classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: axelrod.player.Player) -> axelrod.actions.Action:
        if len(self.history) == 0:
            return C
        if self.history[-1] == C:
            return D
        return C
