from axelrod.actions import Actions
from axelrod.player import Player
from axelrod.strategy_transformers import FinalTransformer
from axelrod.actions import Action

C, D = Actions.C, Actions.D


@FinalTransformer((D, D), name_prefix=None)  # End with two defections
class BackStabber(Player):
    """
    Forgives the first 3 defections but on the fourth
    will defect forever. Defects on the last 2 rounds unconditionally.
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

    From rounds 7 through 179,
    if the opponent did not defect in the first 6 rounds,
    the player will only defect after the opponent has defected twice in-a-row.
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
    Cooperates until opponent defects a total of four times, then always defects.
    """
    if not opponent.history:
        return C
    if opponent.defections > 3:
        return D
    return C


def _alt_strategy(opponent: Player) -> Action:
    """
    If opponent's last two plays were defect, then defects on next round. Otherwise, cooperates.
    """
    final_two_plays = opponent.history[-2:]
    if final_two_plays == [D, D]:
        return D
    return C


def _opponent_triggers_alt_strategy(opponent: Player) -> bool:
    """
    If opponent did not defect in first 6 rounds and the round is from 7 to 179, return True. Else, return False.
    """
    before_alt_strategy = 6
    after_alt_strategy = 180
    if _opponent_defected_in_first_n_rounds(opponent, before_alt_strategy):
        return False
    rounds_opponent_played = len(opponent.history)
    return before_alt_strategy < rounds_opponent_played < after_alt_strategy


def _opponent_defected_in_first_n_rounds(opponent: Player, first_n_rounds: int) -> bool:
    """
    If opponent defected in the first N rounds, return True. Else return False.
    """
    return D in opponent.history[:first_n_rounds]
