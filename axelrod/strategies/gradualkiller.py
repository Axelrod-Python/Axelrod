from axelrod import Actions, Player, init_args
C, D = Actions.C, Actions.D


class GradualKiller(Player):
    """
    It begins by defecting in the first five moves, then cooperates two times.
    It then defects all the time if the opponent has defected in move 6 and 7,
    else cooperates all the time.

    Names

    - Gradual Killer: [PRISON1998]_
    """

    # These are various properties for the strategy
    name = 'Gradual Killer'
    classifier = {
        'memory_depth': float('Inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        """This is the actual strategy"""
        # First seven moves
        firstseven = [D, D, D, D, D, C, C]
        if len(self.history) < 7:
            return firstseven[len(self.history)]
        # React to the opponent's 6th and 7th moves
        elif opponent.history[5:7] == [D, D]:
            return D
        return C