import itertools

from axelrod import Player
from .axelrod_tournaments import Joss


class Calculator(Player):
    """
    Plays like (Hard) Joss for the first 20 rounds. If periodic behavior is
    detected, defect forever. Otherwise play TFT.
    """

    name = "Calculator"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        Player.__init__(self)
        self.joss_instance = Joss()

    @staticmethod
    def detect_cycle(history):
        """Detects if there is a cycle in the opponent's history."""
        for i in range(len(history) // 2):
            cycle = itertools.cycle(history[0: i + 1])
            cycle_list = list(itertools.islice(cycle, 0, len(history)))
            if list(history) == cycle_list:
                return True
        return False

    def strategy(self, opponent):
        turn = len(self.history)
        if turn == 20:
            self.cycle = self.detect_cycle(opponent.history)
            return self.extended_strategy(opponent)
        if turn > 20:
            return self.extended_strategy(opponent)
        else:
            play = self.joss_instance.strategy(opponent)
            self.joss_instance.history.append(play)
            return play

    def extended_strategy(self, opponent):
        if self.cycle:
            return 'D'
        else:
            # TFT
            return 'D' if opponent.history[-1:] == ['D'] else 'C'

    def reset(self):
        Player.reset(self)
        self.joss_instance = Joss()
