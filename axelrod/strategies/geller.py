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

This code will fall into infinite recursion when played against itself,
a problem that can be alleviated by looking at the name of the function
calling `strategy`. If it is also `strategy`, we should return some
default value - for example 'C', 'D' or random.
"""

import inspect
import random

from axelrod import Player


class Geller(Player):

    default = lambda self: 'C' if random.random() > 0.5 else 'D'

    def strategy(self, opponent):
        """
        Look at what the opponent will play in the next round and choose a strategy
        that gives the least jail time, which is is equivalent to playing the same
        strategy as that which the opponent will play.
        """
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        calname = calframe[1][3]
        if calname == 'strategy':
            return self.default()
        else:
            return opponent.strategy(self)

    def __repr__(self):
        """
        The string method for the strategy:
        """
        return 'Geller'

class GellerCooperator(Geller):
    default = lambda self: 'C'
    __repr__ = lambda self: 'Geller Cooperator'

class GellerDefector(Geller):
    default = lambda self: 'D'
    __repr__ = lambda self: 'Geller Defector'