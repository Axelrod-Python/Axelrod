from axelrod.action import Action, actions_to_str
from axelrod.player import Player
from axelrod.random_ import randrange
from axelrod._strategy_utils import calculate_scores

from enum import Enum

C, D = Action.C, Action.D

class Mode(Enum):
    """
    Enumerated type for the four "modes" for MoreGraaskamp after round 56:
        1. Tit for tat starting with cooperate, defect randomly every 5 - 15 turns
        2. Tit for tat for rest of the game starting with cooperate
        3. Defect for the rest of the game
        4. Cooperate until move 118 and then transition to tit for tat
    """
    Unknown = 0
    DefectRandomly = 1
    TitForTat = 2
    AlwaysDefect = 3
    CooperateThenTitForTat = 4
        
class MoreGraaskamp(Player):
    """
    This strategy can be described as follows:

    1. Play tit for tat for the first 50 rounds.
    2. Defect on round 51.
    3. Play 5 further rounds of tit for tat.
    4. In round 57, select between four different "modes" for the rest of the game:
        1 - If none of the below modes are selected, cooperate and defect randomly
            every 5 to 15 turns
        2 - If the opponent's score is greater than 135 and moves 52 through 55 were
            [C, D, C, D] or [D, D, D, D], play tit for tat thereafter starting with
            cooperate
        3 - If the opponent's score is less than or equal to 135, always defect hereafter
        4 - If the opponent's score is greater than 135 and moves 52 through 56 were
            [C, C, D, C, C], cooperate until and including move 118, and tit for tat
            thereafter

    Names:

    - GRASR: [Axelrod1993]_
    """

    # These are various properties for the
    name = 'MoreGraaskamp'
    classifier = {
        'memory_depth': 5,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        self.mode = Mode.Unknown
        self.defect_round = 0

    # The strategy itself
    def strategy(self, opponent: Player) -> Action:
        round_number = len(self.history) + 1

        # Tit for tat for first 50 rounds
        if round_number == 1:
            return C
        elif round_number < 51:
            return opponent.history[-1]
        # Defect on round 51
        elif round_number == 51:
            return D
        # Play 5 further rounds of tit for tat
        elif round_number < 57:
            return opponent.history[-1]
        elif round_number == 57:
            game = self.match_attributes['game']

            self_score, opponent_score = calculate_scores(self, opponent, game)

            if opponent_score <= 135:
                self.mode = Mode.AlwaysDefect
                return D
            else:
                # Opponent's moves 52 through 56
                last_five_opponent_actions = opponent.history[-5:]
                # Opponent's moves 52 through 55
                prev_four_opponent_actions = opponent.history[-5:-1]

                if last_five_opponent_actions == [C, C, D, C, C]:
                    self.mode = Mode.CooperateThenTitForTat
                elif prev_four_opponent_actions == [C, D, C, D] or prev_four_opponent_actions == [D, D, D, D]:
                    self.mode = Mode.TitForTat
                else:
                    self.mode = Mode.DefectRandomly
                    self.defect_round = round_number + randrange(5, 15) + 1

                return C

        # Beyond round 57, obey the rules of the mode entered during round 57
        else:
            if self.mode == Mode.TitForTat:
                return opponent.history[-1]
            elif self.mode == Mode.AlwaysDefect:
                return D
            elif self.mode == Mode.CooperateThenTitForTat:
                if round_number == 118:
                    self.mode = Mode.TitForTat

                return C
            else:
                # self.mode must be Mode.DefectRandomly
                if round_number == self.defect_round:
                    self.defect_round = round_number + randrange(5, 15) + 1
                    return D
                else:
                    return C
            
