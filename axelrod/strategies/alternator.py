from axelrod import Player


class Alternator(Player):
    """A player who alternates between cooperating and defecting."""

    name = 'Alternator'
    behaviour = {
        'memory_depth': 1,
        'stochastic': False,
        'inspects_opponent_source': False,
        'manipulates_opponent_source': False,
        'manipulates_opponent_state': False
    }

    def strategy(self, opponent):
        if len(self.history) == 0:
            return 'C'
        if self.history[-1] == 'C':
            return 'D'
        return 'C'
