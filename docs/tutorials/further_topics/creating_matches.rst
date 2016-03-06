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

By default, a match will not be noisy, but you can introduce noise if you wish::

    >>> import axelrod as axl
    >>> players = (axl.Cooperator(), axl.Alternator())
    >>> match = axl.Match(players=players, turns=5, noise=0.2)
    >>> match.play() # doctest: +SKIP
    [('D', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C')]

The result of the match is held as an attribute within the :code:`Match` class.
Each time :code:`play()` is called, it will overwrite the content of that
attribute::

    >>> import axelrod as axl
    >>> players = (axl.Cooperator(), axl.Alternator())
    >>> match = axl.Match(players=players, turns=5, noise=0.2)
    >>> match.play()  # doctest: +SKIP
    [('D', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C')]
    >>> match.result # doctest: +SKIP
    [('D', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C')]
    >>> match.play() # doctest: +SKIP
    [('D', 'C'), ('D', 'C'), ('C', 'D'), ('C', 'D'), ('C', 'C')]
    >>> match.result # doctest: +SKIP
    [('D', 'C'), ('D', 'C'), ('C', 'D'), ('C', 'D'), ('C', 'C')]


The result of the match can also be viewed as sparklines where cooperation is
shown as a solid block and defection as a space. Sparklines are a very concise
way to view the result and can be useful for spotting patterns::


    >>> import axelrod as axl
    >>> players = (axl.Cooperator(), axl.Alternator())
    >>> match = axl.Match(players, 25)
    >>> match.play()
    [('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C')]
    >>> print(match.sparklines()) # doctest: +SKIP
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

It is also possible to create matches that that have a given probability of
ending after certain number of turns::

    >>> import axelrod as axl
    >>> players = (axl.Cooperator(), axl.Alternator())
    >>> match = axl.Match(players, 25, prob_end=.4)
    >>> match.play() # doctest: +SKIP
    [('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C')]

In that particular instance the probability of any turn being the last is .4 so the mean length of a match would in fact be :math:`1/0.6\approx 1.667`. Note that you can also pass an infinite amount of turns when passing an ending probability::

    >>> players = (axl.Cooperator(), axl.Alternator())
    >>> match = axl.Match(players, turns=float("inf"), prob_end=.4)
    >>> match.play() # doctest: +SKIP
    [('C', 'C'), ('C', 'D')]
