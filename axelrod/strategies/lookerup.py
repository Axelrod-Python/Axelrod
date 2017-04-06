from itertools import product
from collections import namedtuple
from axelrod.actions import Actions, str_to_actions
from axelrod.player import Player

C, D = Actions.C, Actions.D


ActionKeys = namedtuple('ActionKeys', 'self_plays, op_plays, op_initial_plays')


class LookerUp(Player):
    """
    This strategy uses a lookup table to decide its next action. If there is not enough
    history to use the table, it calls form a list of self.initial_actions.

    The keys to the lookup table (a dictionary) are ActionKeys(self_plays, op_plays, op_initial_plays).
    self_plays is a tuple of the player's last m1 plays.  op_plays is a tuple of the last m2 opponent plays.
    op_initial_plays is a tuple of the first N opponent plays.  The lookup table must contain keys
    for every possible combination.  Here is a sample lookup table with

    - self_plays: depth=2
    - op_plays: depth=1
    - op_initial_plays: depth=0::

        {ActionsKeys((C, C), (C), ()): C,
         ActionsKeys((C, C), (D), ()): D,
         ActionsKeys((C, D), (C), ()): D,  <- example below
         ActionsKeys((C, D), (D), ()): D,
         ActionsKeys((D, C), (C), ()): C,
         ActionsKeys((D, C), (D), ()): D,
         ActionsKeys((D, D), (C), ()): C,
         ActionsKeys((D, D), (D), ()): D}


    From the above table, if the player last played C, D and the opponent last played C (here the
    initial opponent play is ignored) then this round, the player would play D.

    Some well-known strategies can be expressed as special cases; for example
    Cooperator is given by the dict::

        {ActionKeys((), (), ()) : C}

    All history is ignored and always play C.

    Tit-For-Tat is given by::

       {ActionKeys((), (D,), ()): D,
        ActionKeys((), (C,), ()): C}

    The only history that is important is the opponent's last play.

    The table defaults to Tit-For-Tat.  The initial actions defaults to playing C.

    You can init the table either by specifying lookup_table=  or
    by specifying lookup_pattern= and parameters=.

    lookup_table can use tuples as keys and it will be converted to ActionKeys.

    parameters is a tuple of ints (self_plays depth, opponent_plays depth, opponent_initial_plays depth).
    lookup_pattern is a string like 'CCDCDDCD'.
    it will create a keys for a lookup_table of size 2 ** (sp_depth + op_depth + oip_depth) and map
    the actions, in order, to the keys.

    initial_actions is a tuple such as (C, C, D). A table needs initial actions equal to
    max(self_plays depth, opponent_plays depth, opponent_initial_plays depth). If provided initial_actions
    is too long, the extra will be ignored.  If provided initial_actions is too short, the shortfall will
    be made up with C's.
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

    default_tft_lookup_table = {ActionKeys(self_plays=(), op_plays=(D,), op_initial_plays=()): D,
                                ActionKeys(self_plays=(), op_plays=(C,), op_initial_plays=()): C}

    def __init__(self, lookup_table: dict = None, initial_actions: tuple = None,
                 lookup_pattern: str = None, parameters: tuple = None) -> None:

        super().__init__()

        self.lookup_table = self._get_lookup_table(lookup_table, lookup_pattern, parameters)

        sample_key = next(iter(self.lookup_table))
        self.player_history_depth = len(sample_key.self_plays)
        self.op_history_depth = len(sample_key.op_plays)
        self.op_initial_plays = len(sample_key.op_initial_plays)

        self._set_memory_depth()

        self.initial_actions = self._get_initial_actions(initial_actions)
        self._initial_actions_pool = list(self.initial_actions)

        self._raise_error_for_bad_lookup_table()

    def _get_lookup_table(self, lookup_table: dict = None,
                          pattern_string: str = None,
                          keys_parameters: tuple = None) -> dict:
        if lookup_table:
            return make_keys_into_action_keys(lookup_table)

        if pattern_string and keys_parameters:
            plays, opponent_plays, op_initial_plays = keys_parameters
            return create_lookup_table_from_string(plays=plays, op_plays=opponent_plays,
                                                   op_initial_plays=op_initial_plays,
                                                   pattern_string=pattern_string)

        return self.default_tft_lookup_table.copy()

    def _set_memory_depth(self):
        if self.op_initial_plays == 0:
            self.classifier['memory_depth'] = max(self.player_history_depth, self.op_history_depth)
        else:
            self.classifier['memory_depth'] = float('inf')

    def _get_initial_actions(self, initial_actions):
        """Initial actions will always be cut down to table_depth."""
        table_depth = max(self.player_history_depth, self.op_history_depth, self.op_initial_plays)
        if not initial_actions:
            initial_actions = tuple([C] * table_depth)
        initial_actions_too_short = table_depth - len(initial_actions)
        if initial_actions_too_short > 0:
            initial_actions += tuple([C] * initial_actions_too_short)
        return initial_actions[:table_depth]

    def _raise_error_for_bad_lookup_table(self):
        if any(
            len(key.self_plays) != self.player_history_depth or
            len(key.op_plays) != self.op_history_depth or
            len(key.op_initial_plays) != self.op_initial_plays
            for key in self.lookup_table
        ):
            raise ValueError("Lookup table keys are not all the same size.")
        total_key_combinations = 2 ** (self.player_history_depth + self.op_history_depth + self.op_initial_plays)
        if total_key_combinations != len(self.lookup_table):
            raise ValueError("Lookup table does not have enough keys to cover all possibilities.")

    def strategy(self, opponent):
        while self._initial_actions_pool:
            return self._initial_actions_pool.pop(0)

        player_last_n_plays = get_last_n_plays(player=self, depth=self.player_history_depth)
        opponent_last_n_plays = get_last_n_plays(player=opponent, depth=self.op_history_depth)
        opponent_initial_plays = tuple(opponent.history[:self.op_initial_plays])

        key = ActionKeys(self_plays=player_last_n_plays,
                         op_plays=opponent_last_n_plays,
                         op_initial_plays=opponent_initial_plays)

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


def make_keys_into_action_keys(lookup_table: dict) -> dict:
    """Returns a dict where all keys are ActionKeys."""
    new_table = lookup_table.copy()
    if any(not isinstance(key, ActionKeys) for key in new_table):
        new_table = {ActionKeys(*key): value for key, value in new_table.items()}
    return new_table


def create_lookup_table_from_string(plays: int, op_plays: int, op_initial_plays: int, pattern_string: str) -> dict:
    """Creates a set of keys, and maps a string of actions (such as "DDCDC") to those keys. Returns that dictionary."""
    pattern_to_pass_in = str_to_actions(pattern_string)
    lookup_table = create_lookup_table_from_tuple(plays=plays,
                                                  op_plays=op_plays,
                                                  op_initial_plays=op_initial_plays,
                                                  pattern=pattern_to_pass_in)
    return lookup_table


def create_lookup_table_from_tuple(plays: int, op_plays: int, op_initial_plays: int, pattern: tuple) -> dict:
    """Creates a set of keys, and maps a tuple of actions to those keys. Returns that dictionary."""
    lookup_table_keys = create_lookup_table_keys(plays=plays, op_plays=op_plays, op_initial_plays=op_initial_plays)
    if len(lookup_table_keys) != len(pattern):
        raise ValueError("Table keys and pattern are not of the same size.")
    table = dict(zip(lookup_table_keys, pattern))
    return table


def create_lookup_table_keys(plays: int, op_plays: int, op_initial_plays: int) -> list:
    """Creates the keys for a lookup table."""
    self_histories = product((C, D), repeat=plays)
    other_histories = product((C, D), repeat=op_plays)
    op_initial_history = product((C, D), repeat=op_initial_plays)

    iterator = product(self_histories, other_histories, op_initial_history)
    return [ActionKeys(*action_tuples) for action_tuples in iterator]


def get_last_n_plays(player: Player, depth: int) -> tuple:
    """Returns the last N plays of player as a tuple."""
    if depth == 0:
        return ()
    return tuple(player.history[-1 * depth:])
