from axelrod.action import Action
from axelrod.player import Player

from typing import Optional

C, D = Action.C, Action.D


class APavlov2006(Player):
    """
    APavlov attempts to classify its opponent as one of five strategies:
    Cooperative, ALLD, STFT, PavlovD, or Random. APavlov then responds in a
    manner intended to achieve mutual cooperation or to defect against
    uncooperative opponents.

    Names:

    - Adaptive Pavlov 2006: [Li2007]_
    """

    name = "Adaptive Pavlov 2006"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        self.opponent_class = None  # type: Optional[str]

    def strategy(self, opponent: Player) -> Action:
        # TFT for six rounds
        if len(self.history) < 6:
            return D if opponent.history[-1:] == [D] else C
        # Classify opponent
        if len(self.history) % 6 == 0:
            if opponent.history[-6:] == [C] * 6:
                self.opponent_class = "Cooperative"
            if opponent.history[-6:] == [D] * 6:
                self.opponent_class = "ALLD"
            if opponent.history[-6:] == [D, C, D, C, D, C]:
                self.opponent_class = "STFT"
            if opponent.history[-6:] == [D, D, C, D, D, C]:
                self.opponent_class = "PavlovD"
            if not self.opponent_class:
                self.opponent_class = "Random"

        # Play according to classification
        if self.opponent_class in ["Random", "ALLD"]:
            return D
        if self.opponent_class == "STFT":
            if len(self.history) % 6 in [0, 1]:
                return C
            # TFT
            if opponent.history[-1:] == [D]:
                return D
        if self.opponent_class == "PavlovD":
            # Return D then C for the period
            if len(self.history) % 6 == 0:
                return D
        if self.opponent_class == "Cooperative":
            # TFT
            if opponent.history[-1:] == [D]:
                return D
        return C


class APavlov2011(Player):
    """
    APavlov attempts to classify its opponent as one of four strategies:
    Cooperative, ALLD, STFT, or Random. APavlov then responds in a manner
    intended to achieve mutual cooperation or to defect against
    uncooperative opponents.

    Names:

    - Adaptive Pavlov 2011: [Li2011]_
    """

    name = "Adaptive Pavlov 2011"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        self.opponent_class = None  # type: Optional[str]

    def strategy(self, opponent: Player) -> Action:
        # TFT for six rounds
        if len(self.history) < 6:
            return D if opponent.history[-1:] == [D] else C
        if len(self.history) % 6 == 0:
            # Classify opponent
            if opponent.history[-6:] == [C] * 6:
                self.opponent_class = "Cooperative"
            if opponent.history[-6:].count(D) >= 4:
                self.opponent_class = "ALLD"
            if opponent.history[-6:].count(D) == 3:
                self.opponent_class = "STFT"
            if not self.opponent_class:
                self.opponent_class = "Random"
        # Play according to classification
        if self.opponent_class in ["Random", "ALLD"]:
            return D
        if self.opponent_class == "STFT":
            # TFTT
            return D if opponent.history[-2:] == [D, D] else C
        if self.opponent_class == "Cooperative":
            # TFT
            return D if opponent.history[-1:] == [D] else C
