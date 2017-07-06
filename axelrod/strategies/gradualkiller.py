from axelrod.action import Action
from axelrod.player import Player
from axelrod.strategy_transformers import InitialTransformer

C, D = Action.C, Action.D


@InitialTransformer((D, D, D, D, D, C, C), name_prefix=None)
class GradualKiller(Player):
    """
    It begins by defecting in the first five moves, then cooperates two times.
    It then defects all the time if the opponent has defected in move 6 and 7,
    else cooperates all the time.
    Initially designed to stop Gradual from defeating TitForTat in a 3 Player
    tournament.

    Names

    - Gradual Killer: [Prison1998]_
    """

    # These are various properties for the strategy
    name = 'Gradual Killer'
    classifier = {
        'memory_depth': float('Inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        if opponent.history[5:7] == [D, D]:
            return D
        return C
