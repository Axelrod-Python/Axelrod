from axelrod import Actions, Player, Game

C, D = Actions.C, Actions.D


class Handshake(Player):
    """Starts with C, D. If the opponent plays the same way, cooperate forever,
    else defect forever."""

    name = 'Handshake'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        Player.__init__(self)
        self.initial_plays = [C, D]

    def strategy(self, opponent):
        # Begin by playing the sequence C, D
        index = len(self.history)
        if index < len(self.initial_plays):
            return self.initial_plays[index]
        # If our opponent played [C, D] on the first two moves, cooperate
        # forever. Otherwise defect.
        if opponent.history[0:2] == self.initial_plays:
            return C
        return D


class Fortress3(Player):
    """Starts with D, D, C. If the opponent plays the same way, cooperate until
    the opponent defects. Otherwise defect until the opponent cooperates on
    two consecutive plays. Ref: 10.1109/CEC.2006.1688322. Note that the
    description in http://www.graham-kendall.com/papers/lhk2011.pdf is
    incorrect."""

    name = 'Fortress3'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        Player.__init__(self)
        self.initial_plays = [D, D, C]

    def strategy(self, opponent):
        # Begin by playing the sequence C, D
        index = len(self.history)
        if index < len(self.initial_plays):
            return self.initial_plays[index]
        # If our opponent played [C, D] on the first two moves, cooperate
        # forever. Otherwise defect.
        if opponent.history[0:3] == self.initial_plays:
            return C
        return D
