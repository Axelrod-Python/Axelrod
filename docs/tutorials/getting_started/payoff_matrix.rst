.. _payoff-matrix:

Accessing the payoff matrix
===========================

This tutorial will show you briefly how to access the payoff matrix
corresponding to the tournament.

As shown in :ref:`getting-started` let us create a tournament::

    >>> import axelrod as axl
    >>> players = [axl.Cooperator(), axl.Defector(),
    ...            axl.TitForTat(), axl.Grudger()]
    >>> tournament = axl.Tournament(players)
    >>> results = tournament.play()

We can view the payoff matrix of our tournament showing the score of the row-th
strategy when played against the column-th strategy::

    >>> m = results.payoff_matrix
    >>> for row in m:
    ...     print([round(ele, 1) for ele in row]) # Rounding output
    [3.0, 0.0, 3.0, 3.0]
    [5.0, 1.0, 1.0, 1.0]
    [3.0, 1.0, 3.0, 3.0]
    [3.0, 1.0, 3.0, 3.0]

Here we see that the second strategy (:code:`Defector`) obtains an average
utility per game of :code:`5.0` against the first strategy (:code:`Cooperator`)
as expected.

