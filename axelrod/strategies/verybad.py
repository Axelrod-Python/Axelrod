from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class VeryBad(Player):
    """
    It cooperates in the first three rounds, and uses probability
    (it implements a memory, which stores the opponent’s moves) to decide for
    cooperating or defecting.
    Due to a lack of information as to what that probability refers to in this
    context, probability(P(X)) refers to (Count(X)/Total_Moves) in this
    implementation
    P(C) = Cooperations / Total_Moves
    P(D) = Defections / Total_Moves = 1 - P(C)

    Names:

    - VeryBad: [Andre2013]_
    """

    name = 'VeryBad'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        total_moves = len(opponent.history)

        if total_moves < 3:
            return C

        cooperations = opponent.cooperations

        cooperation_probability = cooperations / total_moves

        if cooperation_probability > 0.5:
            return C

        elif cooperation_probability < 0.5:
            return D

        else:
            return opponent.history[-1]
