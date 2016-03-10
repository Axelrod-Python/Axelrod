class Gambler(Player):

    name = 'Gambler'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
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
            ('', 'C', 'D') : 0,
            ('', 'D', 'D') : 0,
            ('', 'C', 'C') : 1,
            ('', 'D', 'C') : 1,
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


    def strategy(self, opponent):
        # If there isn't enough history to lookup an action, cooperate.
        if len(self.history) < max(self.plays, self.opponent_start_plays):
            return C
        # GK: Defect Last 2 turns
        if len(opponent.history) > (self.tournament_attributes['length'] - 3):
            return D
        # Count backward m turns to get my own recent history.
        history_start = -1 * self.plays
        my_history = ''.join(self.history[history_start:])
        # Do the same for the opponent.
        opponent_history = ''.join(opponent.history[history_start:])
        # Get the opponents first n actions.
        opponent_start = ''.join(opponent.history[:self.opponent_start_plays])
        # Put these three strings together in a tuple.
        key = (opponent_start, my_history, opponent_history)
        # Look up the action number associated with that tuple in the lookup table.
        action = float(self.lookup_table[key])
        # Depending on the action number return a choice
        return random_choice(action)



class PSOGambler(Gambler):
    """
    A LookerUp strategy that uses a lookup table with probability numbers generated using 
    a Particle Swarm Optimisation (PSO) algorithm.
    """

    name = "PSO Gambler"

    def __init__(self,pattern):
        plays = 2
        opponent_start_plays = 2

        # Generate the list of possible tuples, i.e. all possible combinations
        # of m actions for me, m actions for opponent, and n starting actions
        # for opponent.
        self_histories = [''.join(x) for x in product('CD', repeat=plays)]
        other_histories = [''.join(x) for x in product('CD', repeat=plays)]
        opponent_starts = [''.join(x) for x in
                           product('CD', repeat=opponent_start_plays)]
        lookup_table_keys = list(product(opponent_starts, self_histories,
                                         other_histories))

        # Pattern of values determed previously with a pso algorithm.
        pattern_pso = [1.0 ,0.0,1.0,1.0 ,0.0 ,1.0,1.0,1.0,0.0 ,1.0 ,0.0,0.0,0.0,0.0,0.0,1.0 ,
                       0.93,0.0,1.0,0.67,0.42,0.0,0.0,0.0,0.0 ,1.0 ,0.0,1.0,0.0,0.0,0.0,0.48,
                       0.0 ,0.0,0.0,0.0 ,1.0 ,1.0,1.0,0.0,0.19,1.0 ,1.0,0.0,0.0,0.0,0.0,0.0 ,
                       1.0 ,0.0,1.0,0.0 ,0.0 ,0.0,1.0,0.0,1.0 ,0.36,0.0,0.0,0.0,0.0,0.0,0.0 ]

        # Zip together the keys and the action pattern to get the lookup table.
        lookup_table = dict(zip(lookup_table_keys, pattern))
        Gambler.__init__(self, lookup_table=lookup_table)
