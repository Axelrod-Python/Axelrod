from axelrod.actions import Action, Actions
from axelrod.player import Player
from axelrod.strategy_transformers import FinalTransformer

C, D = Actions.C, Actions.D


@FinalTransformer((D, D), name_prefix=None)  # End with two defections
class BackStabber(Player):
    """
    Forgives the first 3 defections but on the fourth
    will defect forever. Defects on the last 2 rounds unconditionally.

    Names:

    - Backstabber: Original name by Thomas Campbell
    """

    name = 'BackStabber'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': {'length'},
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        return _backstabber_strategy(opponent)


@FinalTransformer((D, D), name_prefix=None)  # End with two defections
class DoubleCrosser(Player):
    """
    Forgives the first 3 defections but on the fourth
    will defect forever. Defects on the last 2 rounds unconditionally.

    If 8 <= current round <= 180,
    if the opponent did not defect in the first 7 rounds,
    the player will only defect after the opponent has defected twice in-a-row.

    Names:

    - Double Crosser: Original name by Thomas Campbell
    """

    name = 'DoubleCrosser'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': {'length'},
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        if _opponent_triggers_alt_strategy(opponent):
            return _alt_strategy(opponent)
        return _backstabber_strategy(opponent)


def _backstabber_strategy(opponent: Player) -> Action:
    """
    Cooperates until opponent defects a total of four times, then always
    defects.
    """
    if not opponent.history:
        return C
    if opponent.defections > 3:
        return D
    return C


def _alt_strategy(opponent: Player) -> Action:
    """
    If opponent's previous two plays were defect, then defects on next round.
    Otherwise, cooperates.
    """
    previous_two_plays = opponent.history[-2:]
    if previous_two_plays == [D, D]:
        return D
    return C


def _opponent_triggers_alt_strategy(opponent: Player) -> bool:
    """
    If opponent did not defect in first 7 rounds and the current round is from 8
    to 180, return True. Else, return False.
    """
    before_alt_strategy = first_n_rounds = 7
    last_round_of_alt_strategy = 180
    if _opponent_defected_in_first_n_rounds(opponent, first_n_rounds):
        return False
    current_round = len(opponent.history) + 1
    return before_alt_strategy < current_round <= last_round_of_alt_strategy


def _opponent_defected_in_first_n_rounds(opponent: Player, first_n_rounds: int
                                         ) -> bool:
    """
    If opponent defected in the first N rounds, return True. Else return False.
    """
    return D in opponent.history[:first_n_rounds]
