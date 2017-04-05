from itertools import product
from collections import namedtuple
from axelrod.actions import Actions, str_to_actions
from axelrod.player import Player

C, D = Actions.C, Actions.D


ActionKeys = namedtuple('ActionKeys', 'player, opponent, opponent_starts')


def make_keys_into_action_keys(lookup_table: dict) -> dict:
    """Returns a dict where all keys are ActionKeys."""
    new_table = lookup_table.copy()
    if any(not isinstance(key, ActionKeys) for key in new_table):
        new_table = {ActionKeys(*key): value for key, value in new_table.items()}
    return new_table


def create_lookup_table_keys(plays: int, op_plays: int, op_start_plays: int) -> list:
    """Creates the keys for a lookup table."""
    self_histories = product((C, D), repeat=plays)
    other_histories = product((C, D), repeat=op_plays)
    opponent_starts = product((C, D), repeat=op_start_plays)

    iterator = product(self_histories, other_histories, opponent_starts)
    return [ActionKeys(*action_tuples) for action_tuples in iterator]


def create_lookup_table_from_tuple(plays: int, op_plays: int, op_start_plays: int, pattern: tuple) -> dict:
    """Creates a set of keys, and maps a tuple of actions to those keys. Returns that dictionary."""
    lookup_table_keys = create_lookup_table_keys(plays=plays, op_plays=op_plays, op_start_plays=op_start_plays)
    if len(lookup_table_keys) != len(pattern):
        raise ValueError("Table keys and pattern are not of the same size.")
    table = dict(zip(lookup_table_keys, pattern))
    return table


def create_lookup_table_from_string(plays: int, op_plays: int, op_start_plays: int, pattern_string: str) -> dict:
    """Creates a set of keys, and maps a string of actions (such as "DDCDC") to those keys. Returns that dictionary."""
    pattern_to_pass_in = str_to_actions(pattern_string)
    lookup_table = create_lookup_table_from_tuple(plays=plays,
                                                  op_plays=op_plays,
                                                  op_start_plays=op_start_plays,
                                                  pattern=pattern_to_pass_in)
    return lookup_table


class LookerUp(Player):
    """
    A strategy that uses a lookup table to decide what to do based on a
    combination of the last m1 plays, m2 opponent plays, and the opponent's
    opening n actions. If there isn't enough history to do this (i.e. for the
    first m1 or m2 turns) then call, in order, the actions in self.initial_actions
    (defaults to C's) until there is enough history to use the lookup table.

    The lookup table is implemented as a dict. The keys are named tuples, ActionKeys(player, opponent, opponent_start)
    giving self's last m1 actions, opponents last m2 actions, and the opponents first n actions, all as tuples of
    Action(s). The values are the actions to play on this round.

    For example, in the case of m1=m2=n=1, if
    - my last action was a C
    - the opponent's last action was a D
    - the opponent started by playing C
    then the corresponding key would be

        ActionKeys((C,), (D,), (C,))

    and the value would contain the action to play on this turn.

    Some well-known strategies can be expressed as special cases; for example
    Cooperator is given by the dict::

        {((), (), ()) : C}

    where m and n are both zero.

    Tit-For-Tat is given by::

       {((C, ), (D, ), ()): D,
        ((D, ), (D, ), ()): D,
        ((C, ), (C, ), ()): C,
        ((D, ), (C, ), ()): C}

    where m=1 and n=0.

    Lookup tables where the action depends on the opponent's first actions (as
    opposed to most recent actions) will have a non-empty final tuple in the
    ActionKeys. For example, this fragment of a dict::

       {((C, ), (C, ), (C, )): C,
        ((C, ), (C, ), (D, )): D}

    states that if self and opponent both cooperated on the previous turn, we
    should cooperate this turn unless the opponent started by defecting, in
    which case we should defect.

    To denote lookup tables where the action depends on sequences of actions
    (so m or n are greater than 1), simply make the tuple larger.

    Below is an incomplete example where m1=m2=3 and n=2.

       {((C, D, D), (C, C, C), (C, C)): C,
        ((C, C, D), (C, C, C), (C, D)): D}
    """

    name = 'LookerUp'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    default_tft_lookup_table = {((C,), (D,), ()): D,
                                ((D,), (D,), ()): D,
                                ((C,), (C,), ()): C,
                                ((D,), (C,), ()): C}

    def __init__(self, lookup_table: dict = None, initial_actions: tuple = None,
                 lookup_pattern: str = None, parameters: tuple = None) -> None:

        super().__init__()

        self.lookup_table = self._get_lookup_table(lookup_table, lookup_pattern, parameters)

        sample_key = next(iter(self.lookup_table))
        self.plays = len(sample_key.player)
        self.op_plays = len(sample_key.opponent)
        self.op_start_plays = len(sample_key.opponent_starts)

        self._set_memory_depth()

        self.initial_actions = self._get_initial_actions(initial_actions)
        self._initial_actions_pool = list(self.initial_actions)

        self._raise_error_for_bad_lookup_table()

    def _get_lookup_table(self, lookup_table: dict = None,
                          pattern_string: str = None,
                          keys_parameters: tuple = None) -> dict:

        if pattern_string is not None and keys_parameters is not None:
            plays, opponent_plays, opponent_starts = keys_parameters
            lookup_table = create_lookup_table_from_string(plays=plays, op_plays=opponent_plays,
                                                           op_start_plays=opponent_starts,
                                                           pattern_string=pattern_string)
        if not lookup_table:
            lookup_table = self.default_tft_lookup_table

        new_lookup_table = make_keys_into_action_keys(lookup_table)
        return new_lookup_table

    def _set_memory_depth(self):
        if self.op_start_plays == 0:
            self.classifier['memory_depth'] = max(self.plays, self.op_plays)
        else:
            self.classifier['memory_depth'] = float('inf')

    def _get_initial_actions(self, initial_actions):
        """Initial actions will always be cut down to table_depth."""
        table_depth = max(self.plays, self.op_plays, self.op_start_plays)
        if not initial_actions:
            initial_actions = tuple([C] * table_depth)
        return initial_actions[:table_depth]

    def _raise_error_for_bad_lookup_table(self):
        if any(
            len(key.player) != self.plays or
            len(key.opponent) != self.op_plays or
            len(key.opponent_starts) != self.op_start_plays
            for key in self.lookup_table
        ):
            raise ValueError("All table elements must have the same size")

    def strategy(self, opponent):
        while self._initial_actions_pool:
            return self._initial_actions_pool.pop(0)

        player_last_n_plays = self.history[-1 * self.plays:] if self.plays else []
        opponent_last_n_plays = opponent.history[-1 * self.op_plays:] if self.op_plays else []
        opponent_starting_plays = opponent.history[:self.op_start_plays]

        key = ActionKeys(player=tuple(player_last_n_plays),
                         opponent=tuple(opponent_last_n_plays),
                         opponent_starts=tuple(opponent_starting_plays))

        return self.lookup_table[key]

    def reset(self):
        super(LookerUp, self).reset()
        self._initial_actions_pool = list(self.initial_actions)

class EvolvedLookerUp1_1_1(LookerUp):
    """
    A 1 1 1 Lookerup trained with an evolutionary algorithm.

    Names:
        - Evolved Lookerup 1 1 1: Original name by Marc Harper
    """
    name = "EvolvedLookerUp1_1_1"

    def __init__(self) -> None:
        # original = 'CDDDDDCD'
        super().__init__(parameters=(1, 1, 1), lookup_pattern='CDDDDCDD',
                         initial_actions=(C,))


class EvolvedLookerUp2_2_2(LookerUp):
    """
    A 2 2 2 Lookerup trained with an evolutionary algorithm.

    Names:
        - Evolved Lookerup 2 2 2: Original name by Marc Harper
    """
    name = "EvolvedLookerUp2_2_2"

    def __init__(self) -> None:
        # original = 'CDCCDCCCDCDDDCCCDCDDDDDDDCDDDCDCDDDDCCDCCCCDDDDCCDDDDCCDCDDDDDDD'
        pattern = 'CDDCDCDDCDDDCDDDDDCDCDCCCDDCCDCDDDCCCCCDDDCDDDDDDDDDCCDDCDDDCCCD'
        super().__init__(parameters=(2, 2, 2), lookup_pattern=pattern,
                         initial_actions=(C, C))


class Winner12(LookerUp):
    """
    A lookup table based strategy.

    Names:
        - Winner12 [Mathieu2015]_
    """
    name = "Winner12"

    def __init__(self) -> None:
        pattern = 'CDCDDCDD'
        super().__init__(parameters=(1, 2, 0), lookup_pattern=pattern,
                         initial_actions=(C, C))


class Winner21(LookerUp):
    """
    A lookup table based strategy.

    Names:
        - Winner21 [Mathieu2015]_
    """
    name = "Winner21"

    def __init__(self) -> None:
        pattern = 'CDCDCDDD'
        super().__init__(parameters=(1, 2, 0), lookup_pattern=pattern,
                         initial_actions=(D, C))
