from axelrod.action import Action, actions_to_str
from axelrod.player import Player
from axelrod.strategy_transformers import (
    FinalTransformer,
    TrackHistoryTransformer,
)

C, D = Action.C, Action.D


class FrequencyAnalyzer(Player):
    """
    A player starts by playing TitForTat for the first 30 turns (dataset generation phase).

    Take the matrix of last 2 moves by both Player and Opponent.

    While in dataset generation phase, construct a dictionary d, where keys are each 4 move sequence
    and the corresponding value for each key is a list of the subsequent Opponent move. The 4 move sequence
    starts with the Opponent move.

    For example, if a game at turn 5 looks like this:

    Opp:    C, C, D, C, D
    Player: C, C, C, D, C

    d should look like this:

    { [CCCC]: [D],
      [CCDC]: [C],
      [DCCD]: [D] }

    During dataset generation phase, Player will play TitForTat. After end of dataset generation phase,
    Player will switch strategies. Upon encountering a particular 4-move sequence in the game, Player will look up history
    of subsequent Opponent move. If ratio of defections to total moves exceeds p, Player will defect. Otherwise,
    Player will cooperate.

    Could fall under "Hunter" class of strategies.
    More likely falls under LookerUp class of strategies.

    Names:

    - FrequencyAnalyzer (FREQ): Original by Ian Miller
    """

    # These are various properties for the strategy
    name = "FrequencyAnalyzer"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        """
        Parameters
        ----------
        p, float
            The probability to cooperate
        """
        super().__init__()
        self.minimum_cooperation_ratio = 0.25
        self.frequency_table = dict()
        self.last_sequence = ""
        self.current_sequence = ""

    def strategy(self, opponent: Player) -> Action:
        """This is the actual strategy"""
        if len(self.history) > 5:
            self.last_sequence = (
                str(opponent.history[-3])
                + str(self.history[-3])
                + str(opponent.history[-2])
                + str(self.history[-2])
            )
            self.current_sequence = (
                str(opponent.history[-2])
                + str(self.history[-2])
                + str(opponent.history[-1])
                + str(self.history[-1])
            )
            self.update_table(opponent)

        # dataset generation phase
        if (len(self.history) < 30) or (
            self.current_sequence not in self.frequency_table
        ):
            if not self.history:
                return C
            if opponent.history[-1] == D:
                return D
            return C

        # post-dataset generation phase
        results = self.frequency_table[self.current_sequence]
        cooperates = results.count(C)
        if (cooperates / len(self.history)) > self.minimum_cooperation_ratio:
            return C
        return D

    def update_table(self, opponent: Player):
        if self.last_sequence in self.frequency_table.keys():
            results = self.frequency_table[self.last_sequence]
            results.append(opponent.history[-1])
            self.frequency_table[self.last_sequence] = results
        else:
            self.frequency_table[self.last_sequence] = [opponent.history[-1]]
