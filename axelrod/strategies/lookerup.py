from collections import namedtuple
from itertools import product

from axelrod.actions import Action, Actions, str_to_actions
from axelrod.player import Player

from typing import Any, TypeVar

C, D = Actions.C, Actions.D


Plays = namedtuple('Plays', 'self_plays, op_plays, op_openings')


class LookupTable(object):
    """
    LookerUp and its children use this object to determine their next actions.

    It is an object that creates a table of all possible plays to a specified
    depth and the action to be returned for each combination of plays.
    The "get" method returns the appropriate response.
    For the table containing::

        ....
        Plays(self_plays=(C, C), op_plays=(C, D), op_openings=(D, C): D
        Plays(self_plays=(C, C), op_plays=(C, D), op_openings=(D, D): C
        ...

    with:
    player.history[-2:]=[C, C] and
    opponent.history[-2:]=[C, D] and
    opponent.history[:2]=[D, D],
    calling LookupTable.get(plays=(C, C), op_plays=(C, D), op_openings=(D, D))
    will return C.

    Instantiate the table with a lookup_dict. This is
    {(self_plays_tuple, op_plays_tuple, op_openings_tuple): action, ...}.
    It must contain every possible
    permutation with C's and D's of the above tuple.  so::

        good_dict = {((C,), (C,), ()): C,
                     ((C,), (D,), ()): C,
                     ((D,), (C,), ()): D,
                     ((D,), (D,), ()): C}

        bad_dict = {((C,), (C,), ()): C,
                    ((C,), (D,), ()): C,
                    ((D,), (C,), ()): D}

    LookupTable.from_pattern() creates an ordered list of keys for you and maps
    the pattern to the keys.::

        LookupTable.from_pattern(pattern=(C, D, D, C),
            player_depth=0, op_depth=1, op_openings_depth=1
        )

    creates the dictionary::

        {Plays(self_plays=(), op_plays=(C), op_openings=(C)): C,
         Plays(self_plays=(), op_plays=(C), op_openings=(D)): D,
         Plays(self_plays=(), op_plays=(D), op_openings=(C)): D,
         Plays(self_plays=(), op_plays=(D), op_openings=(D)): C,}

    and then returns a LookupTable with that dictionary.
    """
    def __init__(self, lookup_dict: dict) -> None:
        self._dict = make_keys_into_plays(lookup_dict)

        sample_key = next(iter(self._dict))
        self._plays_depth = len(sample_key.self_plays)
        self._op_plays_depth = len(sample_key.op_plays)
        self._op_openings_depth = len(sample_key.op_openings)
        self._table_depth = max(self._plays_depth,
                                self._op_plays_depth,
                                self._op_openings_depth)
        self._raise_error_for_bad_lookup_dict()

    def _raise_error_for_bad_lookup_dict(self):
        if any(
            len(key.self_plays) != self._plays_depth or
            len(key.op_plays) != self._op_plays_depth or
            len(key.op_openings) != self._op_openings_depth
            for key in self._dict
        ):
            raise ValueError("Lookup table keys are not all the same size.")
        total_key_combinations = 2 ** (self._plays_depth +
                                       self._op_plays_depth +
                                       self._op_openings_depth)
        if total_key_combinations != len(self._dict):
            msg = ("Lookup table does not have enough keys" +
                   " to cover all possibilities.")
            raise ValueError(msg)

    @classmethod
    def from_pattern(cls, pattern: tuple, player_depth: int, op_depth: int,
                     op_openings_depth: int):
        keys = create_lookup_table_keys(player_depth=player_depth,
                                        op_depth=op_depth,
                                        op_openings_depth=op_openings_depth)
        if len(keys) != len(pattern):
            msg = "Pattern must be len: {}, but was len: {}".format(
                len(keys), len(pattern)
            )
            raise ValueError(msg)
        input_dict = dict(zip(keys, pattern))
        return cls(input_dict)

    def get(self, plays: tuple, op_plays: tuple, op_openings: tuple) -> Any:
        return self._dict[Plays(self_plays=plays,
                                op_plays=op_plays,
                                op_openings=op_openings)]

    @property
    def player_depth(self) -> int:
        return self._plays_depth

    @property
    def op_depth(self) -> int:
        return self._op_plays_depth

    @property
    def op_openings_depth(self) -> int:
        return self._op_openings_depth

    @property
    def table_depth(self) -> int:
        return self._table_depth

    @property
    def dictionary(self) -> dict:
        return self._dict.copy()

    def display(self,
                sort_by: tuple = ('op_openings', 'self_plays', 'op_plays')
                ) -> str:
        """
        Returns a string for printing lookup_table info in specified order.

        :param sort_by: only_elements='self_plays', 'op_plays', 'op_openings'
        """
        def sorter(plays):
            return tuple(getattr(plays, field) for field in sort_by)

        col_width = 11
        sorted_keys = sorted(self._dict, key=sorter)
        header_line = ('{str_list[0]:^{width}}|' +
                       '{str_list[1]:^{width}}|' +
                       '{str_list[2]:^{width}}')
        display_line = header_line.replace('|', ',') + ': {str_list[3]},'

        line_elements = [(', '.join(getattr(key, sort_by[0])),
                          ', '.join(getattr(key, sort_by[1])),
                          ', '.join(getattr(key, sort_by[2])),
                          self._dict[key])
                         for key in sorted_keys]
        header = header_line.format(str_list=sort_by, width=col_width) + '\n'
        lines = [display_line.format(str_list=line, width=col_width)
                 for line in line_elements]
        return header + '\n'.join(lines) + '\n'

    def __eq__(self, other) -> bool:
        if not isinstance(other, LookupTable):
            return False
        return self._dict == other.dictionary


def make_keys_into_plays(lookup_table: dict) -> dict:
    """Returns a dict where all keys are Plays."""
    new_table = lookup_table.copy()
    if any(not isinstance(key, Plays) for key in new_table):
        new_table = {Plays(*key): value for key, value in new_table.items()}
    return new_table


def create_lookup_table_keys(player_depth: int,
                             op_depth: int,
                             op_openings_depth: int) -> list:
    """Returns a list of Plays that has all possible permutations of C's and
    D's for each specified depth. the list is in order,
    C < D sorted by ((player_tuple), (op_tuple), (op_openings_tuple)).
    create_lookup_keys(2, 1, 0) returns::

        [Plays(self_plays=(C, C), op_plays=(C,), op_openings=()),
         Plays(self_plays=(C, C), op_plays=(D,), op_openings=()),
         Plays(self_plays=(C, D), op_plays=(C,), op_openings=()),
         Plays(self_plays=(C, D), op_plays=(D,), op_openings=()),
         Plays(self_plays=(D, C), op_plays=(C,), op_openings=()),
         Plays(self_plays=(D, C), op_plays=(D,), op_openings=()),
         Plays(self_plays=(D, D), op_plays=(C,), op_openings=()),
         Plays(self_plays=(D, D), op_plays=(D,), op_openings=())]

    """
    self_plays = product((C, D), repeat=player_depth)
    op_plays = product((C, D), repeat=op_depth)
    op_openings = product((C, D), repeat=op_openings_depth)

    iterator = product(self_plays, op_plays, op_openings)
    return [Plays(*plays_tuple) for plays_tuple in iterator]


Reaction = TypeVar('Reaction', Action, float)


class LookerUp(Player):
    """
    This strategy uses a LookupTable to decide its next action. If there is not
    enough history to use the table, it calls from a list of
    self.initial_actions.

    if self_depth=2, op_depth=3, op_openings_depth=5, LookerUp finds the last 2
    plays of self, the last 3 plays of opponent and the opening 5 plays of
    opponent. It then looks those up on the LookupTable and returns the
    appropriate action. If 5 rounds have not been played (the minimum required
    for op_openings_depth), it calls from self.initial_actions.

    LookerUp can be instantiated with a dictionary. The dictionary uses
    tuple(tuple, tuple, tuple) or Plays as keys. for example.

    - self_plays: depth=2
    - op_plays: depth=1
    - op_openings: depth=0::

        {Plays((C, C), (C), ()): C,
         Plays((C, C), (D), ()): D,
         Plays((C, D), (C), ()): D,  <- example below
         Plays((C, D), (D), ()): D,
         Plays((D, C), (C), ()): C,
         Plays((D, C), (D), ()): D,
         Plays((D, D), (C), ()): C,
         Plays((D, D), (D), ()): D}

    From the above table, if the player last played C, D and the opponent last
    played C (here the initial opponent play is ignored) then this round,
    the player would play D.

    The dictionary must contain all possible permutations of C's and D's.

    LookerUp can also be instantiated with `pattern=str/tuple` of actions, and::

        parameters=Plays(
            self_plays=player_depth: int,
            op_plays=op_depth: int,
            op_openings=op_openings_depth: int)

    It will create keys of len=2 ** (sum(parameters)) and map the pattern to
    the keys.

    initial_actions is a tuple such as (C, C, D). A table needs initial actions
    equal to max(self_plays depth, opponent_plays depth, opponent_initial_plays
    depth). If provided initial_actions is too long, the extra will be ignored.
    If provided initial_actions is too short, the shortfall will be made up
    with C's.

    Some well-known strategies can be expressed as special cases; for example
    Cooperator is given by the dict (All history is ignored and always play C)::

        {Plays((), (), ()) : C}


    Tit-For-Tat is given by (The only history that is important is the
    opponent's last play.)::

       {Plays((), (D,), ()): D,
        Plays((), (C,), ()): C}


    LookerUp's LookupTable defaults to Tit-For-Tat.  The initial_actions
    defaults to playing C.

    Names:

    - Lookerup: Original name by Martin Jones
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

    default_tft_lookup_table = {
        Plays(self_plays=(), op_plays=(D,), op_openings=()): D,
        Plays(self_plays=(), op_plays=(C,), op_openings=()): C
    }

    def __init__(self, lookup_dict: dict = None,
                 initial_actions: tuple = None,
                 pattern: Any = None,  # pattern is str or tuple of Action's.
                 parameters: Plays = None) -> None:

        super().__init__()
        self._lookup = self._get_lookup_table(lookup_dict, pattern, parameters)

        self._set_memory_depth()

        self.initial_actions = self._get_initial_actions(initial_actions)
        self._initial_actions_pool = list(self.initial_actions)

    def _get_lookup_table(self, lookup_dict: dict,
                          pattern: Any,
                          parameters: tuple) -> LookupTable:
        if lookup_dict:
            return LookupTable(lookup_dict=lookup_dict)
        if pattern and parameters:
            if isinstance(pattern, str):
                pattern = str_to_actions(pattern)
            self_depth, op_depth, op_openings_depth = parameters
            return LookupTable.from_pattern(pattern, self_depth, op_depth,
                                            op_openings_depth)
        return LookupTable(self.default_tft_lookup_table)

    def _set_memory_depth(self):
        if self._lookup.op_openings_depth == 0:
            self.classifier['memory_depth'] = self._lookup.table_depth
        else:
            self.classifier['memory_depth'] = float('inf')

    def _get_initial_actions(self, initial_actions: tuple) -> tuple:
        """Initial actions will always be cut down to table_depth."""
        table_depth = self._lookup.table_depth
        if not initial_actions:
            return tuple([C] * table_depth)
        initial_actions_shortfall = table_depth - len(initial_actions)
        if initial_actions_shortfall > 0:
            return initial_actions + tuple([C] * initial_actions_shortfall)
        return initial_actions[:table_depth]

    def strategy(self, opponent: Player) -> Reaction:
        while self._initial_actions_pool:
            return self._initial_actions_pool.pop(0)

        player_last_n_plays = get_last_n_plays(player=self,
                                               depth=self._lookup.player_depth)
        opponent_last_n_plays = get_last_n_plays(player=opponent,
                                                 depth=self._lookup.op_depth)
        opponent_initial_plays = tuple(
            opponent.history[:self._lookup.op_openings_depth]
        )

        return self._lookup.get(player_last_n_plays,
                                opponent_last_n_plays,
                                opponent_initial_plays)

    def reset(self) -> None:
        super(LookerUp, self).reset()
        self._initial_actions_pool = list(self.initial_actions)

    @property
    def lookup_dict(self):
        return self._lookup.dictionary

    def lookup_table_display(
        self, sort_by: tuple = ('op_openings', 'self_plays', 'op_plays')
    ) -> str:
        """
        Returns a string for printing lookup_table info in specified order.

        :param sort_by: only_elements='self_plays', 'op_plays', 'op_openings'
        """
        return self._lookup.display(sort_by=sort_by)


class EvolvedLookerUp1_1_1(LookerUp):
    """
    A 1 1 1 Lookerup trained with an evolutionary algorithm.

    Names:

    - Evolved Lookerup 1 1 1: Original name by Marc Harper
    """
    name = "EvolvedLookerUp1_1_1"

    def __init__(self) -> None:
        params = Plays(self_plays=1, op_plays=1, op_openings=1)
        super().__init__(parameters=params, pattern='CDDDDCDD',
                         initial_actions=(C,))


class EvolvedLookerUp2_2_2(LookerUp):
    """
    A 2 2 2 Lookerup trained with an evolutionary algorithm.

    Names:

    - Evolved Lookerup 2 2 2: Original name by Marc Harper
    """
    name = "EvolvedLookerUp2_2_2"

    def __init__(self) -> None:
        params = Plays(self_plays=2, op_plays=2, op_openings=2)
        pattern = 'CDDCDCDDCDDDCDDDDDCDCDCCCDDCCDCDDDCCCCCDDDCDDDDDDDDDCCDDCDDDCCCD'
        super().__init__(parameters=params, pattern=pattern,
                         initial_actions=(C, C))


class Winner12(LookerUp):
    """
    A lookup table based strategy.

    Names:

    - Winner12: [Mathieu2015]_
    """
    name = "Winner12"

    def __init__(self) -> None:
        params = Plays(self_plays=1, op_plays=2, op_openings=0)
        pattern = 'CDCDDCDD'
        super().__init__(parameters=params, pattern=pattern,
                         initial_actions=(C, C))


class Winner21(LookerUp):
    """
    A lookup table based strategy.

    Names:

    - Winner21: [Mathieu2015]_
    """
    name = "Winner21"

    def __init__(self) -> None:
        params = Plays(self_plays=1, op_plays=2, op_openings=0)
        pattern = 'CDCDCDDD'
        super().__init__(parameters=params, pattern=pattern,
                         initial_actions=(D, C))


def get_last_n_plays(player: Player, depth: int) -> tuple:
    """Returns the last N plays of player as a tuple."""
    if depth == 0:
        return ()
    return tuple(player.history[-1 * depth:])
