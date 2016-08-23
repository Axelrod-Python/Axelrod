from axelrod import Actions, Player


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

    def strategy(self, opponent):
        if len(self.history) == 0:
            return Actions.C
        if self.history[-1] == Actions.C:
            return Actions.D
        return Actions.C
