# -*- coding: utf-8 -*-

"""
Geller - by Martin Chorley (@martinjc), heavily inspired by Matthew Williams (@voxmjw)

This code is inspired by Matthew Williams' talk 
"Cheating at rock-paper-scissors — meta-programming in Python"
given at Django Weekend Cardiff in February 2014.

His code is here: https://github.com/mattjw/rps_metaprogramming
and there's some more info here: http://www.mattjw.net/2014/02/rps-metaprogramming/

This code is **way** simpler than Matt's, as in this exercise we already
have access to the opponent instance, so don't need to go 
hunting for it in the stack. Instead we can just call it to
see what it's going to play, and return a result based on that

This is almost certainly cheating, and more than likely against the
spirit of the 'competition' :-)
"""

import random
from axelrod import Player


class Geller(Player):

    def strategy(self, opponent):

        #
        # See what the opponent will throw
        # respond with whatever gives least jail time
        rand_state = random.getstate()
        opp_move = opponent.strategy(self)
        random.setstate(rand_state)

        if opp_move == 'C':
            return 'C'
        elif opp_move == 'D':
            return 'D'

    def __repr__(self):
        """
        The string method for the strategy:
        """
        return 'Geller'
