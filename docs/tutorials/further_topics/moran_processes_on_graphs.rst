.. _moran-process-on-graphs:

Moran Process on Graphs
=======================

The library also provides a graph-based Moran process [Shakarian2013]_ with
:code:`MoranProcessGraph`.  To use this class you must supply at least one
:code:`Axelrod.graph.Graph` object, which can be initialized with just a list of
edges::

    edges = [(source_1, target1), (source2, target2), ...]

The nodes can be any hashable object (integers, strings, etc.). For example::

    >>> import axelrod as axl
    >>> from axelrod.graph import Graph
    >>> edges = [(0, 1), (1, 2), (2, 3), (3, 1)]
    >>> graph = Graph(edges)

Graphs are undirected by default. Various intermediates such as the list of
neighbors are cached for efficiency by the graph object.

A Moran process can be invoked with one or two graphs. The first graph, the
*interaction graph*, dictates how players are matched up in the scoring phase.
Each player plays a match with each neighbor. The second graph dictates how
players replace another during reproduction. When an individual is selected to
reproduce, it replaces one of its neighbors in the *reproduction graph*. If only
one graph is supplied to the process, the two graphs are assumed to be the same.

To create a graph-based Moran process, use a graph as follows::

    >>> from axelrod.graph import Graph
    >>> axl.seed(40)
    >>> edges = [(0, 1), (1, 2), (2, 3), (3, 1)]
    >>> graph = Graph(edges)
    >>> players = [axl.Cooperator(), axl.Cooperator(), axl.Cooperator(), axl.Defector()]
    >>> mp = axl.MoranProcessGraph(players, interaction_graph=graph)
    >>> results = mp.play()
    >>> mp.population_distribution()
    Counter({'Cooperator': 4})

You can supply the `reproduction_graph` as a keyword argument. The standard Moran
process is equivalent to using a complete graph for both graphs.
