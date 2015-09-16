from axelrod import Player


class Prober(Player):
    """
    Plays D, C, C initially. Defects forever if opponent cooperated in moves 2
    and 3. Otherwise plays TFT.
    """

    name = 'Prober'
    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),  # Long memory
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        turn = len(self.history)
        if turn == 0:
            return 'D'
        if turn == 1:
            return 'C'
        if turn == 2:
            return 'C'
        if turn > 2:
            if opponent.history[1: 3] == ['C', 'C']:
                return 'D'
            else:
                # TFT
                return 'D' if opponent.history[-1:] == ['D'] else 'C'


class Prober2(Player):
    """
    Plays D, C, C initially. Cooperates forever if opponent played D then C
    in moves 2 and 3. Otherwise plays TFT.
    """

    name = 'Prober 2'
    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),  # Long memory
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        turn = len(self.history)
        if turn == 0:
            return 'D'
        if turn == 1:
            return 'C'
        if turn == 2:
            return 'C'
        if turn > 2:
            if opponent.history[1: 3] == ['D', 'C']:
                return 'C'
            else:
                # TFT
                return 'D' if opponent.history[-1:] == ['D'] else 'C'


class Prober3(Player):
    """
    Plays D, C initially. Defects forever if opponent played C in moves 2.
    Otherwise plays TFT.
    """

    name = 'Prober 3'
    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),  # Long memory
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        turn = len(self.history)
        if turn == 0:
            return 'D'
        if turn == 1:
            return 'C'
        if turn > 1:
            if opponent.history[1] == 'C':
                return 'D'
            else:
                # TFT
                return 'D' if opponent.history[-1:] == ['D'] else 'C'


class HardProber(Player):
    """
    Plays D, D, C, C initially. Defects forever if opponent cooperated in moves
    2 and 3. Otherwise plays TFT.
    """

    name = 'Hard Prober'
    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),  # Long memory
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        turn = len(self.history)
        if turn == 0:
            return 'D'
        if turn == 1:
            return 'D'
        if turn == 2:
            return 'C'
        if turn == 3:
            return 'C'
        if turn > 3:
            if opponent.history[1: 3] == ['C', 'C']:
                return 'D'
            else:
                # TFT
                return 'D' if opponent.history[-1:] == ['D'] else 'C'
