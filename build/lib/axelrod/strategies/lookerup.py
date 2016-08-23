from axelrod import Actions, Player, init_args
from itertools import product

C, D = Actions.C, Actions.D


class LookerUp(Player):
    """
    A strategy that uses a lookup table to decide what to do based on a
    combination of the last m turns and the opponent's opening n actions. If
    there isn't enough history to do this (i.e. for the first m turns) then
    cooperate.

    The lookup table is implemented as a dict. The keys are 3-tuples giving the
    opponents first n actions, self's last m actions, and opponents last m
    actions, all as strings. The values are the actions to play on this round.
    For example, in the case of m=n=1, if

    * the opponent started by playing C
    * my last action was a C the opponents
    * last action was a D

    then the corresponding key would be::

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
    Below is an incomplete example where m=3 and n=2::

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
    def __init__(self, lookup_table=None, value_length=1):
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
        # The number of opponent starting actions is the length of the first
        # element of any given key in the dict.
        self.opponent_start_plays = len(list(self.lookup_table.keys())[0][0])
        # If the table dictates to ignore the opening actions of the opponent
        # then the memory classification is adjusted
        if self.opponent_start_plays == 0:
            self.classifier['memory_depth'] = self.plays

        # Ensure that table is well-formed
        for k, v in lookup_table.items():
            if (len(k[1]) != self.plays) or (len(k[0]) != self.opponent_start_plays):
                raise ValueError("All table elements must have the same size")
            if value_length is not None:
                if len(v) > value_length:
                    raise ValueError("Table values should be of length one, C or D")

    def strategy(self, opponent):
        # If there isn't enough history to lookup an action, cooperate.
        if len(self.history) < max(self.plays, self.opponent_start_plays):
            return C
        # Count backward m turns to get my own recent history.
        if self.plays == 0:
            my_history = ''
            opponent_history = ''
        else:
            history_start = -1 * self.plays
            my_history = ''.join(self.history[history_start:])
            # Do the same for the opponent.
            opponent_history = ''.join(opponent.history[history_start:])
            # Get the opponents first n actions.
        opponent_start = ''.join(opponent.history[:self.opponent_start_plays])
        # Put these three strings together in a tuple.
        key = (opponent_start, my_history, opponent_history)
        # Look up the action associated with that tuple in the lookup table.
        action = self.lookup_table[key]
        return action


def create_lookup_table_keys(plays=2, opponent_start_plays=2):
    """Creates the keys for a lookup table."""
    self_histories = [''.join(x) for x in product('CD', repeat=plays)]
    other_histories = [''.join(x) for x in product('CD', repeat=plays)]
    opponent_starts = [''.join(x) for x in
                       product('CD', repeat=opponent_start_plays)]
    lookup_table_keys = list(product(opponent_starts, self_histories,
                                         other_histories))
    return lookup_table_keys


class EvolvedLookerUp(LookerUp):
    """
    A LookerUp strategy that uses a lookup table generated using an evolutionary
    algorithm.

    A description of how this strategy was trained is given here:
    http://mojones.net/evolving-strategies-for-an-iterated-prisoners-dilemma-tournament.html
    """

    name = "EvolvedLookerUp"

    def __init__(self):
        lookup_table_keys = create_lookup_table_keys(plays=2,
                                                     opponent_start_plays=2)

        # Pattern of values determed previously with an evolutionary algorithm.
        pattern='CDCCDCCCDCDDDDDCCDCCDDDDDCDCDDDCDDDDCCCDDCCDDDDDCDCDDDCDCDDDDDDD'
        # Zip together the keys and the action pattern to get the lookup table.
        lookup_table = dict(zip(lookup_table_keys, pattern))
        LookerUp.__init__(self, lookup_table=lookup_table)
