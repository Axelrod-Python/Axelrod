import random
from typing import List, Dict, Any
from axelrod.action import Action
from axelrod.player import Player


class SchwobaSenGnitz(Player):
    """Schwoba sen gnitz."""

    name: str = "schwoba sen gnitz"
    authors: List[str] = ["Georg 'HackyHackberger' Schmidt"]
    classifier: Dict[str, Any] = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_state": False,
        "manipulates_history": False,
        "uses_length": False,
        "uses_game": False,
        "uses_tournament": False,
        "uses_clones": False,
    }

    def __init__(self) -> None:
        super().__init__()
        self.raubtier_erwacht = False
        self.schutz_modus_aktiviert = False

    def strategy(self, opponent: Player) -> Action:
        runde = len(self.history)
        if runde == 0:
            return Action.C

        if not opponent.history:
            return Action.C

        if not self.raubtier_erwacht and opponent.history[-1] == Action.D:
            self.raubtier_erwacht = True

        if not self.raubtier_erwacht:
            return Action.C

        if runde >= 10 and len(opponent.history) >= 10:
            letzte_10_gegner = opponent.history[-10:]
            if all(zug == Action.D for zug in letzte_10_gegner):
                self.schutz_modus_aktiviert = True

        if self.schutz_modus_aktiviert:
            return Action.D

        if opponent.history[-1] == Action.D:
            if random.random() < 0.897:
                return Action.C
            else:
                return Action.D

        if random.random() < 0.102:
            return Action.D

        return Action.C
