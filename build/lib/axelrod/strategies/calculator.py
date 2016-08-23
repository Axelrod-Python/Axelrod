from axelrod import Actions, Player
from .axelrod_first import Joss
from axelrod._strategy_utils import detect_cycle


class Calculator(Player):
    """
    Plays like (Hard) Joss for the first 20 rounds. If periodic behavior is
    detected, defect forever. Otherwise play TFT.
    """

    name = "Calculator"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        Player.__init__(self)
        self.joss_instance = Joss()

    def strategy(self, opponent):
        turn = len(self.history)
        if turn == 20:
            self.cycle = detect_cycle(opponent.history)
            return self.extended_strategy(opponent)
        if turn > 20:
            return self.extended_strategy(opponent)
        else:
            play = self.joss_instance.strategy(opponent)
            self.joss_instance.history.append(play)
            return play

    def extended_strategy(self, opponent):
        if self.cycle:
            return Actions.D
        else:
            # TFT
            return Actions.D if opponent.history[-1:] == [Actions.D] else Actions.C

    def reset(self):
        Player.reset(self)
        self.joss_instance = Joss()
