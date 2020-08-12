from axelrod._strategy_utils import detect_cycle
from axelrod.action import Action
from axelrod.player import Player

from .axelrod_first import FirstByJoss as Joss

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
        "memory_depth": float("inf"),
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        self.joss_instance = Joss()
        super().__init__()

    def set_seed(self, seed: int = None):
        super().set_seed(seed)
        self.joss_instance.set_seed(seed)

    def strategy(self, opponent: Player) -> Action:
        turn = len(self.history)
        if turn > 0:
            self.joss_instance.history.append(self.history[-1],
                                              opponent.history[-1])
        if turn == 20:
            self.cycle = detect_cycle(opponent.history)
            return self.extended_strategy(opponent)
        if turn > 20:
            return self.extended_strategy(opponent)
        else:
            play = self.joss_instance.strategy(opponent)
            return play

    def extended_strategy(self, opponent: Player) -> Action:
        if self.cycle:
            return D
        else:
            # TFT
            return D if opponent.history[-1:] == [D] else C
