from axelrod import Player


class Alternator(Player):
    """A player who alternates between cooperating and defecting."""

    name = 'Alternator'
    memory_depth = 1

    def strategy(self, opponent):
        if len(self.history) == 0:
            return 'C'
        if self.history[-1] == 'C':
            return 'D'
        return 'C'
