from axelrod import Actions, Player

C, D = Actions.C, Actions.D

class Appeaser(Player):
    """A player who tries to guess what the opponent wants.

    Switch the classifier every time the opponent plays 'D'.
    Start with 'C', switch between 'C' and 'D' when opponent plays 'D'.
    """

    name = 'Appeaser'
    classifier = {
        'memory_depth': float('inf'),  # Depends on internal memory.
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        if not len(opponent.history):
            self.move = C
        else:
            if opponent.history[-1] == D:
                if self.move == C:
                    self.move = D
                else:
                    self.move = C
        return self.move
