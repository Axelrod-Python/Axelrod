from axelrod import Player


class Appeaser(Player):
    """A player who tries to guess what the opponent wants.

    Switch the behaviour every time the opponent plays 'D'.
    Start with 'C', switch between 'C' and 'D' when opponent plays 'D'.
    """

    name = 'Appeaser'
    memory_depth = float('inf')  # Depends on internal memory.

    def strategy(self, opponent):
        if not len(self.history):
            self.move = 'C'
        else:
            if opponent.history[-1] == 'D':
                if self.move == 'C':
                    self.move = 'D'
                else:
                    self.move = 'C'
        return self.move
