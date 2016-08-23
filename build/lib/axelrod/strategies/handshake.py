from axelrod import Actions, Player, init_args

C, D = Actions.C, Actions.D


class Handshake(Player):
    """Starts with C, D. If the opponent plays the same way, cooperate forever,
    else defect forever."""

    name = 'Handshake'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self, initial_plays=None):
        Player.__init__(self)
        if not initial_plays:
            initial_plays = [C, D]
        self.initial_plays = initial_plays

    def strategy(self, opponent):
        # Begin by playing the sequence C, D
        index = len(self.history)
        if index < len(self.initial_plays):
            return self.initial_plays[index]
        # If our opponent played [C, D] on the first two moves, cooperate
        # forever. Otherwise defect forever.
        if opponent.history[0: len(self.initial_plays)] == self.initial_plays:
            return C
        return D
