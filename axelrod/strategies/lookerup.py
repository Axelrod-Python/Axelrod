from axelrod import Player, Actions
import itertools

C, D = Actions.C, Actions.D

class LookerUp(Player):     

    """     
A strategy that uses a lookup table to
decide what to do based on a combination of the last m rounds and the opponent's
opening n moves. If there isn't enough history to do this (i.e. for the first m
rounds) then cooperate.

    The lookup table is implemented as a dict. The keys are 3-tuples giving the
    opponents first n moves, self's last m moves, and opponents last m moves,
    all as strings. The values are the moves to play on this round.  For
    example, if

        - the opponent started by playing C  
        - my last move was a C the opponents
        - last move was a D

    the corresponding key would be

        ('C', 'C', 'D')

    and the value would contain the move to play on this turn.

    Some well-known strategies can be expressed as special cases; for example
    Cooperator is given by the dict:

        {('', '', '') : 'C'}

    where m and n are both zero. Tit For Tat is given by:

    { 
        ('', 'C', 'D') : 'D',         
        ('', 'D', 'D') : 'D',         
        ('', 'C', 'C') : 'C',
        ('', 'D', 'C') : 'C',     
    }

    where m=1 and n=0.
    
    """
    

    name = 'LookerUp'
    classifier = {
        'memory_depth': float('inf'), 
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, lookup_table=None):
        """
        If no lookup table is provided to the constructor, then use the TFT one
        """
        Player.__init__(self)

        if not lookup_table:
            lookup_table = { 
            ('', 'C', 'D') : 'D',         
            ('', 'D', 'D') : 'D',         
            ('', 'C', 'C') : 'C',
            ('', 'D', 'C') : 'C',     
        }

        self.lookup_table = lookup_table


        # rather than pass number of previous rounds to consider in as a separate variable, figure it out
        # the number of rounds is the length of the second element of any given key in the dict 
        self.plays = len(self.lookup_table.keys()[0][1]) 

        # the number of opponent starting moves is the lgnth of the first element of any given key in the dict
        self.opponent_start_plays = len(self.lookup_table.keys()[0][0])

        if self.opponent_start_plays == 0:
            self.classifier['memory_depth'] = self.plays

        self.init_args = (lookup_table,)

    def strategy(self, opponent):
        """
        If there isn't enough history to lookup a move from the table, cooperate
        """
        if len(self.history) < max([self.plays,self.opponent_start_plays]) :
            return 'C'
            
        else:
            # count back m moves to get my own recent history
            history_start = -1 * self.plays
            my_history = ''.join(self.history[history_start:])

            # do the same for the opponent
            opponent_history = ''.join(opponent.history[history_start:])

            # get the opponents first n moves
            opponent_start = ''.join(opponent.history[0:self.opponent_start_plays])

            # put these three strings together in a tuple
            key = (opponent_start, my_history, opponent_history)

            # look up the move associated with that tuple in the lookup table
            move = self.lookup_table[key]

            return move


class EvolvedLookerUp(LookerUp):
    """
    A LookerUp strategy that uses a lookup table generated using an evolutionary algorithm. 
    //TODO: update this docstring with a link to a blog post once I've written about it :-)
    """

    def __init__(self):
        plays = 2
        opponent_start_plays = 2

        # functionaly generate the list of possible tuples (i.e. all possible combinations of m moves for me, m moves for opponent, and n starting moves for opponent) 
        self_histories = [''.join(x) for x in itertools.product('CD', repeat=plays)]
        other_histories = [''.join(x) for x in itertools.product('CD', repeat=plays)]
        opponent_starts = [''.join(x) for x in itertools.product('CD', repeat=opponent_start_plays)]
        lookup_table_keys = list(itertools.product(opponent_starts,self_histories, other_histories))

        # pattern of values determed with an evolutionary algorithm (blog post to follow)
        pattern='CDCCDCCCDCDDDDDCCDCCCDDDCDDDDDDCDDDDCDDDDCCDDCDDCDDDCCCDCDCDDDDD'

        # zip together the keys and the move pattern to get the lookup table
        lookup_table = dict(zip(lookup_table_keys, pattern))

        LookerUp.__init__(self, lookup_table=lookup_table)
