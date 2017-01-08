from axelrod import Actions, Player
from axelrod.strategy_transformers import InitialTransformer

C, D = Actions.C, Actions.D


@InitialTransformer(D * 5 + C * 2, name_prefix=None)
class GradualKiller(Player):
    """
    It begins by defecting in the first five moves, then cooperates two times.
    It then defects all the time if the opponent has defected in move 6 and 7,
    else cooperates all the time.
    Initially designed to stop Gradual from defeating TitForTat in a 3 Player
    tournament.

    Names

    - Gradual Killer: [PRISON1998]_
    """

    name = 'Gradual Killer'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        if opponent.history[5:7] == D + D:
            return D
        return C
