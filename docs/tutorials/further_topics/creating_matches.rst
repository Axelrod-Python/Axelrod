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
    >>> match.play()
    [('D', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C')]

The result of the match is held as an attribute within the :code:`Match` class.
Each time :code:`play()` is called, it will overwrite the content of that
attribute::

    >>> import axelrod as axl
    >>> players = (axl.Cooperator(), axl.Alternator())
    >>> match = axl.Match(players=players, turns=5, noise=0.2)
    >>> match.play()
    [('D', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C')]
    >>> match.result
    [('D', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C')]
    >>> match.play()
    [('D', 'C'), ('D', 'C'), ('C', 'D'), ('C', 'D'), ('C', 'C')]
    >>> match.result
    [('D', 'C'), ('D', 'C'), ('C', 'D'), ('C', 'D'), ('C', 'C')]


The result of the match can also be viewed as sparklines where cooperation is
shown as a solid block and defection as a space. Sparklines are a very concise
way to view the result and can be useful for spotting patterns::


    >>> import axelrod as axl
    >>> players = (axl.Cooperator(), axl.Alternator())
    >>> match = axl.Match(players, 25)
    >>> match.play()
    [('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C')]
    >>> print(match.sparklines)
    █████████████████████████
    █ █ █ █ █ █ █ █ █ █ █ █ █
