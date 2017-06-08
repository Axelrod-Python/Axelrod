from axelrod.actions import Actions, Action
from axelrod.player import Player
from .titfortat import TitForTat, TitFor2Tats
from .defector import Defector

C, D = Actions.C, Actions.D


class MEM2(Player):
    """A memory-two player that switches between TFT, TFTT, and ALLD.

    Note that the reference claims that this is a memory two strategy but in
    fact it is infinite memory. This is because the player plays as ALLD if
    ALLD has ever been selected twice, which can only be known if the entire
    history of play is accessible.

    Names:

    - MEM2: [Li2014]_
    """

    name = 'MEM2'
    classifier = {
        'memory_depth': float('inf'),
        'long_run_time': False,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        self.players = {
            "TFT" : TitForTat(),
            "TFTT": TitFor2Tats(),
            "ALLD": Defector()
        }
        self.play_as = "TFT"
        self.shift_counter = 3
        self.alld_counter = 0

    def strategy(self, opponent: Player) -> Action:
        # Update Histories
        # Note that this assumes that TFT and TFTT do not use internal counters,
        # Rather that they examine the actual history of play
        if len(self.history) > 0:
            for v in self.players.values():
                v.history.append(self.history[-1])
        self.shift_counter -= 1
        if (self.shift_counter == 0) and (self.alld_counter < 2):
            self.shift_counter = 2
            # Depending on the last two moves, play as TFT, TFTT, or ALLD
            last_two = list(zip(self.history[-2:], opponent.history[-2:]))
            if set(last_two) == set([(C, C)]):
                self.play_as = "TFT"
            elif set(last_two) == set([(C, D), (D, C)]):
                self.play_as = "TFTT"
            else:
                self.play_as = "ALLD"
                self.alld_counter += 1
        return self.players[self.play_as].strategy(opponent)

    def reset(self):
        super().reset()
        for v in self.players.values():
            v.reset()
        self.play_as = "TFT"
        self.shift_counter = 3
        self.alld_counter = 0
