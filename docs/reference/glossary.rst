Glossary
========

There are a variety of terms used in the documentation and throughout the
library. Here is an overview:

An action
---------

An **action** is either :code:`C` or :code:`D`.
You can access these actions as follows but should not really have a reason to::

    >>> import axelrod as axl
    >>> axl.Actions.C
    'C'
    >>> axl.Actions.D
    'D'

A play
------

A **play** is a single player choosing an **action**.
In terms of code this is equivalent to::

    >>> p1, p2 = axl.Cooperator(), axl.Defector()
    >>> p1.play(p2)  # This constitues two 'plays' (p1 plays and p2 plays).

This is equivalent to :code:`p2.play(p1)`. Either function invokes both
:code:`p1.strategy(p2)` and :code:`p2.strategy(p1)`.

A turn
------

A **turn** is a 1 shot interaction between two players. It is in effect a
composition of two **plays**.

Each turn has four possible outcomes of a play: :code:`(C, C)`, :code:`(C, D)`,
:code:`(D, C)`, or :code:`(D, D)`.

A match
-------

A **match** is a consecutive number of **turns**. The default number of turns
used in the tournament is 200. Here is a single match between two players over
10 turns::

    >>> p1, p2 = axl.Cooperator(), axl.Defector()
    >>> for turn in range(10):
    ...     p1.play(p2)
    >>> p1.history, p2.history
    (['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C'], ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'])

A win
-----

A **win** is attributed to the player who has the higher total score at the end
of a match. For the example above, :code:`Defector` would win that match.

A strategy
----------

A **strategy** is a set of instructions that dictate how to play given one's own
strategy and the strategy of an opponent. In the library these correspond to the
strategy classes: `TitForTat`, `Grudger`, `Cooperator` etc...

When appropriate to do so this will be used interchangeable with `A player`_.

A player
--------

A **player** is a single agent using a given strategy. Players are the
participants of tournament, usually they each represent one strategy but of
course you can have multiple players choosing the same strategy. In the library
these correspond to __instances__ of classes::

    >>> p1, p2 = axl.Cooperator(), axl.Defector()
    >>> p1
    Cooperator
    >>> p2
    Defector

When appropriate to do so this will be used interchangeable with `A strategy`_.

A round robin
-------------

A **round robin** is the set of all potential (order invariant) matches between
a given collection of players.

A tournament
------------

A **tournament** is a repetition of round robins so as to smooth out stochastic effects.

Noise
-----

A match or tournament can be played with **noise**: this is the probability that
indicates the chance of an action dictated by a strategy being swapped.
