from functools import partial
from itertools import product
import sys

from axelrod import Actions, Player, init_args, load_lookerup_tables
from axelrod.strategy_transformers import InitialTransformer

module = sys.modules[__name__]
C, D = Actions.C, Actions.D

# Dictionary of table patterns
# Keys are (plays, opp_plays, opponent_start_plays)
patterns = load_lookerup_tables()


def create_lookup_table_keys(plays=2, opp_plays=None, opponent_start_plays=2):
    """Creates the keys for a lookup table."""
    if opp_plays is None:
        opp_plays = plays
    self_histories = [''.join(x) for x in product('CD', repeat=plays)]
    other_histories = [''.join(x) for x in product('CD', repeat=opp_plays)]
    opponent_starts = [''.join(x) for x in
                       product('CD', repeat=opponent_start_plays)]
    lookup_table_keys = list(product(opponent_starts, self_histories,
                                         other_histories))
    return lookup_table_keys

def create_lookup_table_from_pattern(
    plays=2, opp_plays=None, opponent_start_plays=2, pattern=None):
    lookup_table_keys = create_lookup_table_keys(
        plays=plays, opp_plays=opp_plays,
        opponent_start_plays=opponent_start_plays)
    table = dict(zip(lookup_table_keys, pattern))
    return table


class LookerUp(Player):
    """
    A strategy that uses a lookup table to decide what to do based on a
    combination of the last m1 plays, m2 opponent plays, and the opponent's
    opening n actions. If there isn't enough history to do this (i.e. for the
    first m1 or m2 turns) then cooperate.

    The lookup table is implemented as a dict. The keys are 3-tuples giving the
    opponents first n actions, self's last m1 actions, and opponents last m2
    actions, all as strings. The values are the actions to play on this round.

    For example, in the case of m1=m2=n=1, if
    - the opponent started by playing C
    - my last action was a C the opponents
    - last action was a D
    then the corresponding key would be

        ('C', 'C', 'D')

    and the value would contain the action to play on this turn.

    Some well-known strategies can be expressed as special cases; for example
    Cooperator is given by the dict::

        {('', '', '') : C}

    where m and n are both zero. Tit-For-Tat is given by::

       {('', 'C', 'D'): D,
        ('', 'D', 'D'): D,
        ('', 'C', 'C'): C,
        ('', 'D', 'C'): C}

    where m=1 and n=0.

    Lookup tables where the action depends on the opponent's first actions (as
    opposed to most recent actions) will have a non-empty first string in the
    tuple. For example, this fragment of a dict::

       {('C', 'C', 'C'): C,
        ('D', 'C', 'C'): D}

    states that if self and opponent both cooperated on the previous turn, we
    should cooperate this turn unless the opponent started by defecting, in
    which case we should defect.

    To denote lookup tables where the action depends on sequences of actions
    (so m or n are greater than 1), simply concatenate the strings together.

    Below is an incomplete example where m1=m2=3 and n=2.

       {('CC', 'CDD', 'CCC'): C,
        ('CD', 'CCD', 'CCC'): D}
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

    @init_args
    def __init__(self, lookup_table=None):
        """
        If no lookup table is provided to the constructor, then use the TFT one.
        """
        Player.__init__(self)

        if not lookup_table:
            lookup_table = {
                ('', 'C', 'D'): D,
                ('', 'D', 'D'): D,
                ('', 'C', 'C'): C,
                ('', 'D', 'C'): C,
            }

        self.lookup_table = lookup_table
        # Rather than pass the number of previous turns (m) to consider in as a
        # separate variable, figure it out. The number of turns is the length
        # of the second element of any given key in the dict.
        self.plays = len(list(self.lookup_table.keys())[0][1])
        self.opp_plays = len(list(self.lookup_table.keys())[0][2])
        # The number of opponent starting actions is the length of the first
        # element of any given key in the dict.
        self.opponent_start_plays = len(list(self.lookup_table.keys())[0][0])
        # If the table dictates to ignore the opening actions of the opponent
        # then the memory classification is adjusted
        if self.opponent_start_plays == 0:
            self.classifier['memory_depth'] = max(self.plays, self.opp_plays)
        else:
            self.classifier['memory_depth'] = float('inf')

        # Ensure that table is well-formed
        for k, v in lookup_table.items():
            if (len(k[1]) != self.plays) or \
               (len(k[0]) != self.opponent_start_plays) or \
               (len(k[2]) != self.opp_plays):
                raise ValueError("All table elements must have the same size")


    def strategy(self, opponent):
        # If there isn't enough history to lookup an action, cooperate.
        table_depth = max(self.opp_plays, self.plays, self.opponent_start_plays)
        if len(self.history) < table_depth:
            return C
        # Count backward m turns to get my own recent history.
        if self.plays == 0:
            my_history = ''
        else:
            history_start = -1 * self.plays
            my_history = ''.join(self.history[history_start:])
        if self.opp_plays == 0:
            opponent_history = ''
        else:
            history_start = -1 * self.opp_plays
            opponent_history = ''.join(opponent.history[history_start:])
        opponent_start = ''.join(opponent.history[:self.opponent_start_plays])
        # Put these three strings together in a tuple.
        key = (opponent_start, my_history, opponent_history)
        # Look up the action associated with that tuple in the lookup table.
        action = self.lookup_table[key]
        return action


# Create several classes at runtime based on the data in the look up tables
# loaded above, one for each key.

for k, pattern in patterns.items():
    plays, opp_plays, opp_start_plays = k
    table = create_lookup_table_from_pattern(
        plays, opp_plays, opp_start_plays, pattern)
    class_name = "EvolvedLookerUp{}_{}_{}".format(
        plays, opp_plays, opp_start_plays)
    # Dynamically create the class
    new_class = type(class_name, (LookerUp,), {})
    new_class.__init__ = init_args(partial(
        new_class.__init__, lookup_table=table))
    new_class.name = class_name
    # Add the generated class to the module dictionary so it can be
    # imported into other modules
    setattr(module, class_name, new_class)


@InitialTransformer((C, C), name_prefix=None)
class Winner12(LookerUp):
    """
    Names:
        - Winner12 [Mathieu2015]
    """
    name = "Winner12"

    def __init__(self):
        lookup_table_keys = create_lookup_table_keys(
            plays=1, opp_plays=2, opponent_start_plays=0)

        pattern = 'CDCDDCDD'
        # Zip together the keys and the action pattern to get the lookup table.
        lookup_table = dict(zip(lookup_table_keys, pattern))
        LookerUp.__init__(self, lookup_table=lookup_table)


@InitialTransformer((D, C), name_prefix=None)
class Winner21(LookerUp):
    """
    Names:
        - Winner21 [Mathieu2015]
    """
    name = "Winner21"

    def __init__(self):
        lookup_table_keys = create_lookup_table_keys(
            plays=2, opp_plays=1, opponent_start_plays=0)

        pattern = 'CDCDCDDD'
        # Zip together the keys and the action pattern to get the lookup table.
        lookup_table = dict(zip(lookup_table_keys, pattern))
        LookerUp.__init__(self, lookup_table=lookup_table)
