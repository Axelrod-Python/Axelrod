from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D

class AdaptiveCooperator(Player):
    """
    This is an adaptive strategy where the player starts
    by cooperating, but switches to Tit-For-Tat if the
    opponent's score exceed's its own score. Then, it
    switches to Defector if the opponent's score is twice
    its own score.
    """

    name = 'Adaptive Cooperator'
    classifier = {
        'memory': 1,
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        super().__init__()
        self.is_tft = False
        self.is_defect = False
        self.current_score = 0
        self.opponent_score = 0

    def _score_last_round(self, opponent):
        game = self.match_attributes["game"]
        last_round = (self.history[-1], opponent.history[-1])
        scores = game.score(last_round)
        self.current_score += scores[0]
        self.opponent_score += scores[1]

    def strategy(self, opponent):
        turn = len(self.history) + 1
        if turn > 1:
            self._score_last_round(opponent)

        if self.opponent_score > self.current_score * 2:
            self.is_defect = True
        elif self.opponent_score > self.current_score:
            self.is_tft = True

        #response to strategies
        if self.is_defect:
            return D
        elif self.is_tft:
            if not opponent.history or len(self.history) == 0:
                return C
            else:
                return opponent.history[-1]
        else: #cooperate
            return C

    def reset(self):
        super().__init__()
        self.is_defect = False
        self.is_tft = False

