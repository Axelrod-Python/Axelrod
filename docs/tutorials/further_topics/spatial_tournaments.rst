Spatial tournaments
===================

A spatial tournament is defined on a graph where the nodes correspond to players
and edges define whether or not a given player pair will have a match.

The initial work on spatial tournaments was done by Nowak and May in a 1992
paper: [Nowak1992]_.

Additionally, Szabó and Fáth in their 2007 paper [Szabo2007]_ consider a variety
of graphs, such as lattices, small world, scale-free graphs and evolving
networks.

Let's create a tournament where :code:`Cooperator` and :code:`Defector` do not
play each other and neither do :code:`TitForTat` and :code:`Grudger` :

.. image:: _static/spatial_tournaments/spatial.png
   :width: 80%
   :align: center

Note that the edges have to be given as a list of tuples of player
indices::

  >>> import axelrod as axl
  >>> players = [axl.Cooperator(), axl.Defector(),
  ...            axl.TitForTat(), axl.Grudger()]
  >>> edges = [(0, 2), (0, 3), (1, 2), (1, 3)]

To create a spatial tournament you pass the :code:`edges` to the
:code:`Tournament` class::

    >>> spatial_tournament = axl.Tournament(players, edges=edges)
    >>> results = spatial_tournament.play()

We can plot the results::

    >>> plot = axl.Plot(results)
    >>> p = plot.boxplot()
    >>> p.show()

.. image:: _static/spatial_tournaments/spatial_results.png
     :width: 50%
     :align: center

We can, like any other tournament, obtain the ranks for our players::

   >>> results.ranked_names
   ['Cooperator', 'Tit For Tat', 'Grudger', 'Defector']

Let's run a small tournament of 2 :code:`turns` and 2 :code:`repetitions`
and obtain the interactions::

    >>> spatial_tournament = axl.Tournament(players ,turns=2, repetitions=2, edges=edges)
    >>> results = spatial_tournament.play()
    >>> results.payoffs
    [[[], [], [3.0, 3.0], [3.0, 3.0]], [[], [], [3.0, 3.0], [3.0, 3.0]], [[3.0, 3.0], [0.5, 0.5], [], []], [[3.0, 3.0], [0.5, 0.5], [], []]]

As anticipated not all players interact with each other.

It is also possible to create a probabilistic ending spatial tournament::

    >>> prob_end_spatial_tournament = axl.Tournament(players, edges=edges, prob_end=.1, repetitions=1)
    >>> axl.seed(0)
    >>> prob_end_results = prob_end_spatial_tournament.play()

We see that the match lengths are no longer all equal::

    >>> prob_end_results.match_lengths
    [[[0, 0, 18.0, 14.0], [0, 0, 6.0, 3.0], [18.0, 6.0, 0, 0], [14.0, 3.0, 0, 0]]]
