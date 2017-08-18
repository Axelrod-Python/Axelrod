from axelrod.action import Action
from axelrod.player import Player
from .axelrod_first import Joss
from axelrod._strategy_utils import detect_cycle

C, D = Action.C, Action.D


class Calculator(Player):
    """
    Plays like (Hard) Joss for the first 20 rounds. If periodic behavior is
    detected, defect forever. Otherwise play TFT.


    Names:

    - Calculator: [Prison1998]_
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

    def __init__(self) -> None:
        super().__init__()
        self.joss_instance = Joss()

    def strategy(self, opponent: Player) -> Action:
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

    def extended_strategy(self, opponent: Player) -> Action:
        if self.cycle:
            return D
        else:
            # TFT
            return D if opponent.history[-1:] == [D] else C
