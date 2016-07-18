Spatial tournaments
===================

In a spatial topology tournament the connectivity between players is given by
a graph where the nodes represent players, and  the  edges, connecting the nodes,
refer to the connection between the corresponding players.

The initial work was done by Nowak  and May in a 1992 paper, "Evolutionary games
and spatial chaos", introducing spatial topology as a square lattice. (The
paper can be found here: http://www.nature.com/nature/journal/v359/n6398/abs/359826a0.html).

Additionally, Szabó and Fáth in their 2007 paper consider a variety of graphs,
such as lattices, small world, scale-free graphs and evolving networks. (Their
paper can be found here: https://arxiv.org/abs/cond-mat/0607344).

Even so, here it is possible to create a tournament where the players are
allocated to any given graph and they only interact with players to which they
have a connection - edge.

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

To create a spatial tournament you call the :code:`SpatialTournamnent` class::

    >>> spatial_tournament = axl.SpatialTournament(players, edges=edges)
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

Let's run small tournament of 2 :code:`turns` and 5 :code:`repetitions`
and obtain the interactions::

    >>> spatial_tournament = axl.SpatialTournament(players ,turns=2, repetitions=2, edges=edges)
    >>> results = spatial_tournament.play()
    >>> for index_pair, interaction in results.interactions.items():
    ...     player1 = spatial_tournament.players[index_pair[0]]
    ...     player2 = spatial_tournament.players[index_pair[1]]
    ...     print('%s vs %s: %s' % (player1, player2, interaction))
    Defector vs Tit For Tat: [[('D', 'C'), ('D', 'D')], [('D', 'C'), ('D', 'D')]]
    Cooperator vs Grudger: [[('C', 'C'), ('C', 'C')], [('C', 'C'), ('C', 'C')]]
    Defector vs Grudger: [[('D', 'C'), ('D', 'D')], [('D', 'C'), ('D', 'D')]]
    Cooperator vs Tit For Tat: [[('C', 'C'), ('C', 'C')], [('C', 'C'), ('C', 'C')]]

As anticipated  :code:`Cooperator` does not interact with :code:`Defector` neither
:code:`TitForTat` with :code:`Grudger`.
