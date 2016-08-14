.. _creating_tournaments:

Creating and running a simple tournament
========================================

The following lines of code creates a list players playing simple
strategies::

    >>> import axelrod as axl
    >>> players = [axl.Cooperator(), axl.Defector(),
    ...            axl.TitForTat(), axl.Grudger()]
    >>> players
    [Cooperator, Defector, Tit For Tat, Grudger]

We can now create a tournament, play it, save the results and view the rank of
each player::

    >>> tournament = axl.Tournament(players)
    >>> results = tournament.play()
    >>> results.ranked_names
    ['Defector', 'Tit For Tat', 'Grudger', 'Cooperator']

We can also plot these results::

    >>> plot = axl.Plot(results)
    >>> p = plot.boxplot()
    >>> p.show()

.. image:: _static/getting_started/demo_deterministic_strategies_boxplot.svg
   :width: 50%
   :align: center

Note that in this case none of our strategies are stochastic so the boxplot
shows that there is no variation. Take a look at the :ref:`visualising-results`
section to see plots showing a stochastic effect.
