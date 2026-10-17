import random
from axelrod.action import Action
from axelrod.player import Player

class SchwobaSenGnitz(Player):
    """
    Schwoba sen gnitz (Schwaben sind gerissen) - Python-Version 2026.
    Autor: Georg 'HackyHackberger' Schmidt (1985 / 2026)
    Ursprünglicher Code in Turbo Pascal, 1985
    Startet 100 % friedlich. Nach dem ersten gegnerischen Verrat erwacht die 
    optimierte gnitze Technik: 10,2 % Sondierung, 89,7 % Deeskalation.
    Erkennt nach 10 Runden unversöhnliche Gegner und riegelt ab.
    """

    name = "Schwoba sen gnitz"
    authors = ["Georg 'HackyHackberger' Schmidt"]
    classifier = {
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

        if not self.raubtier_erwacht and opponent.history[-1] == Action.D:
            self.raubtier_erwacht = True

        if not self.raubtier_erwacht:
            return Action.C

        if runde >= 10:
            letzte_10_gegner = opponent.history[-10:]
            if all(zug == Action.D for zug in letzte_10_gegner):
                self.schutz_modus_aktiviert = True

        if self.schutz_modus_aktiviert:
            return Action.D

        if opponent.history[-1] == Action.D:
            # 89,7 % Deeskalations-Bremse gegen KIs
            if random.random() < 0.897:
                return Action.C
            else:
                return Action.D

        # 10,2 % gnitze Sondierung
        if random.random() < 0.102:
            return Action.D

        return Action.C
