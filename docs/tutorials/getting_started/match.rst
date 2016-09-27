.. _creating_matches:

Creating Matches
================

You can create your own match between two players using the :code:`Match` class.
This is often useful when designing new strategies in order to study how they
perform against specific opponents.

For example, to create a 5 turn match between :code:`Cooperator` and
:code:`Alternator`::

    >>> import axelrod as axl
    >>> players = (axl.Cooperator(), axl.Alternator())
    >>> match = axl.Match(players, 5)
    >>> match.play()
    [('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C')]

By default, a match will not be noisy, but you can introduce noise if you wish.
Noise is the probability with which any action dictated by a strategy will be
swapped::

    >>> match = axl.Match(players=players, turns=5, noise=0.2)
    >>> match.play()  # doctest: +SKIP
    [('D', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('D', 'D')]

The result of the match is held as an attribute within the :code:`Match` class.
Each time :code:`play()` is called, it will overwrite the content of that
attribute::

    >>> match.result  # doctest: +SKIP
    [('D', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('D', 'D')]
    >>> match.play()  # doctest: +SKIP
    [('C', 'C'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'C')]
    >>> match.result  # doctest: +SKIP
    [('C', 'C'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'C')]


The result of the match can also be viewed as sparklines where cooperation is
shown as a solid block and defection as a space. Sparklines are a very concise
way to view the result and can be useful for spotting patterns::


    >>> import axelrod as axl
    >>> players = (axl.Cooperator(), axl.Alternator())
    >>> match = axl.Match(players, 25)
    >>> match.play()
    [('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C')]
    >>> print(match.sparklines())  # doctest: +SKIP
    █████████████████████████
    █ █ █ █ █ █ █ █ █ █ █ █ █

The █ character for cooperation and a space for defection are default values
but you can use any characters you like::

    >>> import axelrod as axl
    >>> players = (axl.Cooperator(), axl.Alternator())
    >>> match = axl.Match(players, 25)
    >>> match.play()
    [('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C')]
    >>> print(match.sparklines(c_symbol='|', d_symbol='-'))
    |||||||||||||||||||||||||
    |-|-|-|-|-|-|-|-|-|-|-|-|

A `Match` class can also score the individual turns of a match. Just call
`match.scores()` after play::

    >>> import axelrod as axl
    >>> players = (axl.Cooperator(), axl.Alternator())
    >>> match = axl.Match(players, 25)
    >>> match.play()
    [('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C')]
    >>> match.scores()
    [(3, 3), (0, 5), (3, 3), (0, 5), (3, 3), (0, 5), (3, 3), (0, 5), (3, 3), (0, 5), (3, 3), (0, 5), (3, 3), (0, 5), (3, 3), (0, 5), (3, 3), (0, 5), (3, 3), (0, 5), (3, 3), (0, 5), (3, 3), (0, 5), (3, 3)]

There are various further methods::

    >>> match.final_score()
    (39, 99)
    >>> match.final_score_per_turn()
    (1.56, 3.96)
    >>> match.winner()
    Alternator
    >>> match.cooperation()  # The count of cooperations
    (25, 13)
    >>> match.normalised_cooperation()  # The count of cooperations per turn
    (1.0, 0.52)
