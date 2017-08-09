from axelrod.action import Action, actions_to_str
from axelrod.player import Player
from axelrod.random_ import randrange
from axelrod._strategy_utils import calculate_scores

from enum import Enum

C, D = Action.C, Action.D
        
class MoreGraaskamp(Player):
    """
    This strategy can be described as follows:
    
    1. Play tit for tat for the first 50 rounds.
    2. Defect on round 51.
    3. Play 5 further rounds of tit for tat.
    4. In round 57, select between four different "modes" for the rest of the game:
        defect_randomly - If none of the below modes is selected, cooperate and
            defect randomly every 5 to 15 turns
        tit_for_tat - If the opponent's score is greater than 135 and moves 52
            through 55 were [C, D, C, D] or [D, D, D, D], play tit for tat
            thereafter starting with cooperate
        always_defect - If the opponent's score is less than or equal to 135,
            always defect hereafter
        cooperate_then_tit_for_tat - If the opponent's score is greater than 135
            and moves 52 through 56 were [C, C, D, C, C], cooperate until and
            including move 118, and tit for tat thereafter

    Names:

    - GRASR: [Axelrod1993]_
    - Graaskamp: [Axelrod1980b]_
    """

    # These are various properties of the strategy
    name = 'MoreGraaskamp'
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
        self.mode = 'unknown'
        self.defect_round = 0

    def reset(self):
        super().reset()
        self.mode = 'unknown'
        self.defect_round = 0

    # The strategy itself
    def strategy(self, opponent: Player) -> Action:
        round_number = len(self.history) + 1

        # Tit for tat for first 50 rounds
        if round_number == 1:
            return C
        if round_number < 51:
            return opponent.history[-1]
        # Defect on round 51
        if round_number == 51:
            return D
        # Play 5 further rounds of tit for tat
        if round_number < 57:
            return opponent.history[-1]
        if round_number == 57:
            game = self.match_attributes['game']

            self_score, opponent_score = calculate_scores(self, opponent, game)

            if opponent_score <= 135:
                self.mode = 'always_defect'
                return D
            else:
                # Opponent's moves 52 through 56
                last_five_opponent_actions = opponent.history[-5:]
                # Opponent's moves 52 through 55
                prev_four_opponent_actions = opponent.history[-5:-1]

                if last_five_opponent_actions == [C, C, D, C, C]:
                    self.mode = 'cooperate_then_tit_for_tat'
                elif prev_four_opponent_actions == [C, D, C, D] or prev_four_opponent_actions == [D, D, D, D]:
                    self.mode = 'tit_for_tat'
                else:
                    self.mode = 'defect_randomly'
                    self.defect_round = round_number + randrange(5, 15) + 1

                return C

        # Beyond round 57, obey the rules of the mode entered during round 57
        if self.mode == 'tit_for_tat':
            return opponent.history[-1]
        if self.mode == 'always_defect':
            return D
        if self.mode == 'cooperate_then_tit_for_tat':
            if round_number == 118:
                self.mode = 'tit_for_tat'

            return C

        # self.mode must be 'defect_randomly'
        if round_number == self.defect_round:
            self.defect_round = round_number + randrange(5, 15) + 1
            return D

        return C
